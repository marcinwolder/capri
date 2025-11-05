import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SingupComponent } from './signup.component';

describe('SingupComponent', () => {
  let component: SingupComponent;
  let fixture: ComponentFixture<SingupComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [SingupComponent]
    });
    fixture = TestBed.createComponent(SingupComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
