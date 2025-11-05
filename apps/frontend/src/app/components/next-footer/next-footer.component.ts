import { Component } from '@angular/core';
import {DestinationService} from "../../services/destination.service";

@Component({
  selector: 'app-next-footer',
  templateUrl: './next-footer.component.html',
  styleUrls: ['./next-footer.component.css']
})
export class NextFooterComponent {

  constructor(public destinationService: DestinationService) {}

}
