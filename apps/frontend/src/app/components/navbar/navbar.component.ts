import { Component, OnInit } from '@angular/core';
import {NavigationEnd, Router} from "@angular/router";
import {filter, Observable} from "rxjs";
import {ServiceStatusService} from "../../services/service-status.service";

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit {
  currentRoute: string = '';

  backendOffline$!: Observable<boolean>;
  llamaOffline$!: Observable<boolean>;

  constructor(private router: Router, private serviceStatus: ServiceStatusService) {
    this.backendOffline$ = this.serviceStatus.backendOffline$;
    this.llamaOffline$ = this.serviceStatus.llamaOffline$;
  }

  ngOnInit() {
    this.router.events.pipe(
      filter((event: any): event is NavigationEnd => event instanceof NavigationEnd)
    ).subscribe((event) => {
      this.currentRoute = event.url;
    });
  }

}
