import {Categories} from "./categories";

export class Preferences{
  money: number = 1;
  categories: Categories = new Categories();
  categories_restaurant: string[] = [];
  needs: string[] = [];

  public toString(): string {
    return `Preferences: {money: ${this.money}, categories: ${JSON.stringify(this.categories, null, 2)}, needs: ${this.needs}}`;
  }
}
