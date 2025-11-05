import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TextNoteComponent } from './text-note.component';

describe('TextNoteComponent', () => {
  let component: TextNoteComponent;
  let fixture: ComponentFixture<TextNoteComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [TextNoteComponent]
    });
    fixture = TestBed.createComponent(TextNoteComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
