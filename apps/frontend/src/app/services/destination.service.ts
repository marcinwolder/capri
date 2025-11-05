import {Injectable} from '@angular/core';
import {Destination} from "../data-model/destination";
import {Categories} from "../data-model/categories";
import {LocalStorageService} from "./local-storage.service";

@Injectable({
  providedIn: 'root'
})
export class DestinationService {

  constructor(private localStorageService: LocalStorageService) {
    this.getDestination();
  }

  private destination: Destination = new Destination();

  private nextFunction = () => {};
  private previousFunction?: () => void = undefined;

  setNextFunction(nextFunction: () => void) {
    this.nextFunction = nextFunction;
  }

  next() {
    this.nextFunction();
  }

  setPreviousFunction(previousFunction?: () => void) {
    this.previousFunction = previousFunction;
  }

  previous() {
    if (this.previousFunction) {
      this.previousFunction();
    }
  }

  isPreviousDisabled() {
    return !this.previousFunction;
  }

  setCity(city_id: number, city_name: string, country: string) {
    this.destination.city = city_name;
    this.destination.country = country;
    this.destination.city_id = city_id;

    this.localStorageService.set("destination", JSON.stringify(this.destination));
  }

  setTime(dates: [Date, Date]) {
    this.destination.dates = dates;
    this.destination.days = this.getTripLength();
    this.localStorageService.set("destination", JSON.stringify(this.destination));
  }

  getTripLength(): number {
    return this.destination.dates[1].getDate() - this.destination.dates[0].getDate() + 1;
  }

  getDestination(): Destination {
    const destination = this.localStorageService.get("destination");
    if (destination) {
      this.destination = JSON.parse(destination);
      this.destination.dates = [new Date(this.destination.dates[0]), new Date(this.destination.dates[1])];
    }
    return this.destination;
  }


}
