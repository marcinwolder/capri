import {Image} from "./image";

export class Place {
  id: string = '';
  name: string = '';
  description: string = '';
  formattedAddress: string = '';
  types: string[] = [];
  price: number = 0;
  rating: number = 0;
  reviews: number = 0;
  image: Image = new Image();
  googleMapsUri: string = '';
  latitude: number = 0;
  longitude: number = 0;
  user_rating?: number;
  personal_rating?: number;
  transportation?: [number, string];
  restaurants?: Place[];
}
