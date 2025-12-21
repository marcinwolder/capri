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
  deletingTripId?: string;

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

  deleteTrip(trip: TripOverview): void {
    this.deletingTripId = trip.trip_id;
    this.tripHistoryService.deleteTrip(trip.trip_id).subscribe(success => {
      this.deletingTripId = undefined;
      if (!success) {
        this.error = 'Unable to remove trip.';
        return;
      }
      if (this.trips) {
        this.trips = this.trips.filter(item => item.trip_id !== trip.trip_id);
      }
    });
  }

  getTripDatesLabel(trip: TripOverview): string | null {
    if (!trip.dates || trip.dates.length === 0) {
      return null;
    }
    const dates = trip.dates.map(date => new Date(date));
    const start = this.formatDate(dates[0]);
    if (trip.days_len <= 1 || dates.length < 2) {
      return start;
    }
    const end = this.formatDate(dates[1]);
    return `${start} - ${end}`;
  }

  private formatDate(date: Date): string {
    if (Number.isNaN(date.getTime())) {
      return '';
    }
    return date.toLocaleDateString();
  }
}
