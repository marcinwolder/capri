import { Component } from '@angular/core';
import { AngularFireAuth } from '@angular/fire/compat/auth';
import { AngularFirestore } from '@angular/fire/compat/firestore';
import {Router} from "@angular/router";
import {user} from "@angular/fire/auth";
import {AuthService} from "../../services/auth.service";

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent {
  error?: string;
  constructor(private authService: AuthService, private router: Router) {}

  onSignup(value: any) {
    this.authService.createUserWithEmailAndPassword(value.email, value.password, value.name, value.surname, value.birthdate)
      .then(() => this.router.navigate(['/selection']))
      .catch(error => this.error = error.message.replace('Firebase: ', ''));
  }
}
