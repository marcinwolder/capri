import {Component, OnInit} from '@angular/core';
import {DestinationService} from "../../../services/destination.service";
import {Router} from "@angular/router";
// @ts-ignore
import citiesData from "../../../constants/cities.json";


@Component({
  selector: 'app-city',
  templateUrl: './city.component.html',
  styleUrls: ['./city.component.css']
})
export class CityComponent implements OnInit{

  constructor(private _router: Router, private destinationService: DestinationService) {}

  ngOnInit(): void {
    this.destinationService.setNextFunction(() => {
      this.nextClicked = true;
    });
    this.destinationService.setPreviousFunction(undefined);
    this.cities = citiesData;
  }

  nextClicked = false;

  searchText = '';
  cities: { country: string, city: string, id: number }[] = [];
  filteredCities: { city: string, country: string, id: number }[] = [];
  isInputFocused: boolean = false;


  searchCities() {
    if (this.searchText) {
      this.filteredCities = this.cities.filter(item =>
        item.city.toLowerCase().startsWith(this.searchText.toLowerCase())
      ).slice(0, 5);
    } else {
      this.filteredCities = [];
    }
  }

  popularCities: { img: string; name: string, country: string, id: number }[] = [
    {name:'Krakow', country:'Poland', img: 'assets/images/city_thumbnails/cracow.jpg', id: 1616172264},
    {name:'Prague', country:'Czech Republic', img: 'assets/images/city_thumbnails/prague.jpg', id: 1203744823},
    {name:'Budapest', country:'Hungary', img: 'assets/images/city_thumbnails/budapest.jpg', id: 1348611435},
    {name:'Rome', country:'Italy', img: 'assets/images/city_thumbnails/rome.jpg', id: 1380382862},
    {name:'Paris', country:'France', img: 'assets/images/city_thumbnails/paris.jpg', id: 1250015082},
    {name:'Rio de Janeiro', country:'Brazil', img: 'assets/images/city_thumbnails/rio.jpg', id: 1076887657},
    {name:'New York', country:'United States', img: 'assets/images/city_thumbnails/new_york.jpg', id: 1840034016},
    {name:'London', country:'United Kingdom', img: 'assets/images/city_thumbnails/london.jpg', id: 1826645935},
    {name:'Barcelona', country:'Spain', img: 'assets/images/city_thumbnails/barcelona.jpg', id: 1608408567},
    {name:'Lisbon', country:'Portugal', img: 'assets/images/city_thumbnails/lisbon.jpg', id: 1620619017},
    {name:'Dubrovnik', country:'Croatia', img: 'assets/images/city_thumbnails/dubrovnik.jpg', id: 1191004286},
    {name:'Dubai', country:'United Arab Emirates', img: 'assets/images/city_thumbnails/dubai.jpg', id: 1784736618},

  ];



  select(cityName: string, country: string, id: number): void {
    this.destinationService.setCity(id, cityName, country);
    this._router.navigate(['selection/time']);
  }

  onFocus() {
    this.isInputFocused = true;
  }

  onBlur() {
    setTimeout(() => this.isInputFocused = false, 100);
  }

  protected readonly focus = focus;
}
