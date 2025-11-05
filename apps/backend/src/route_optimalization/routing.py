"""Vehicles Routing Problem (VRP) with Time Windows."""

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

from src.data_model.place.place import Place
from src.data_model.places.places import Places
from src.travel_time import travel_estimator


class Routing:
    def __init__(self, places: Places, depot=None, num_routes=1, period_index=0):
        self.places = places
        self.num_routes = num_routes
        self.depot_idx = 0
        self.depot = depot
        self.period_index = period_index
        self.max_time = 22 * 60
        self.transport_modes = None
        self.matrix = self._make_time_matrix()
        self.time_windows = self._open_close_time()

    def _make_time_matrix(self):
        """Function that makes a time matrix for each day.
        :return: time matrix for each day"""

        places_list = self.places.get_list()
        places_list.insert(0, self.depot)
        time_matrix = [[0 for _ in range(len(places_list))] for _ in range(len(places_list))]
        self.transport_modes = [['' for _ in range(len(places_list))] for _ in range(len(places_list))]
        for idx_day, place1 in enumerate(places_list):
            for idx_day2, place2 in enumerate(places_list):
                if idx_day == idx_day2:
                    travel_time = 0
                    transport_mode = ''
                else:
                    travel_time, transport_mode = travel_estimator.get_estimated_time(
                        place1.location, place2.location, self.places.city)
                time_matrix[idx_day][idx_day2] = travel_time
                time_matrix[idx_day2][idx_day] = travel_time
                self.transport_modes[idx_day][idx_day2] = transport_mode
                self.transport_modes[idx_day2][idx_day] = transport_mode
        return time_matrix

    def _print_time_matrix(self, time_matrix):
        """Function that prints a time matrix.
        :param time_matrix: time matrix
        :return: None"""
        for row in time_matrix:
            print(row)

    def _open_close_time(self):
        """Function that returns the opening and closing time for a place.
        :return: opening and closing time for a place"""
        time_for_place = []
        for place in self.places.get_list():
            opening_time, closing_time = self._get_opening_close_time(place)
            adjusted_close = min(max(opening_time, closing_time - place.estimatedTime), self.max_time)
            adjusted_open = min(opening_time, adjusted_close)
            time_for_place.append((adjusted_open, adjusted_close))
        time_for_place.insert(0, (600, self.max_time))
        return time_for_place

    def _get_opening_close_time(self, place: Place):
        """Function that returns the opening and closing time for a place.
        :param place: place
        :return: opening and closing time for a place"""
        opening_time = place.regularOpeningHours.periods[self.period_index].open_in_minutes
        closing_time = place.regularOpeningHours.periods[self.period_index].close_in_minutes
        return opening_time, closing_time

    def print_solution(self, manager, routing, solution):
        """Prints solution on console."""
        print(f"Objective: {solution.ObjectiveValue()}")
        dropped_nodes = "Dropped nodes:"
        for node in range(routing.Size()):
            if routing.IsStart(node) or routing.IsEnd(node):
                continue
            if solution.Value(routing.NextVar(node)) == node:
                dropped_nodes += f" {manager.IndexToNode(node)} rating: {self.places.get_by_index(manager.IndexToNode(node) - 1).ratings.cumulative_rating} "
        print(dropped_nodes)
        print(f"Objective: {solution.ObjectiveValue()}")
        time_dimension = routing.GetDimensionOrDie("Time")
        total_time = 0
        last_time = 0
        last_time_spent = 0
        for vehicle_id in range(self.num_routes):
            index = routing.Start(vehicle_id)
            plan_output = f"Route for vehicle {vehicle_id}:\n"
            while not routing.IsEnd(index):
                time_var = time_dimension.CumulVar(index)
                node = manager.IndexToNode(index)
                if node != 0:
                    place = self.places.get_by_index(node - 1)
                else:
                    place = self.depot
                open_close = place.regularOpeningHours.periods[self.period_index]
                if last_time != 0:
                    plan_output += f'Travel for {solution.Min(time_var) - last_time - last_time_spent}min'
                plan_output += (
                    "\n->"
                    f"\n{place.placeInfo.displayName} {node}"
                    f"\nHours: {int(open_close.open.sum_minutes / 60)}:{open_close.open.sum_minutes % 60} "
                    f"- {int(open_close.close.sum_minutes / 60)}:{open_close.close.sum_minutes % 60}"
                    f"\nRating: {place.ratings.cumulative_rating}"
                    f"\nTime({int(solution.Min(time_var) / 60)}:{solution.Min(time_var) % 60}, {int(solution.Max(time_var) / 60)}:{solution.Max(time_var) % 60})"
                    f"\nSpend here: {place.estimatedTime}min\n"
                    "->\n"
                )

                last_time = solution.Min(time_var)
                last_time_spent = place.estimatedTime
                index = solution.Value(routing.NextVar(index))
            time_var = time_dimension.CumulVar(index)
            place = self.depot
            plan_output += (
                f'Travel for {solution.Min(time_var) - last_time - last_time_spent}min'
                "\n->"
                f"\n{place.placeInfo.displayName}"
                f"\nHours: {int(open_close.open.sum_minutes / 60)}:{open_close.open.sum_minutes % 60} "
                f"- {int(open_close.close.sum_minutes / 60)}:{open_close.close.sum_minutes % 60}"
                f"\nRating: {place.ratings.cumulative_rating}"
                f"\nTime({int(solution.Min(time_var) / 60)}:{solution.Min(time_var) % 60}, {int(solution.Max(time_var) / 60)}:{solution.Max(time_var) % 60})"
                f"\nSpend here: {place.estimatedTime}min\n"
                "->\n"
            )
            plan_output += f"Time of the route: {solution.Min(time_var)}min = {total_time / 60}h\n"
            print(plan_output)
            total_time += solution.Min(time_var)
        print(f"Total time of all routes: {total_time}min = {total_time / 60}h")

    def solver_route(self):
        """Solve the VRP with time windows."""
        manager = pywrapcp.RoutingIndexManager(
            len(self.matrix), self.num_routes, self.depot_idx
        )
        routing = pywrapcp.RoutingModel(manager)

        def time_callback(from_index, to_index):
            """Returns the travel time between the two nodes."""
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            time_spend = 0 if from_node == 0 else self.places.get_by_index(from_node - 1).estimatedTime
            return self.matrix[from_node][to_node] + time_spend

        transit_callback_index = routing.RegisterTransitCallback(time_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
        time = "Time"
        routing.AddDimension(
            transit_callback_index,
            30,  
            self.max_time+1,  
            False,  
            time,
        )
        time_dimension = routing.GetDimensionOrDie(time)
        
        for location_idx, time_window in enumerate(self.time_windows):
            if location_idx == self.depot_idx:
                continue
            index = manager.NodeToIndex(location_idx)
            time_dimension.CumulVar(index).SetRange(time_window[0], time_window[1])
        depot_idx = self.depot_idx
        for vehicle_id in range(self.num_routes):
            index = routing.Start(vehicle_id)
            time_dimension.CumulVar(index).SetRange(
                self.time_windows[depot_idx][0], self.time_windows[depot_idx][1]
            )
        for i in range(self.num_routes):
            routing.AddVariableMinimizedByFinalizer(
                time_dimension.CumulVar(routing.Start(i))
            )
            routing.AddVariableMinimizedByFinalizer(time_dimension.CumulVar(routing.End(i)))

        penalty = 1000  
        for node in range(1, len(self.matrix)):
            place = self.places.get_by_index(node - 1)
            place_penalty = penalty*penalty if place.must_see else int(place.ratings.cumulative_rating * penalty)
            routing.AddDisjunction([manager.NodeToIndex(node)], place_penalty)

        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_MOST_CONSTRAINED_ARC
        )
        solution = routing.SolveWithParameters(search_parameters)
        if solution:
            self.print_solution(manager, routing, solution)
            return manager, routing, solution
        else:
            raise ValueError("No solution found")

    def _routes_from_solution(self, manager, routing, solution) -> tuple[Places, list[tuple[int, str]]]:
        """Function that returns the routes from the solution.
        :param manager: manager
        :param routing: routing
        :param solution: solution
        :return: routes"""
        day = []
        transportations = []
        index = routing.Start(0)
        last_node_index = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            if node_index != 0:
                day.append(self.places.get_by_index(node_index - 1))
            if node_index != 0 and last_node_index != 0:
                transportations.append((self.matrix[last_node_index][node_index], self.transport_modes[last_node_index][node_index]))
            last_node_index = node_index
            index = solution.Value(routing.NextVar(index))
        return Places(day), transportations

    def get_routes(self) -> tuple[Places, list[tuple[int, str]]]:
        manager, routing, solution = self.solver_route()
        return self._routes_from_solution(manager, routing, solution)

    def split_for_days(self) -> list[Places]:
        """Function that splits the places for a given number of days.
        :param days: number of days
        :return: list of places for each day"""

        
        manager = pywrapcp.RoutingIndexManager(
            len(self.matrix), self.num_routes, self.depot_idx
        )

        
        routing = pywrapcp.RoutingModel(manager)

        
        def distance_callback(from_index, to_index):
            """Returns the distance between the two nodes."""
            
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return self.matrix[from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)

        
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        
        dimension_name = "Distance"
        routing.AddDimension(
            transit_callback_index,
            0,  
            999*999,
            True,  
            dimension_name,
        )
        distance_dimension = routing.GetDimensionOrDie(dimension_name)
        distance_dimension.SetGlobalSpanCostCoefficient(100)

        
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_MOST_CONSTRAINED_ARC
        )

        
        solution = routing.SolveWithParameters(search_parameters)

        return self._routes_from_solution(manager, routing, solution)
