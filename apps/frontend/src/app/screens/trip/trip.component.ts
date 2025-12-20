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


interface AttractionField extends Place {
  visible: boolean;
}

@Component({
  selector: 'app-trip',
  templateUrl: './trip.component.html',
  styleUrls: ['./trip.component.css']
})
export class TripComponent implements OnInit{

  constructor(private recommendationService: RecommendationService, private tripHistoryService: TripHistoryService,
              private restaurantsService: RestaurantsService) {}

  ngOnInit(): void {
    this.resetLoadingState();
    this.recommendationService.getRecommendedTrip().subscribe({
      next: (trip) => {
        this.attractions = trip.days.map(day => day.places.map(attraction => {
            return {...attraction, visible: false}
        }));
        this.weatherForecasts = trip.days.map(day => day.weather);
        this.summary = trip.summary;
        this.tripLoaded = true;
        this.accelerateChecklist = true;
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
  private tripLoaded = false;
  checklistCompleted = false;
  accelerateChecklist = false;
  cancelChecklist = false;

  attractions: AttractionField[][] = [];
  summary: string = '';
  currentDayIndex = 0;
  showMap = false;
  displayAllSummary = false;
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
    if (this.tripLoaded && this.checklistCompleted) {
      this.isLoaded = true;
    }
  }

  private resetLoadingState(): void {
    this.isLoaded = false;
    this.tripLoaded = false;
    this.checklistCompleted = false;
    this.accelerateChecklist = false;
    this.cancelChecklist = false;
  }

  protected readonly Number = Number;
  protected readonly String = String;
  protected readonly getCategoryName = getCategoryName;
  protected readonly categories = categories;
  protected readonly categories_restaurant = categories_restaurant;
}
