import {Injectable} from '@angular/core';
import {LocalStorageService} from "./local-storage.service";
import {Categories} from "../data-model/categories";
import {Observable, of} from "rxjs";
import {Preferences} from "../data-model/preferences";

@Injectable({
  providedIn: 'root'
})
export class PreferencesService {

  constructor(private localStorageService: LocalStorageService) {
    this.getLocalPreferences();
  }

  private preferences: Preferences = new Preferences();

  public save(local: boolean = false){
    this.localStorageService.set("preferences", JSON.stringify(this.preferences));
    if(local) return;
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


  getUserPreferences(): Observable<Preferences | undefined> {
    const prefs = this.getLocalPreferences();
    return of(prefs);
  }

  hasSavedPreferences(): Observable<boolean> {
    const hasPrefs = !!this.localStorageService.get("preferences");
    return of(hasPrefs);
  }


  getLocalPreferences() {
    const preferences = this.localStorageService.get("preferences");
    if (preferences) {
      this.preferences = JSON.parse(preferences);
    }
    return this.preferences;
  }
}
