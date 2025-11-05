import {Injectable} from '@angular/core';
import {AuthService} from "./auth.service";
import {catchError, from, map, Observable, of, pipe, switchMap} from "rxjs";
import {HttpClient} from "@angular/common/http";
import {environment} from "../../environments/environment";
import {Trip} from "../data-model/trip";
import {TripOverview} from "../data-model/tripOverview";
import {data} from "autoprefixer";

interface TripHistoryResponse {
  data: Trip[] | Trip;
  success: boolean;
}

@Injectable({
  providedIn: 'root'
})
export class TripHistoryService {

  constructor(private http: HttpClient, private authService: AuthService) {
  }

  getTripHistoryOverview() {
    return this.authService.getCurrentUserDocRef().pipe(
      switchMap(userRef => {
        if (!userRef) {
          return of(null);
        }
        return from(userRef.collection('trip_history').get()).pipe(
          map(tripsSnapshot => {
            const trips: TripOverview[] = [];
            tripsSnapshot.forEach(doc => {
              const data = doc.data()
              trips.push({
                trip_id: doc.id,
                city_name: data['city_name'],
                days_len: data['days_len'],
                dates: data['dates']
              } as TripOverview);
            });
            return trips;
          }),
          catchError(error => {
            console.error('Error fetching trip history:', error);
            return of(null);
          })
        );
      })
    );
  }

  private getHttpOptions = (token: string) => {
    return {headers: {'Authorization': 'Bearer ' + token}}
  };

  public getTrip(tripId: string) {
    return this.authService.currentUserValue.pipe(
      switchMap(user => {
        if (!user) {
          return of(null);
        }
        return from(user.getIdToken()).pipe(
          switchMap(token => {
            return this.http.get<TripHistoryResponse>(environment.backendHost + 'api/trip-history/' + tripId,
              this.getHttpOptions(token));
          }),
          switchMap(response => {
            if (!response.success) {
              throw new Error('Failed to fetch trip history');
            }
            return of(response.data as Trip);
          }),
          catchError(error => {
            console.error('Error fetching trip:', error);
            return of(null);
          })
        );
      })
    )
  }

  rateTripAttraction(tripId: string, day_index: number, attraction_index: number, rating: number): Observable<boolean> {
    return this.authService.getCurrentUserDocRef().pipe(
      switchMap(userRef => {
        if (!userRef) {
          throw new Error("User reference is not available");
        }
        const dayRef = userRef.collection('trip_history')
          .doc(tripId)
          .collection('days')
          .doc(day_index.toString());
        const placeRef = dayRef.collection('places')
          .doc(attraction_index.toString());

        return from(placeRef.update({ user_rating: rating })).pipe(
          map(() => true)
        );
      }),
      catchError(error => {
        console.error('Error rating attraction:', error);
        return of(false);
      })
    );
  }



}
