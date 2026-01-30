import {Place} from "./place";
import {TripDay} from "./tripDay";

export interface Trip {
  id: string;
  days: TripDay[];
  summary: string;
  city_name?: string;
  city_id?: string;
  survey?: TripSurvey;
}

export interface TripSurvey {
  sus: {
    answers: number[];
    score: number;
  };
  csat: number;
  nps: number;
  subjective: {
    questions: string[];
    answers: number[];
  };
  submitted_at?: string;
  updated_at?: string;
}
