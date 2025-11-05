import { Component } from '@angular/core';
import { AngularFireAuth } from '@angular/fire/compat/auth';
import {Router} from "@angular/router";
import {AuthService} from "../../services/auth.service";

@Component({
  selector: 'app-signin',
  templateUrl: './signin.component.html',
  styleUrls: ['./signin.component.css']
})
export class SigninComponent {
  error?: string;
  constructor(private authService: AuthService, private router: Router) {}

  onSignIn(value: { email: string; password: string }) {
    this.authService.signInWithEmailAndPassword(value.email, value.password)
      .then(res => {
        console.log('You are Successfully signed in!', res);
        this.router.navigate(['/selection']);
      })
      .catch(err => {
        console.log('Something went wrong:', typeof err.message);
        this.error = err.message.replace('Firebase: ', '');
      });
  }

  signInWithGoogle() {
    this.authService.signInWithGoogle()
      .then(res => {
        console.log('You are Successfully signed in with Google!', res);
        this.router.navigate(['/selection']);
      })
      .catch(err => {
        console.log('Error during Google sign in:', typeof err.message);
        this.error = err.message.replace('Firebase: ', '');
      });
  }

}
