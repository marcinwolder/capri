
import {Injectable} from '@angular/core';
import {catchError, firstValueFrom, map, Observable, of, switchMap, take, throwError} from "rxjs";
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {environment} from "../../environments/environment";
import {ChatMessage} from "../data-model/chatMessage";
import {Preferences} from "../data-model/preferences";
import {DestinationService} from "./destination.service";
import {LocalStorageService} from "./local-storage.service";
import {Trip} from "../data-model/trip";
import {AuthService} from "./auth.service";
import {mock1} from "./mock1";
import {TripHistoryService} from "./trip-history.service";

const httpOptions = {
  headers: new HttpHeaders({'Content-Type': 'application/json'})
};

type PreferenceType = 'messages' | 'note' | 'preferences';

interface RecommendationResponse {
  received_data: Trip;
  status: string;
}

@Injectable({
  providedIn: 'root'
})
export class RecommendationService {

  private HOST = environment.backendHost;
  private preference: {
    messages?: ChatMessage[];
    note?: string;
    preferences?: Preferences;
  } = {};

  private trip?: Trip;
  private history_trip_id?: string;
  private fetchNewTrip = false;

  constructor(private http: HttpClient, private destinationService: DestinationService,
              private localStorageService: LocalStorageService, private authService: AuthService,
              private tripHistoryService: TripHistoryService) {
  }

  private setPreference(key: PreferenceType, value: any): void {
    this.preference = {};
    this.preference[key] = value;
    this.savePreferencesToLocalStorage();
    this.fetchNewTrip = true;
  }

  public setMessages(messages: ChatMessage[]): void {
    this.setPreference('messages', messages);
  }

  public setNote(note: string): void {
    this.setPreference('note', note);
  }

  public setPreferences(preferences: Preferences): void {
    this.setPreference('preferences', preferences);
  }

  public getTripFromHistory(trip_id: string): void {
    this.history_trip_id = trip_id;
    this.fetchNewTrip = false;
  }

  private savePreferencesToLocalStorage(): void {
    this.localStorageService.set('recommendation-preferences', JSON.stringify(this.preference));
  }

  private loadPreferencesFromLocalStorage(): void {
    const data = this.localStorageService.get('recommendation-preferences');
    if (data) {
      this.preference = JSON.parse(data);
    }
  }

  private setTrip(trip: Trip): void {
    this.trip = trip;
    this.localStorageService.set('trip', JSON.stringify(this.trip));
  }

  private loadTripFromLocalStorage(): void {
    const data = this.localStorageService.get('trip');
    if (data) {
      this.trip = JSON.parse(data);
    }
  }

  private dateToString(date: Date): string {
    return date.getFullYear() + '-' +
      ('0' + (date.getMonth() + 1)).slice(-2) + '-' +
      ('0' + date.getDate()).slice(-2);
  };


  private postRecommendationRequest(endpoint: string, data: ChatMessage[] | string | Preferences):
    Observable<RecommendationResponse> {

    console.log(this.destinationService.getDestination().dates[0])
    
    
    return this.authService.currentUserValue.pipe(
      take(1),
      switchMap(user => {
        if (!user) {
          return throwError(() => new Error('User not logged in'));
        }
        const payload: any = {
          ...this.destinationService.getDestination(),
          preferences: data,
          user_id: user.uid
        };
        console.log(payload.dates)
        payload.dates = payload.dates.map((date: Date) => this.dateToString(date));
        console.log(payload.dates)
        console.log(this.HOST + endpoint, payload);
        return this.http.post<RecommendationResponse>(this.HOST + 'api/recommendation/' + endpoint, payload,
          httpOptions);
      }),
      catchError(error => throwError(() => new Error(`An error occurred while posting request: ${error.message || error}`)))
    );
  }


  getRecommendedTrip(): Observable<Trip> {
    if (!this.fetchNewTrip && this.history_trip_id) {
      return this.tripHistoryService.getTrip(this.history_trip_id).pipe(
        map(trip => {
          if (!trip) {
            throw new Error('Failed to get trip from history');
          }
          this.setTrip(trip);
          return trip;
        }),
        catchError(error => throwError(() =>
          new Error(`An error occurred while getting trip from history: ${error.message || error}`))
        ));
    } else if (!this.fetchNewTrip && !this.history_trip_id) {
      this.loadTripFromLocalStorage();
      if (!this.trip) {
        return throwError(() => new Error('No trip data provided'));
      }
      return of(this.trip);
    }

    if (!this.preference.messages && !this.preference.note && !this.preference.preferences) {
      this.loadPreferencesFromLocalStorage();
      if (!this.preference.messages && !this.preference.note && !this.preference.preferences) {
        return throwError(() => new Error('No data provided'));
      }
    }

    const requestType: PreferenceType = this.preference.messages ? 'messages' :
      this.preference.note ? 'note' : 'preferences';
    const requestData = this.preference[requestType];

    return this.postRecommendationRequest(requestType, requestData!).pipe(
      map(response => {
        if (response['status'] !== 'success') {
          throw new Error('Failed to get recommendations');
        }
        this.setTrip(response.received_data);
        return response.received_data;
      }),
      catchError(error => throwError(() => new Error(`An error occurred while getting recommended trip: ${error.message || error}`)))
    );
  }


}







































































































































































































































































































































































































































































































































































































































































































































































































































