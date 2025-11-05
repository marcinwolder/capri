import { Component } from '@angular/core';
import {AuthService} from "../../services/auth.service";
import {Router} from "@angular/router";
import {user} from "@angular/fire/auth";

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {

  constructor(private router: Router, private authService: AuthService) {
  }

  start() {
    this.authService.currentUserValue.subscribe(user => {
      if (user) {
        this.router.navigate(['/selection']);
      } else {
        this.router.navigate(['/signin']);
      }
    });
  }
}
