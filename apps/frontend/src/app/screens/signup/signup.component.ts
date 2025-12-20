import { Component } from '@angular/core';
import { Router } from "@angular/router";
import { AuthService } from "../../services/auth.service";

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent {
  error?: string;
  constructor(private authService: AuthService, private router: Router) { }

  onSignup(value: any) {
    this.authService.createUserWithEmailAndPassword(value.email, value.password, value.name, value.surname, value.birthdate)
      .then(() => this.router.navigate(['/selection']));
  }
}
