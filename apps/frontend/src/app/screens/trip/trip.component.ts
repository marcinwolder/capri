import {Component, OnInit} from '@angular/core';
import { Place } from '../../data-model/place';
import {RecommendationService} from "../../services/recommendation.service";
import {TripHistoryService} from "../../services/trip-history.service";
import weatherDescriptions from "../../constants/weather_descriptions.json";
import {environment} from "../../../environments/environment";
import {RestaurantsService} from "../../services/restaurants.service";
import {getCategoryName} from "../../helpers/getCategoryName";
import {categories} from "../../constants/categories";
import {categories_restaurant} from "../../constants/categories_restaurant";
import {ServiceStatusService} from "../../services/service-status.service";
import {combineLatest, map, Observable} from "rxjs";


interface AttractionField extends Place {
  visible: boolean;
}

interface LoadingChecklistStep {
  key: string;
  label: string;
  detail?: string;
  minMs: number;
  maxMs: number;
}

@Component({
  selector: 'app-trip',
  templateUrl: './trip.component.html',
  styleUrls: ['./trip.component.css']
})
export class TripComponent implements OnInit{

  backendOffline$!: Observable<boolean>;
  llamaOffline$!: Observable<boolean>;
  serviceStatus$!: Observable<{ backendOffline: boolean; llamaOffline: boolean }>;
  checkingServices$!: Observable<boolean>;
  backendHost = environment.backendHost.replace(/\/$/, '');
  llamaHost = environment.llamaHost.replace(/\/$/, '');

  constructor(private recommendationService: RecommendationService, private tripHistoryService: TripHistoryService,
              private restaurantsService: RestaurantsService, private serviceStatus: ServiceStatusService) {
    this.backendOffline$ = this.serviceStatus.backendOffline$;
    this.llamaOffline$ = this.serviceStatus.llamaOffline$;
    this.checkingServices$ = this.serviceStatus.checking$;
    this.serviceStatus$ = combineLatest([this.backendOffline$, this.llamaOffline$]).pipe(
      map(([backendOffline, llamaOffline]) => ({backendOffline, llamaOffline}))
    );
  }

  ngOnInit(): void {
    this.resetLoadingState();
    this.loadingMode = this.recommendationService.getTripLoadMode();
    this.waitForReadyIndex = this.loadingMode === 'generation' ? 2 : 0;
    this.recommendationService.getRecommendedTrip().subscribe({
      next: (trip) => {
        this.attractions = trip.days.map(day => day.places.map(attraction => {
            return {...attraction, visible: false}
        }));
        this.weatherForecasts = trip.days.map(day => day.weather);
        this.summary = trip.summary;
        this.tripReady = true;
        this.finishLoading();
        this.tripId = trip.id;
        this.city_id = trip.city_id;
      },
      error: (error: Error) => {
        this.error = error.message;
        this.cancelChecklist = true;
      }
    });
  }

  tripId?: string;
  isLoaded = false;
  error?: string;
  // checklist & loading state
  tripReady = false;
  checklistCompleted = false;
  cancelChecklist = false;
  loadingMode: 'generation' | 'history' | 'local' = 'generation';
  waitForReadyIndex = 2;
  simpleLoadingSteps: LoadingChecklistStep[] = [
    {
      key: 'load-trip',
      label: 'Loading trip data',
      detail: 'Fetching your saved itinerary.',
      minMs: 200,
      maxMs: 500
    }
  ];

  attractions: AttractionField[][] = [];
  summary: string = '';
  currentDayIndex = 0;
  showMap = false;
  weatherForecasts: number[] = [];
  city_id?: string;

  getImageUrl(place: Place): string {
    const backendHost = environment.backendHost.endsWith('/')
      ? environment.backendHost.slice(0, -1)
      : environment.backendHost;
    return `${backendHost}/api/places/photos/${place.image.name}?maxHeightPx=400&maxWidthPx=400`;
  }

  getWeatherIcon(weather: number): string {
    if(!weather) return '';
    // @ts-ignore
    return weatherDescriptions[weather.toString()]['day']['image'];
  }

  getWeatherDescription(weather: number): string {
    if(!weather) return '';
    // @ts-ignore
    return weatherDescriptions[weather.toString()]['day']['description'];
  }


  toggleAttractionDetails(day_index:number, att_index: number): void {
    this.attractions[day_index][att_index].visible = !this.attractions[day_index][att_index].visible;
  }

  scrollToSection(sectionId: string): void {
    const section = document.getElementById(sectionId);
    section?.scrollIntoView({ behavior: 'smooth' });
  }

  toggleMap(): void {
    this.showMap = !this.showMap;
  }

  rateAttraction(day_index: number, att_index: number, rating: number): void {
    this.tripHistoryService.rateTripAttraction(this.tripId!, day_index, att_index, rating).subscribe();
  }

  searchRestaurants(place: Place) {
    this.restaurantsService.getRestaurants(this.city_id!, place).subscribe({
      next: (data) => {
        console.log(data);
        place.restaurants = data as Place[];
      },
      error: (error) => {
        console.log(error);
      }
    });
  }

  onChecklistCompleted(): void {
    this.checklistCompleted = true;
    this.finishLoading();
  }

  private finishLoading(): void {
    if (this.tripReady && this.checklistCompleted) {
      this.isLoaded = true;
    }
  }

  private resetLoadingState(): void {
    this.isLoaded = false;
    this.tripReady = false;
    this.checklistCompleted = false;
    this.cancelChecklist = false;
  }

  retryServices(): void {
    this.serviceStatus.retryNow();
  }

  protected readonly Number = Number;
  protected readonly String = String;
  protected readonly getCategoryName = getCategoryName;
  protected readonly categories = categories;
  protected readonly categories_restaurant = categories_restaurant;
}
