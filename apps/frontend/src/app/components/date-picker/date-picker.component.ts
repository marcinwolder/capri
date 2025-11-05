import {Component, ElementRef, EventEmitter, Inject, Input, OnDestroy, OnInit, Output} from '@angular/core';
import {DOCUMENT} from "@angular/common";

@Component({
  selector: 'app-date-picker',
  templateUrl: './date-picker.component.html',
  styleUrls: ['./date-picker.component.css']
})
export class DatePickerComponent implements OnInit, OnDestroy{
  @Input() date: Date = new Date();
  @Input() secondDate: Date = this.date;
  @Input() range: boolean = false;
  @Input() canSelectPastDates: boolean = true;
  @Output() onDateSelect = new EventEmitter<Date[]>();

  protected firstDateSelected: boolean = true;
  protected secondDateSelected: boolean = true;

  protected currentDate = new Date();

  protected MONTH_NAMES = [
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September',
    'October',
    'November',
    'December'
  ];
  protected DAYS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  protected showDatepicker = false;
  protected month!: number;
  protected year!: number;
  protected no_of_days = [] as number[];
  protected blank_days = [] as number[];

  constructor(private elRef: ElementRef, @Inject(DOCUMENT) private document: Document) {}

  private emitDates(dates: Date[]) {
    dates.forEach(date => date.setHours(0, 0, 0, 0));
    this.onDateSelect.emit(dates);
  }

  private getDateStr(date: Date) {
    return this.DAYS[date.getDay()] + ' ' + date.toLocaleDateString();
  }

  protected getInputValue() {
    if(this.range) {
      return this.date.toDateString() + ' - ' + this.secondDate.toDateString();
    }
    return this.date.toDateString();
  }

  protected toggleDatepicker() {
    this.showDatepicker = !this.showDatepicker;
    if (this.showDatepicker) {
      this.document.addEventListener('click', this.closeDatepickerFromOutsideClick, true);
    } else {
      this.document.removeEventListener('click', this.closeDatepickerFromOutsideClick, true);
    }
  }

  protected closeDatepickerFromOutsideClick = (event: MouseEvent) => {
    if (!this.elRef.nativeElement.contains(event.target)) {
      this.showDatepicker = false;
      if(this.range){
        this.emitDates([this.date, this.secondDate]);
      }
      else {
        this.emitDates([this.date]);
      }
      this.document.removeEventListener('click', this.closeDatepickerFromOutsideClick, true);
    }
  }

  ngOnDestroy() {
    this.document.removeEventListener('click', this.closeDatepickerFromOutsideClick, true);
  }

  ngOnInit(): void {
    this.month = this.date.getMonth();
    this.year = this.date.getFullYear();
    this.getNoOfDays();
  }

  protected isToday(date: number) {
    const today = new Date();
    return today.getDate() === date && today.getMonth() === this.month && today.getFullYear() === this.year;
  }

  protected isBetweenDates(date: number) {
    const tempDate = new Date(this.year, this.month, date);
    return tempDate > this.date && tempDate < this.secondDate;
  }

  isPastDate(date: number) {
    const tempDate = new Date(this.year, this.month, date+1);
    return tempDate < this.currentDate;
  }

  protected isSelectedDate(date: number) {
    if (this.range) {
      return this.firstDateSelected && this.date.getDate() === date && this.date.getMonth() === this.month && this.date.getFullYear() === this.year
        || this.secondDateSelected && this.secondDate.getDate() === date && this.secondDate.getMonth() === this.month && this.secondDate.getFullYear() === this.year
    }
    return this.date.getDate() === date && this.date.getMonth() === this.month && this.date.getFullYear() === this.year;
  }

  protected setDate(date: number) {
    if(this.isPastDate(date) && !this.canSelectPastDates) {
      return;
    }

    const selectedDate = new Date(this.year, this.month, date);

    if (this.range) {
      if(this.firstDateSelected && this.secondDateSelected) {
        this.firstDateSelected = false;
        this.secondDateSelected = false;
      }
      if (this.firstDateSelected) {
        this.secondDate = selectedDate;
        if(this.date > selectedDate) {
          this.date = selectedDate;
          return;
        }
        this.secondDateSelected = true;
        this.emitDates([this.date, this.secondDate]);
        this.showDatepicker = false;
      } else {
        this.date = selectedDate;
        this.secondDate = selectedDate;
        this.firstDateSelected = true;
      }
    } else {
      this.date = selectedDate;
      this.secondDate = selectedDate;
      this.showDatepicker = false;
      this.emitDates([this.date]);
    }
  }


  protected getNoOfDays() {
    const daysInMonth = new Date(this.year, this.month + 1, 0).getDate();

    let dayOfWeek = new Date(this.year, this.month).getDay();
    let blankDaysArray = [];
    for (let i = 1; i <= dayOfWeek; i++) {
      blankDaysArray.push(i);
    }

    let daysArray = [];
    for (let i = 1; i <= daysInMonth; i++) {
      daysArray.push(i);
    }

    this.blank_days = blankDaysArray;
    this.no_of_days = daysArray;
  }

  protected nextMonth() {
    if (this.month === 11) {
      this.year++;
      this.month = 0;
    } else {
      this.month++;
    }
    this.getNoOfDays();
  }

  protected previousMonth() {
    if (this.month === 0) {
      this.year--;
      this.month = 11;
    } else {
      this.month--;
    }
    this.getNoOfDays();
  }

  protected trackByIdentity = (index: number, item: any) => item;
}
