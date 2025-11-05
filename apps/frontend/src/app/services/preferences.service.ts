import {Injectable} from '@angular/core';
import {LocalStorageService} from "./local-storage.service";
import {Categories} from "../data-model/categories";
import {catchError, firstValueFrom, map, Observable, switchMap, throwError} from "rxjs";
import {AngularFirestore} from "@angular/fire/compat/firestore";
import {AuthService} from "./auth.service";
import {Preferences} from "../data-model/preferences";

@Injectable({
  providedIn: 'root'
})
export class PreferencesService {

  constructor(private localStorageService: LocalStorageService, private authService: AuthService,
              private firestore: AngularFirestore) {
    this.getLocalPreferences();
  }

  private preferences: Preferences = new Preferences();

  public save(local: boolean = false){
    this.localStorageService.set("preferences", JSON.stringify(this.preferences));
    if(local) return;
    this.saveUserPreferences(this.preferences).then(r => r)
  }

  setNeeds(needs: string[]) {
    this.preferences.needs = needs;
  }

  setMoney(money: number) {
    this.preferences.money = money;
  }

  setCategories(categories: Categories){
    this.preferences.categories = categories;
  }

  setCategoriesRestaurant(categories_restaurant: string[]){
    this.preferences.categories_restaurant = categories_restaurant;
  }

  private async saveUserPreferences(preferences: Preferences) {
    const user = await firstValueFrom(this.authService.currentUserValue);
    if (!user) {
      throw new Error('User is not authenticated');
    }

    const userRef = this.firestore.collection('users').doc(user.uid);
    const writes: Promise<void>[] = [
      userRef.collection('preferences').doc('money').set({value: preferences.money}),
      userRef.collection('preferences').doc('categories').set(preferences.categories),
      userRef.collection('preferences').doc('needs').set({value: preferences.needs}),
      userRef.collection('preferences').doc('categories_restaurant')
        .set({value: preferences.categories_restaurant})
    ];

    await Promise.all(writes);
  }


  getUserPreferences(): Observable<Preferences | undefined> {
    return this.authService.getCurrentUserDocRef().pipe(
      switchMap(userRef => {
        if (!userRef) {
          return throwError(() => new Error('User is not authenticated'));
        }

        return userRef.collection('preferences').get().pipe(
          map(preferencesSnapshot => {
            if(preferencesSnapshot.size === 0) {
              return undefined;
            }
            const userPreferences: Preferences = new Preferences();

            preferencesSnapshot.docs.forEach(doc => {
              const data = doc.data();
              switch (doc.id) {
                case 'money':
                  userPreferences.money = data['value'];
                  break;
                case 'categories':
                  userPreferences.categories = data;
                  break;
                case 'needs':
                  userPreferences.needs = data['value'];
                  break;
                case 'categories_restaurant':
                  userPreferences.categories_restaurant = data['value'];
                  break;
              }
            });

            return userPreferences;
          })
        );
      }),
      catchError(error => {
        console.error(error);
        return throwError(() => error);
      })
    );
  }

  hasSavedPreferences(): Observable<boolean> {
    return this.authService.currentUserValue.pipe(
      switchMap(user => {
        if (!user) {
          return throwError(() => new Error('User is not authenticated'));
        }

        const userRef = this.firestore.collection('users').doc(user.uid);
        return userRef.collection('preferences').get().pipe(
          map(preferencesSnapshot => {
            return preferencesSnapshot.size > 0;
          })
        );
      }),
      catchError(error => {
        console.error(error);
        return throwError(() => error);
      })
    );
  }


  getLocalPreferences() {
    const preferences = this.localStorageService.get("preferences");
    if (preferences) {
      this.preferences = JSON.parse(preferences);
    }
    return this.preferences;
  }
}
