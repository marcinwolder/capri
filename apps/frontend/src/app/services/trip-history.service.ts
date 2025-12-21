import {Injectable} from '@angular/core';
import {catchError, map, Observable, of} from "rxjs";
import {HttpClient} from "@angular/common/http";
import {environment} from "../../environments/environment";
import {Trip} from "../data-model/trip";
import {TripOverview} from "../data-model/tripOverview";

interface TripHistoryResponse {
  data: Trip[] | Trip;
  success: boolean;
}

@Injectable({
  providedIn: 'root'
})
export class TripHistoryService {

  constructor(private http: HttpClient) {}

  getTripHistoryOverview() {
    return this.http.get<TripHistoryResponse>(environment.backendHost + 'api/trip-history').pipe(
      map(response => {
        if (!response.success) {
          throw new Error('Failed to fetch trip history');
        }
        const trips = Array.isArray(response.data) ? response.data as Trip[] : [response.data as Trip];
        return trips.map(trip => ({
          trip_id: trip.id,
          city_name: trip.city_name || '',
          days_len: trip.days?.length || 0,
          dates: (trip as any).dates || []
        } as TripOverview));
      }),
      catchError(error => {
        console.error('Error fetching trip history:', error);
        return of(null);
      })
    );
  }

  public getTrip(tripId: string) {
    return this.http.get<TripHistoryResponse>(environment.backendHost + 'api/trip-history/' + tripId).pipe(
      map(response => {
        if (!response.success) {
          throw new Error('Failed to fetch trip history');
        }
        return response.data as Trip;
      }),
      catchError(error => {
        console.error('Error fetching trip:', error);
        return of(null);
      })
    );
  }

  rateTripAttraction(tripId: string, day_index: number, attraction_index: number, rating: number): Observable<boolean> {
    const body = {
      day_index,
      place_index: attraction_index,
      rating
    };
    return this.http.post<TripHistoryResponse>(`${environment.backendHost}api/trip-history/${tripId}/rating`, body).pipe(
      map(response => response.success),
      catchError(error => {
        console.error('Error rating attraction:', error);
        return of(false);
      })
    );
  }

  deleteTrip(tripId: string): Observable<boolean> {
    return this.http.delete<TripHistoryResponse>(`${environment.backendHost}api/trip-history/${tripId}`).pipe(
      map(response => response.success),
      catchError(error => {
        console.error('Error deleting trip:', error);
        return of(false);
      })
    );
  }



}
