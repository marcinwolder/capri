import {Component, Input, OnInit} from '@angular/core';

@Component({
  selector: 'app-background',
  templateUrl: './background.component.html',
  styleUrls: ['./background.component.css']
})
export class BackgroundComponent implements OnInit{

  @Input() image: string = '' ;

  path = '';

  ngOnInit(): void {
    this.path = `url('assets/images/backgrounds/${this.image}')`
  }


}

