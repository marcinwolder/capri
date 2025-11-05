import {Place} from "./place";
import {TripDay} from "./tripDay";

export interface Trip {
  id: string;
  days: TripDay[];
  summary: string;
  city_name?: string;
  city_id?: string;
}
