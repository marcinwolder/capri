import {Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {PreferencesService} from "./preferences.service";
import {Place} from "../data-model/place";
import {environment} from "../../environments/environment";
import {catchError, map, Observable, switchMap} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class RestaurantsService {

  constructor(private http: HttpClient, private preferencesService: PreferencesService) {
  }

  getRestaurants(city_id: string, place: Place): Observable<Place[]> {
    const preferences = this.preferencesService.getLocalPreferences();
    return this.http.get(environment.backendHost + 'api/restaurants-nearby', {
      params: {
        categories: JSON.stringify(preferences.categories_restaurant),
        vegan: preferences.needs.includes('vegan') ? 1 : 0,
        alcohol: preferences.needs.includes('alcohol') ? 1 : 0,
        lat: place.latitude.toString(),
        lon: place.longitude.toString(),
        city_id: city_id
      }
    }).pipe(
      map((data: any) => {
        return data['data'] as Place[];
      }),
      catchError((error) => {
        console.error('Error getting restaurants', error);
        return [];
      }));
  }
}
