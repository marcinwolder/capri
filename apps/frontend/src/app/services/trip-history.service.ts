import {Injectable} from '@angular/core';
import {catchError, map, Observable, of} from "rxjs";
import {HttpClient} from "@angular/common/http";
import {environment} from "../../environments/environment";
import {Trip, TripSurvey} from "../data-model/trip";
import {TripOverview} from "../data-model/tripOverview";

interface TripHistoryResponse {
  data?: Trip;
  success: boolean;
}

interface TripHistoryOverviewResponse {
  data: TripOverview[];
  success: boolean;
}

interface TripSurveyResponse {
  success: boolean;
  data?: TripSurvey;
}

interface BatchDeleteResponse {
  success: boolean;
  deleted_ids: string[];
  missing_ids?: string[];
  errors?: string[];
}

@Injectable({
  providedIn: 'root'
})
export class TripHistoryService {

  constructor(private http: HttpClient) {}

  getTripHistoryOverview() {
    return this.http.get<TripHistoryOverviewResponse>(environment.backendHost + 'api/trip-history/overview').pipe(
      map(response => {
        if (!response.success) {
          throw new Error('Failed to fetch trip history');
        }
        return response.data as TripOverview[];
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
        if (!response.success || !response.data) {
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

  submitTripSurvey(tripId: string, payload: {
    sus_answers: number[];
    csat: number;
    nps: number;
    subjective_answers: number[];
  }): Observable<TripSurvey | null> {
    return this.http.post<TripSurveyResponse>(`${environment.backendHost}api/trip-history/${tripId}/survey`, payload).pipe(
      map(response => response.success ? (response.data || null) : null),
      catchError(error => {
        console.error('Error submitting trip survey:', error);
        return of(null);
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

  deleteTrips(tripIds: string[]): Observable<BatchDeleteResponse> {
    return this.http.post<BatchDeleteResponse>(`${environment.backendHost}api/trip-history/batch-delete`, {
      trip_ids: tripIds
    }).pipe(
      catchError(error => {
        console.error('Error deleting trips:', error);
        return of({
          success: false,
          deleted_ids: [],
          errors: ['Request failed.']
        });
      })
    );
  }



}
