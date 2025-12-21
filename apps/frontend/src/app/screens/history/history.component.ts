import {Component, OnInit} from '@angular/core';
import {Router} from '@angular/router';
import {TripHistoryService} from '../../services/trip-history.service';
import {RecommendationService} from '../../services/recommendation.service';
import {TripOverview} from '../../data-model/tripOverview';

@Component({
  selector: 'app-history',
  templateUrl: './history.component.html',
  styleUrls: ['./history.component.css']
})
export class HistoryComponent implements OnInit {
  trips: TripOverview[] | null = null;
  loading = true;
  error?: string;

  constructor(private tripHistoryService: TripHistoryService,
              private recommendationService: RecommendationService,
              private router: Router) {}

  ngOnInit(): void {
    this.tripHistoryService.getTripHistoryOverview().subscribe(trips => {
      this.trips = trips;
      this.loading = false;
      if (trips === null) {
        this.error = 'Unable to load trip history.';
      }
    });
  }

  goToTrip(trip: TripOverview): void {
    this.recommendationService.getTripFromHistory(trip.trip_id);
    this.router.navigate(['/trip']);
  }
}
