import {Component, OnInit} from '@angular/core';
import {AuthService} from "../../../../services/auth.service";

@Component({
  selector: 'app-social-media',
  templateUrl: './social-media.component.html',
  styleUrls: ['./social-media.component.css']
})
export class SocialMediaComponent implements OnInit {

  constructor(private authService: AuthService) { }

  ngOnInit(): void {
    this.authService.getTwitterId().subscribe(id => {
      console.log(id);
    });
  }

}
