import {Component, Input} from '@angular/core';

@Component({
  selector: 'app-transportation',
  templateUrl: './transportation.component.html',
  styleUrls: ['./transportation.component.css']
})
export class TransportationComponent {
  @Input()
  transportation!: [number, string];

  get minutes(): number {
    const val = this.transportation?.[0] ?? 0;
    // If value looks like seconds (over 90 and mode provided), convert to minutes.
    return Math.round(val > 90 ? val / 60 : val);
  }

  get mode(): 'car' | 'foot' {
    const raw = (this.transportation?.[1] || '').toLowerCase();
    if (raw.includes('car')) {
      return 'car';
    }
    if (raw.includes('foot') || raw.includes('walk')) {
      return 'foot';
    }
    return 'foot';
  }
}
