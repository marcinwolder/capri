import {Component, OnInit} from '@angular/core';
import {Router} from "@angular/router";
import {DestinationService} from "../../../../services/destination.service";
import {RecommendationService} from "../../../../services/recommendation.service";

@Component({
  selector: 'app-text-note',
  templateUrl: './text-note.component.html',
  styleUrls: ['./text-note.component.css']
})
export class TextNoteComponent implements OnInit{

  constructor(private _router: Router, public destinationService: DestinationService,
              private recommendationService: RecommendationService) {}

  textNote: string = '';

  ngOnInit(): void {
      this.destinationService.setPreviousFunction(() => {
        this._router.navigate(['selection/time'])
      });
      this.destinationService.setNextFunction(() => {
        this.recommendationService.setNote(this.textNote)
        this._router.navigate(['trip'])
      });
  }

}
