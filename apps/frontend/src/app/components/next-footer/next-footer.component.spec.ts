import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NextFooterComponent } from './next-footer.component';

describe('NextFooterComponent', () => {
  let component: NextFooterComponent;
  let fixture: ComponentFixture<NextFooterComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ NextFooterComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(NextFooterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
