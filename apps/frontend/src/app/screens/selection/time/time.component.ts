import {Component, OnInit} from '@angular/core';
import {DestinationService} from "../../../services/destination.service";
import {Router} from "@angular/router";
import {PreferencesService} from "../../../services/preferences.service";
import {LocalStorageService} from "../../../services/local-storage.service";
import {RecommendationService} from "../../../services/recommendation.service";

const PreferencesMethods = [
  'Saved Preferences',
  'Quiz',
  'Social Media',
  'Text Note',
  'Chat bot'
];

type PreferencesMethod = typeof PreferencesMethods[number];

@Component({
  selector: 'app-time',
  templateUrl: './time.component.html',
  styleUrls: ['./time.component.css']
})
export class TimeComponent implements OnInit{

  constructor(private _router: Router, public destinationService: DestinationService,
              private preferencesService: PreferencesService, private localStorageService: LocalStorageService,
              private recommendationService: RecommendationService) {}

  ngOnInit(): void {
    const destination = this.destinationService.getDestination();
    this.dates = destination.dates;
    const saved_preferences = this.preferencesService.getLocalPreferences();
    this.money = saved_preferences.money;
    this.preferencesMethod = this.localStorageService.get('preferencesMethod') || this.preferencesMethod;
    this.algorithmMode = this.recommendationService.getAlgorithmMode();
    this.preferencesService.hasSavedPreferences().subscribe(hasSavedPreferences => {
      this.hasSavedPreferences = hasSavedPreferences;
      if(hasSavedPreferences && !this.preferencesMethod) {
        this.preferencesMethod = 'Saved Preferences';
      }
    });
    this.setNavFunctions()
  }

  private setNavFunctions() {
    this.destinationService.setNextFunction(() => {
      this.nextClicked = true;
      if(!this.preferencesMethod || !this.rodoAccepted) return;
      this.preferencesService.setMoney(this.money);
      this.preferencesService.save(true);
      this.destinationService.setTime(this.dates)
      let link = 'selection/';
      switch (this.preferencesMethod) {
        case 'Saved Preferences':
          this.preferencesService.getUserPreferences().subscribe(preferences => {
            this.recommendationService.setPreferences(preferences!);
            this._router.navigate(['trip']);
          })
          return;
        case 'Social Media':
          link += 'social-media';
          break;
        case 'Quiz':
          link += 'details';
          break;
        case 'Text Note':
          link += 'text-note';
          break;
        case 'Chat bot':
          link += 'chat';
          break;
      }
      this._router.navigate([link]);
    });
    this.destinationService.setPreviousFunction(() => {
      this._router.navigate(['selection'])
    });
  }

  dates!: [Date, Date];
  preferencesMethod!: PreferencesMethod;
  nextClicked = false;
  hasSavedPreferences = false;
  rodoAccepted = false;
  algorithmMode: 'legacy' | 'wibit' = 'legacy';

  setDates(dates: [Date, Date]) {
    this.dates = dates;
    console.log("DATE: "+this.dates);
  }

  setPreferencesMethod(preference: PreferencesMethod) {
    this.preferencesMethod = preference;
    this.localStorageService.set('preferencesMethod', preference);
  }

  protected readonly PreferencesMethods = PreferencesMethods;
  protected money = 0;

  setAlgorithm(mode: 'legacy' | 'wibit') {
    this.algorithmMode = mode;
    this.recommendationService.setAlgorithmMode(mode);
  }
}
