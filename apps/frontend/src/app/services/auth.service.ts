import {Injectable} from '@angular/core';
import {AngularFireAuth} from '@angular/fire/compat/auth';
import {catchError, firstValueFrom, from, map, Observable, of, switchMap, throwError} from 'rxjs';
import {GoogleAuthProvider, TwitterAuthProvider} from 'firebase/auth';
import {AngularFirestore} from "@angular/fire/compat/firestore";
import {User} from "../data-model/user";
import {getAuth, linkWithPopup, signInWithPopup} from "@angular/fire/auth";
import {doc, getDoc} from "@angular/fire/firestore";
import firebase from "firebase/compat/app";

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  constructor(private afAuth: AngularFireAuth, private firestore: AngularFirestore) {}

  public get currentUserValue() {
    return this.afAuth.authState;
  }

  public getCurrentUserDocRef() {
    return this.currentUserValue.pipe(
      switchMap(user => {
        if (!user) {
          return of(null);
        }
        return of(this.firestore.collection('users').doc(user.uid));
      })
    );
  }

  public getCurrentUserInfo(): Observable<User | null> {
    return this.getCurrentUserDocRef().pipe(
      switchMap(userRef => {
        if (!userRef) {
          return of(null);
        }
        return from(userRef.get()).pipe(
          map(doc => {
            if (!doc.exists) {
              return null;
            }
            return doc.data() as User;
          }),
          catchError(error => {
            console.error('Error fetching user info:', error);
            return of(null);
          })
        );
      })
    );
  }

  public async signOut() {
    await this.afAuth.signOut();
  }

  public async signInWithEmailAndPassword(email: string, password: string) {
    return await this.afAuth.signInWithEmailAndPassword(email, password);
  }

  /**
   * Use popup by default; fall back to redirect when popups are blocked (Electron).
   */
  public async signInWithGoogle(): Promise<firebase.auth.UserCredential | void> {
    const provider = new GoogleAuthProvider();

    if (this.isDesktopApp()) {
      await this.afAuth.signInWithRedirect(provider);
      return;
    }

    try {
      const res = await this.afAuth.signInWithPopup(provider);
      await this.createUserFromCredential(res);
      return res;
    } catch (err: any) {
      if (err?.code === 'auth/popup-blocked' || err?.code === 'auth/popup-closed-by-user') {
        await this.afAuth.signInWithRedirect(provider);
        return;
      }
      throw err;
    }
  }

  /**
   * Complete redirect flow after returning from provider.
   */
  public async handleGoogleRedirect(): Promise<firebase.auth.UserCredential | null> {
    const res = await this.afAuth.getRedirectResult();
    if (res?.user) {
      await this.createUserFromCredential(res);
      return res;
    }
    return null;
  }

  public async createUserWithEmailAndPassword(email: string, password: string,
                                              name?: string, surname?: string, birthdate?: string) {
    return await this.afAuth.createUserWithEmailAndPassword(email, password)
      .then(async res => {
        await res.user!.updateProfile({
          displayName: name
        });
        return res;
      }).then(res => {
        return this.createUser(res.user!.uid, name || '',
          surname || '', birthdate || '');
      });
  }

  private async createUser(id: string, name: string, surname: string, birthdate: string = '') {
    const userRef = this.firestore.collection('users').doc(id);
    const docSnap = await firstValueFrom(userRef.get());
    if (!docSnap.exists) {
      await userRef.set(
        {
          id: id,
          name: name,
          surname: surname,
          birthdate: birthdate,
        }
      );
    }
  }

  private async createUserFromCredential(res: firebase.auth.UserCredential) {
    const name = res.user!.displayName?.split(' ')[0] || '';
    const surname = res.user!.displayName?.split(' ')[1] || '';
    await this.createUser(res.user!.uid, name, surname);
  }

  private isDesktopApp(): boolean {
    return typeof window !== 'undefined' && !!(window as any).desktopApp?.isDesktop;
  }

  public async linkTwitterAccount(): Promise<string> {
    const provider = new TwitterAuthProvider();
    try {
      const auth = getAuth();
      return linkWithPopup(auth.currentUser!, provider).then((result: any) => {
        const twitter_id = result._tokenResponse.screenName;
        const userRef = this.firestore.collection('users').doc(result.user.uid);
        userRef.update({twitter_id: twitter_id});
        return twitter_id;
      }).catch((error) => {
        throw Error('Error linking Twitter account:' + error);
      }).then((twitter_id) => {
        console.log('Twitter account linked:', twitter_id);
        return twitter_id;
      });

    } catch (error) {
      throw Error('Error linking Twitter account:' + error);
    }
  }

  public getTwitterId(): Observable<string> {
    return this.getCurrentUserInfo().pipe(
      switchMap(user => {
        if (!user?.twitter_id) {
          return from(this.linkTwitterAccount()).pipe(
            switchMap(twitter_id => {
              console.log('1Twitter account linked:', twitter_id);
              if(!twitter_id) {
                return throwError(() => new Error('Error linking Twitter account'));
              }
              return of(twitter_id);
            })
          );
        } else {
          return of(user.twitter_id);
        }
      })
    );
  }


}
