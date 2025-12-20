import {Component, OnInit} from '@angular/core';
import {Router} from "@angular/router";
import {AuthService} from "../../services/auth.service";
import {User} from "../../data-model/user";
import {Preferences} from "../../data-model/preferences";
import {PreferencesService} from "../../services/preferences.service";
import {TripHistoryService} from "../../services/trip-history.service";
import {Trip} from "../../data-model/trip";
import {RecommendationService} from "../../services/recommendation.service";
import {TripOverview} from "../../data-model/tripOverview";
import {getCategoryName, getSubCategoryName} from "../../helpers/getCategoryName";
import {categories} from "../../constants/categories";
import {categories_restaurant} from "../../constants/categories_restaurant";

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit{
  constructor(private router: Router, private authService: AuthService, private preferencesService: PreferencesService,
              private tripHistoryService: TripHistoryService, private recommendationService: RecommendationService) {}

  user?: User;
  preferences?: Preferences;
  trips?: TripOverview[] | null;

  ngOnInit() {
    this.authService.getCurrentUserInfo().subscribe(user => {
      if (!user) {
        this.user = undefined;
        this.preferences = undefined;
        this.trips = null;
        this.router.navigate(['/signin']);
        return;
      }

      this.user = user;
      this.loadProfileData();
    });
  }

  private loadProfileData() {
    this.tripHistoryService.getTripHistoryOverview().subscribe(trips => {
      this.trips = trips;
    });

    this.preferencesService.getUserPreferences().subscribe(preferences => {
      this.preferences = preferences;
    });
  }

  goToTrip(trip: TripOverview) {
    this.recommendationService.getTripFromHistory(trip.trip_id)
    this.router.navigate(['/trip']);
  }

  protected readonly getCategoryName = getCategoryName;
  protected readonly categories = categories;
  protected readonly getSubCategoryName = getSubCategoryName;
  protected readonly categories_restaurant = categories_restaurant;
}
