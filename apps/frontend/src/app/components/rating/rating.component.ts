import {Component, EventEmitter, Input, OnInit, Output} from "@angular/core";

@Component({
  selector: 'app-rating',
  templateUrl: './rating.component.html',
  styleUrls: ['./rating.component.css']
})
export class RatingComponent implements OnInit{
  @Input()
  value? : number;
  @Output()
  onSetRating = new EventEmitter<number>();


  private totalStars: number = 5;
  stars: number[] = [];
  rating: number = -1;
  hoverIndex: number = -1;

  constructor() {}

  ngOnInit(): void {
    this.initializeStars();
    this.rating = this.value ? this.value - 1 : -1;
  }

  initializeStars(): void {
    this.stars = Array.from({length: this.totalStars}, (_, index) => index);
  }

  setHover(index: number): void {
    this.hoverIndex = index;
  }

  clearHover(): void {
    this.hoverIndex = -1;
  }

  rate(index: number): void {
    this.rating = index;
    this.onSetRating.emit(index + 1);
  }
}
