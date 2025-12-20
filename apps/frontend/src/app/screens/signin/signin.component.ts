import { Component } from '@angular/core';
import {Router} from "@angular/router";
import {AuthService} from "../../services/auth.service";

@Component({
  selector: 'app-signin',
  templateUrl: './signin.component.html',
  styleUrls: ['./signin.component.css']
})
export class SigninComponent {
  error?: string;
  isDesktopApp = this.authService.isDesktopApp();
  constructor(private authService: AuthService, private router: Router) {}

  onSignIn(value: { email: string; password: string }) {
    this.authService.signInWithEmailAndPassword(value.email, value.password)
      .then(() => {
        this.router.navigate(['/selection']);
      });
  }

  signInWithGoogle() {
    this.authService.signInWithGoogle()
      .then(() => {
        this.router.navigate(['/selection']);
      });
  }

}
