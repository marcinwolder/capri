import {Injectable} from '@angular/core';
import {AngularFirestore} from "@angular/fire/compat/firestore";
import {AuthService} from './auth.service';
import {User} from "../data-model/user";
import {catchError, firstValueFrom, map, Observable, of, switchMap} from "rxjs"; 

@Injectable({
  providedIn: 'root'
})
export class UserService {

}
