import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TransportationComponent } from './transportation.component';

describe('TransportationComponent', () => {
  let component: TransportationComponent;
  let fixture: ComponentFixture<TransportationComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [TransportationComponent]
    });
    fixture = TestBed.createComponent(TransportationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should render walking mode for walking transportation', () => {
    component.transportation = [12, 'walking'];

    expect(component.mode).toBe('foot');
    expect(component.minutes).toBe(12);
  });

  it('should render car mode for driving transportation', () => {
    component.transportation = [12, 'driving'];

    expect(component.mode).toBe('car');
    expect(component.minutes).toBe(12);
  });

  it('should convert seconds to minutes for routed transportation', () => {
    component.transportation = [600, 'driving'];

    expect(component.minutes).toBe(10);
  });
});
