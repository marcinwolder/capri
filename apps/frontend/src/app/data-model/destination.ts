export class Destination {
  city_id: number = 0;
  city: string = '';
  country: string = '';
  dates: [Date, Date] = [new Date(), new Date()];
  days: number = 1;
}
