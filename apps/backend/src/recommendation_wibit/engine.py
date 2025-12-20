from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from math import cos, pi, sqrt
from typing import Dict, List, Sequence, Tuple

from src.api_calls.llama import Llama
from src.data_model.place.place import Place
from src.data_model.place.place_visitor import PlaceVisitor
from src.data_model.places.places import Places
from src.data_model.user.user_preferences import UserPreferences

# Default day window for sightseeing
DEFAULT_START = time(9, 0)
DEFAULT_END = time(17, 0)
DEFAULT_VISIT_MIN = 90
PROXIMITY_RADIUS_M = 500
SHORT_DIST = 500
WALKING_SPEED = 0.5  # m/s
DRIVING_SPEED = 3.7  # m/s


@dataclass
class PointOfInterest:
    xid: str
    name: str
    lat: float
    lon: float
    kinds: List[str]
    estimated_minutes: int


@dataclass
class Day:
    date_str: str
    start: datetime
    end: datetime
    weekday: int


@dataclass
class Event:
    start: time
    end: time
    poi: PointOfInterest
    travel_seconds: int = 0
    travel_mode: str = 'walk'


@dataclass
class Trajectory:
    events: List[Event]

    def get_pois(self) -> List[PointOfInterest]:
        return [event.poi for event in self.events]


def dist(poi1: PointOfInterest, poi2: PointOfInterest) -> float:
    """Haversine approximation in meters."""
    dlat = (poi1.lat - poi2.lat) * pi / 180
    dlon = (poi1.lon - poi2.lon) * pi / 180
    mlat = (poi1.lat + poi2.lat) / 2 * pi / 180
    earth_radius = 6371009
    return earth_radius * sqrt(pow(dlat, 2) + pow(cos(mlat) * dlon, 2))


def estimated_time(distance_meters: float) -> float:
    if distance_meters < SHORT_DIST:
        return distance_meters / WALKING_SPEED
    return distance_meters / DRIVING_SPEED


def round_time(dt: datetime) -> datetime:
    return datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute - (dt.minute % 5), 0, 0)


class VisitingTimeProvider:
    def __init__(self, default_minutes: int = DEFAULT_VISIT_MIN):
        self.default_minutes = default_minutes

    def get_visiting_time(self, poi: PointOfInterest) -> timedelta:
        return timedelta(minutes=max(poi.estimated_minutes, 5))


class CategoryConstraint:
    def __init__(self, codes: Sequence[str], weight: int = 20):
        self.codes = list(codes)
        self.weight = weight

    def evaluate(self, poi: PointOfInterest) -> float:
        if not self.codes:
            return 0
        overlap = len(set(poi.kinds) & set(self.codes))
        if overlap == 0:
            return 0
        return overlap / len(self.codes)

    def get_weight(self) -> int:
        return self.weight

    def get_decay(self) -> int:
        return 4


class ProximityConstraint:
    def __init__(self, best_pois_nr: int = 3, radius: int = PROXIMITY_RADIUS_M, rate: float = 0.8):
        self.best_pois_nr = best_pois_nr
        self.radius = radius
        self.rate = rate
        self.weight = 1
        self._modifications = [500, 1000, 250, 2000]

    def evaluate(self, pois_scores: List[Tuple[PointOfInterest, float]]) -> List[Tuple[PointOfInterest, float]]:
        for i in range(min(self.best_pois_nr, len(pois_scores))):
            poi, score = pois_scores[i]
            for j in range(i + 1, len(pois_scores)):
                poi_other, score_other = pois_scores[j]
                if dist(poi, poi_other) < self.radius:
                    pois_scores[j] = (poi_other, (1 - self.rate) * score_other + score * self.rate)
        return pois_scores


class User:
    def __init__(self):
        self.preferences: List[Tuple[CategoryConstraint, int]] = []
        self.total_weights: int = 0
        self.general_constraints: List[ProximityConstraint] = []

    def add_constraint(self, constraint: CategoryConstraint):
        self.preferences.append((constraint, constraint.get_weight()))
        self.total_weights += constraint.get_weight()

    def add_general_constraint(self, constraint: ProximityConstraint):
        self.general_constraints.append(constraint)

    def evaluate(self, poi: PointOfInterest) -> float:
        if self.total_weights == 0:
            return 0.1
        res = 0.0
        for constraint, weight in self.preferences:
            res += constraint.evaluate(poi) * weight
        res /= self.total_weights
        return res + 0.1

    def decay_weights(self):
        new_prefs: List[Tuple[CategoryConstraint, int]] = []
        for constraint, weight in self.preferences:
            decay = constraint.get_decay()
            new_weight = max(weight - decay, 0)
            if new_weight > 0:
                new_prefs.append((constraint, new_weight))
        self.preferences = new_prefs
        self.total_weights = sum(weight for _, weight in self.preferences)

    def general_evaluation(self, pois_score: List[Tuple[PointOfInterest, float]]) -> List[Tuple[PointOfInterest, float]]:
        res = pois_score
        for constraint in self.general_constraints:
            res = constraint.evaluate(res)
        return res


class Evaluator:
    def __init__(self, user: User, visiting_time_provider: VisitingTimeProvider):
        self.user = user
        self.visiting_time_provider = visiting_time_provider
        self.evaluated_places: List[Tuple[PointOfInterest, float]] = []

    def evaluate(self, pois: Sequence[PointOfInterest]):
        self.evaluated_places = [(poi, self.user.evaluate(poi)) for poi in pois]
        self.evaluated_places.sort(key=lambda x: x[1], reverse=True)
        self.user.decay_weights()

    def extract_best(self, day: Day, already_taken: set[str]) -> List[Tuple[PointOfInterest, float]]:
        poi_score: List[Tuple[PointOfInterest, float]] = self.user.general_evaluation(list(self.evaluated_places))
        res: List[Tuple[PointOfInterest, float]] = []
        i = 0
        curr_time = day.start
        while i < len(poi_score) and curr_time < day.end:
            poi = poi_score[i][0]
            if poi.xid not in already_taken:
                curr_time += self.visiting_time_provider.get_visiting_time(poi)
                res.append((poi, poi_score[i][1]))
            i += 1
        return res


def get_mst(graph: List[List[float]]) -> List[List[int]]:
    dl = len(graph)
    mst = [[0 for _ in range(dl)] for _ in range(dl)]
    visited = [False for _ in range(dl)]
    visited[0] = True
    vertices_left = dl - 1
    queue: List[Tuple[float, Tuple[int, int]]] = []
    for u in range(dl):
        if graph[0][u] > 0:
            queue.append((graph[0][u], (0, u)))
    queue.sort(key=lambda x: x[0])

    while vertices_left > 0 and queue:
        w, (v, u) = queue.pop(0)
        if not visited[u]:
            visited[u] = True
            vertices_left -= 1
            mst[v][u] = 1
            mst[u][v] = 1
            for t in range(dl):
                if t != u and not visited[t]:
                    queue.append((graph[u][t], (u, t)))
            queue.sort(key=lambda x: x[0])
    return mst


def estimated_shp_from_mst(mst: List[List[int]]) -> List[int]:
    dl = len(mst)
    path = [0]
    deg = [2 * sum(mst[i]) for i in range(dl)]
    is_bridge = [[False for _ in range(dl)] for _ in range(dl)]

    def dfs(v: int):
        for u in range(dl):
            if mst[v][u] == 1 and deg[u] > 0 and not is_bridge[u][v]:
                path.append(u)
                deg[u] -= 1
                deg[v] -= 1
                is_bridge[u][v] = True
                is_bridge[v][u] = True
                dfs(u)
        for u in range(dl):
            if mst[v][u] == 1 and deg[u] > 0:
                deg[u] -= 1
                deg[v] -= 1
                dfs(u)

    dfs(0)
    return path


def opt_2(path: List[int], graph: List[List[float]]) -> List[int]:
    dl = len(path)
    improvement = True
    n = 0
    while improvement and n < 10:
        improvement = False
        for i in range(dl - 3):
            for j in range(i + 3, dl):
                v = path[i]
                v_next = path[i + 1]
                u = path[j]
                u_prev = path[j - 1]
                d = -graph[v][v_next] - graph[u_prev][u] + graph[v][u_prev] + graph[v_next][u]
                if d < -10:
                    improvement = True
                    new_path = [path[k] for k in range(0, i + 1)]
                    for k in range(j - 1, i, -1):
                        new_path.append(path[k])
                    for m in range(j, len(path)):
                        new_path.append(path[m])
                    path = new_path
        n += 1
    return path


def opt_1(path: List[int], graph: List[List[float]]) -> List[int]:
    dl = len(path)
    max_dist = 0
    new_start = 0
    for i in range(dl):
        if graph[path[i]][path[(i + 1) % dl]] > max_dist:
            max_dist = graph[path[i]][path[(i + 1) % dl]]
            new_start = (i + 1) % dl

    new_path: List[int] = []
    for i in range(new_start, dl):
        new_path.append(path[i])
    for i in range(new_start):
        new_path.append(path[i])
    return new_path


def build_trajectory(day: Day, pois_score: List[Tuple[PointOfInterest, float]], time_provider: VisitingTimeProvider) -> Trajectory:
    if not pois_score:
        return Trajectory(events=[])
    graph = [[dist(i, j) for i, _ in pois_score] for j, _ in pois_score]
    mst_graph = get_mst(graph)
    path = estimated_shp_from_mst(mst_graph)
    path2 = opt_2(path, graph)
    better_path = opt_1(path2, graph)

    curr = day.start
    travel_time = timedelta()
    next_visiting = time_provider.get_visiting_time(pois_score[better_path[0]][0])
    events: List[Event] = []

    for n in range(len(path)):
        if curr + travel_time + next_visiting < day.end:
            travel_seconds = int(travel_time.total_seconds()) if n > 0 else 0
            travel_mode = 'FOOT' if (n == 0 or graph[path[n - 1]][path[n]] < SHORT_DIST) else 'CAR'
            events.append(
                Event(
                    start=round_time(curr + travel_time).time(),
                    end=round_time(curr + travel_time + next_visiting).time(),
                    poi=pois_score[better_path[n]][0],
                    travel_seconds=travel_seconds,
                    travel_mode=travel_mode,
                )
            )
            if n + 1 >= len(path):
                break
            curr += travel_time + next_visiting
            curr = round_time(curr)
            edge_seconds = estimated_time(graph[path[n]][path[n + 1]])
            travel_time = timedelta(seconds=edge_seconds)
            next_visiting = time_provider.get_visiting_time(pois_score[better_path[n + 1]][0])
    return Trajectory(events=events)


def _to_poi(place: Place) -> PointOfInterest | None:
    if place.location.latitude is None or place.location.longitude is None:
        return None
    kinds: List[str] = []
    kinds.extend(place.types or [])
    kinds.extend(place.subcategories or [])
    if place.primaryType:
        kinds.append(place.primaryType)
    return PointOfInterest(
        xid=str(place.placeInfo.id or place.placeInfo.displayName),
        name=place.placeInfo.displayName or place.placeInfo.name or '',
        lat=float(place.location.latitude),
        lon=float(place.location.longitude),
        kinds=[k for k in kinds if k],
        estimated_minutes=int(place.estimatedTime) if place.estimatedTime else DEFAULT_VISIT_MIN,
    )


def _days_from_dates(dates: Tuple[date, date]) -> List[Day]:
    start_date, end_date = dates
    res: List[Day] = []
    curr = start_date
    while curr <= end_date:
        start_dt = datetime.combine(curr, DEFAULT_START)
        end_dt = datetime.combine(curr, DEFAULT_END)
        res.append(Day(date_str=curr.isoformat(), start=start_dt, end=end_dt, weekday=curr.weekday()))
        curr = curr + timedelta(days=1)
    return res


def _preferred_categories(preferences: UserPreferences) -> List[str]:
    codes: List[str] = list(preferences.categories)
    for sub_list in preferences.subcategories.values():
        codes.extend(sub_list)
    return [c for c in codes if c]


def recommend_itinerary(places: Places, preferences: UserPreferences, dates: Tuple[date, date], city_name: str | None = None) -> dict:
    """Build itinerary using the WiBIT-like heuristic."""
    poi_candidates: List[Tuple[PointOfInterest, Place]] = []
    for place in places.get_list():
        poi = _to_poi(place)
        if poi is None:
            continue
        poi_candidates.append((poi, place))
    if not poi_candidates:
        return {
            'days': [],
            'summary': 'No POIs found for the selected city.',
            'dates': [dates[0].isoformat(), dates[1].isoformat()],
        }

    user = User()
    user.add_constraint(CategoryConstraint(_preferred_categories(preferences)))
    user.add_general_constraint(ProximityConstraint())

    visiting_time_provider = VisitingTimeProvider()
    evaluator = Evaluator(user, visiting_time_provider)
    evaluator.evaluate([poi for poi, _ in poi_candidates])

    already_recommended: set[str] = set()
    schedule: List[Trajectory] = []
    days = _days_from_dates(dates)

    for day in days:
        best_candidates = evaluator.extract_best(day, already_recommended)
        trajectory = build_trajectory(day, best_candidates, visiting_time_provider)
        for event in trajectory.events:
            already_recommended.add(event.poi.xid)
        schedule.append(trajectory)

    id_to_place: Dict[str, Place] = {str(poi.xid): place for poi, place in poi_candidates}
    place_visitor = PlaceVisitor()
    summary_trip: List[Places] = []
    out_days = []
    for trajectory in schedule:
        day_places = []
        day_place_objs: List[Place] = []
        for event in trajectory.events:
            place = id_to_place.get(str(event.poi.xid))
            if place is None:
                continue
            transportation = (event.travel_seconds, event.travel_mode) if event.travel_seconds else None
            day_places.append(place_visitor.place_to_itinerary(place, transportation))
            day_place_objs.append(place)
        out_days.append({'places': day_places, 'weather': 0})
        summary_trip.append(Places(day_place_objs))

    summary = ''
    if city_name:
        summary = Llama.get_summary(city=city_name, trip=summary_trip)

    # Persist the selected date range so the frontend can show start/end dates in history.
    return {
        'days': out_days,
        'summary': summary,
        'dates': [dates[0].isoformat(), dates[1].isoformat()],
    }
