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
type TripMode = 'standard' | 'night' | 'luxury' | 'budget';
type DayRhythm = 'balanced' | 'owl' | 'lark';
type GroupingMode = 'current' | 'multi-day-vrp';
type RouteMode = 'mst-2opt' | 'christofides';

type DayPreview = {
  dayLabel: string;
  firstAttractionHour: string;
  lastAttractionHour: string;
  totalAttractions: number;
  barOrClubAttractions: number;
  clubs: number;
  bars: number;
  cafes: number;
};

type RhythmPreview = {
  label: string;
  city: string;
  tripLengthDays: number;
  mode: string;
  nightlifeShare: string;
  days: DayPreview[];
};

const RHYTHM_PREVIEWS: Record<DayRhythm, RhythmPreview> = {
  balanced: {
    label: 'Balanced',
    city: 'Rome',
    tripLengthDays: 2,
    mode: 'Balanced',
    nightlifeShare: '25%',
    days: [
      {
        dayLabel: 'Day 1',
        firstAttractionHour: '09:00',
        lastAttractionHour: '22:00',
        totalAttractions: 7,
        barOrClubAttractions: 2,
        clubs: 0,
        bars: 1,
        cafes: 1
      },
      {
        dayLabel: 'Day 2',
        firstAttractionHour: '10:00',
        lastAttractionHour: '23:00',
        totalAttractions: 8,
        barOrClubAttractions: 3,
        clubs: 1,
        bars: 1,
        cafes: 1
      }
    ]
  },
  lark: {
    label: 'Lark',
    city: 'Rome',
    tripLengthDays: 2,
    mode: 'Morning bird',
    nightlifeShare: '13%',
    days: [
      {
        dayLabel: 'Day 1',
        firstAttractionHour: '08:00',
        lastAttractionHour: '20:00',
        totalAttractions: 8,
        barOrClubAttractions: 1,
        clubs: 0,
        bars: 0,
        cafes: 1
      },
      {
        dayLabel: 'Day 2',
        firstAttractionHour: '08:00',
        lastAttractionHour: '21:00',
        totalAttractions: 8,
        barOrClubAttractions: 1,
        clubs: 0,
        bars: 1,
        cafes: 0
      }
    ]
  },
  owl: {
    label: 'Owl',
    city: 'Rome',
    tripLengthDays: 2,
    mode: 'Night owl',
    nightlifeShare: '40%',
    days: [
      {
        dayLabel: 'Day 1',
        firstAttractionHour: '11:00',
        lastAttractionHour: '00:00',
        totalAttractions: 6,
        barOrClubAttractions: 3,
        clubs: 1,
        bars: 1,
        cafes: 1
      },
      {
        dayLabel: 'Day 2',
        firstAttractionHour: '12:00',
        lastAttractionHour: '01:00',
        totalAttractions: 7,
        barOrClubAttractions: 4,
        clubs: 2,
        bars: 1,
        cafes: 1
      }
    ]
  }
};

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
  tripMode: TripMode = 'standard';
  dayRhythm: DayRhythm = 'balanced';
  groupingMode: GroupingMode = 'current';
  routeMode: RouteMode = 'mst-2opt';
  diversityLevel = 60;
  humanTouchLevel = 50;

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

  setTripMode(mode: TripMode) {
    this.tripMode = mode;
  }

  setDayRhythm(rhythm: DayRhythm) {
    this.dayRhythm = rhythm;
  }

  get dayRhythmPreview(): RhythmPreview {
    return RHYTHM_PREVIEWS[this.dayRhythm];
  }

  setGroupingMode(mode: GroupingMode) {
    this.groupingMode = mode;
  }

  setRouteMode(mode: RouteMode) {
    this.routeMode = mode;
  }
}
