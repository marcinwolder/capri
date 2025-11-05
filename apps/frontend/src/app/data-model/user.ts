import {Place} from "./place";
import {Destination} from "./destination";

export class User {
  id: string = '';
  name: string = '';
  surname: string = '';
  birthdate: string = '';
  email: string = '';
  preferences: string[] = [];
  twitter_id?: string;
}
