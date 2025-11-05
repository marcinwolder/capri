import { Component, OnInit } from '@angular/core';
import {AuthService} from "../../services/auth.service";
import {NavigationEnd, Router} from "@angular/router";
import {filter} from "rxjs";

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit {
  userName: boolean = false;
  currentRoute: string = '';

  constructor(private router: Router, private authService: AuthService) {}

  ngOnInit() {
    this.authService.currentUserValue.subscribe(user => {
      this.userName = !!user;
    });

    this.router.events.pipe(
      filter((event: any): event is NavigationEnd => event instanceof NavigationEnd)
    ).subscribe((event) => {
      this.currentRoute = event.url;
    });
  }

  onSignOut() {
    this.authService.signOut().then(() => {
      this.router.navigate(['/']);
    });
  }
}
