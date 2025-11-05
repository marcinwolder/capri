import {Component, OnInit} from '@angular/core';
import {DestinationService} from "../../../../services/destination.service";
import {Router} from "@angular/router";
import {Categories} from "../../../../data-model/categories";
import {categories} from "../../../../constants/categories";
import {categories_restaurant} from "../../../../constants/categories_restaurant";
import {preferences} from "../../../../constants/preferences";
import {PreferencesService} from "../../../../services/preferences.service";
import {RecommendationService} from "../../../../services/recommendation.service";

@Component({
  selector: 'app-details',
  templateUrl: './details.component.html',
  styleUrls: ['./details.component.css']
})
export class DetailsComponent implements OnInit {

  constructor(private _router: Router, private destinationService: DestinationService,
              private preferencesService: PreferencesService, private recommendationService: RecommendationService) {
  }

  ngOnInit(): void {
    const saved_preferences = this.preferencesService.getLocalPreferences();
    categories.forEach(attraction => {
      attraction.selected = saved_preferences.categories[attraction.key] !== undefined;
      if (attraction.selected) {
        attraction.subcategories.forEach(subcategory => {
          subcategory.selected = saved_preferences.categories[attraction.key].includes(subcategory.key);
        });
      }
    });
    preferences.forEach(need => {
      need.selected = saved_preferences.needs.includes(need.key);
    });
    categories_restaurant.forEach(attraction => {
      attraction.selected = saved_preferences.categories_restaurant.includes(attraction.key);
    });


    this.destinationService.setNextFunction(() => {
      this.preferencesService.setNeeds(preferences
          .filter(need => need.selected)
          .map(need => need.key)
      );
      this.preferencesService.setCategories(categories
        .filter(attraction => attraction.selected)
        .reduce((acc: Categories, attraction) => {
          acc[attraction.key] = attraction.subcategories
            .filter(subcategory => subcategory.selected)
            .map(subcategory => subcategory.key);
          return acc;
        }, {} as Categories));
      this.preferencesService.setCategoriesRestaurant(categories_restaurant
        .filter(attraction => attraction.selected)
        .reduce((acc: string[], attraction) => {
          acc.push(attraction.key);
          return acc;
        }, [] as string[]));
      this.preferencesService.save()
      this.recommendationService.setPreferences(this.preferencesService.getLocalPreferences());
      this._router.navigate(['trip']);
    });


    this.destinationService.setPreviousFunction(() => {
      this._router.navigate(['selection/time']);
    });
  }

  toggleSelected(selectable: any): void {
    selectable.selected = !selectable.selected;
  }

  protected readonly categories = categories;
  protected readonly categories_restaurant = categories_restaurant;
  protected readonly preferences = preferences;
}
