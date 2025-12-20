import {Injectable} from '@angular/core';
import {BehaviorSubject, map, Observable, of} from 'rxjs';
import {User} from "../data-model/user";
import {LocalStorageService} from "./local-storage.service";

export interface LocalUser {
  uid: string;
  displayName?: string;
  email?: string;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private readonly storageKey = 'local-user';
  private currentUserSubject: BehaviorSubject<LocalUser | null>;

  constructor(private localStorage: LocalStorageService) {
    this.currentUserSubject = new BehaviorSubject<LocalUser | null>(this.loadStoredUser());
  }

  private generateLocalId(): string {
    return `local-${Math.random().toString(36).slice(2, 10)}-${Date.now()}`;
  }

  private loadStoredUser(): LocalUser | null {
    const saved = this.localStorage.get(this.storageKey);
    if (!saved) {
      return null;
    }
    try {
      return JSON.parse(saved) as LocalUser;
    } catch (e) {
      console.error('Failed to parse stored user', e);
      return null;
    }
  }

  private createLocalUser(): LocalUser {
    const user: LocalUser = {
      uid: this.generateLocalId(),
      displayName: 'Local User'
    };
    this.persist(user);
    return user;
  }

  private persist(user: LocalUser | null) {
    if (user) {
      this.localStorage.set(this.storageKey, JSON.stringify(user));
    } else {
      this.localStorage.remove(this.storageKey);
    }
  }

  get currentUserValue(): Observable<LocalUser | null> {
    return this.currentUserSubject.asObservable();
  }

  public ensureUser(): LocalUser {
    const user = this.currentUserSubject.value ?? this.loadStoredUser();
    if (!user) {
      throw new Error('User not signed in');
    }
    this.currentUserSubject.next(user);
    this.persist(user);
    return user;
  }

  public getCurrentUser(): LocalUser | null {
    return this.currentUserSubject.value;
  }

  public getCurrentUserInfo(): Observable<User | null> {
    return this.currentUserValue.pipe(
      map(user => {
        if (!user) {
          return null;
        }
        return {
          id: user.uid,
          name: user.displayName || 'Local User',
          surname: '',
          birthdate: '',
          email: user.email || '',
          preferences: []
        } as User;
      })
    );
  }

  public async signOut() {
    this.currentUserSubject.next(null);
    this.persist(null);
  }

  public async signInWithEmailAndPassword(email: string, password: string) {
    const user = this.createLocalUser();
    user.email = email;
    this.currentUserSubject.next(user);
    this.persist(user);
    return user;
  }

  public async signInWithGoogle() {
    const user = this.createLocalUser();
    this.currentUserSubject.next(user);
    this.persist(user);
    return user;
  }

  public async handleGoogleRedirect() {
    const user = this.createLocalUser();
    this.currentUserSubject.next(user);
    this.persist(user);
    return user;
  }

  public async createUserWithEmailAndPassword(email: string, password: string,
                                              name?: string, surname?: string, birthdate?: string) {
    const user = this.createLocalUser();
    user.email = email;
    user.displayName = name || 'Local User';
    this.currentUserSubject.next(user);
    this.persist(user);
    return user;
  }

  public isDesktopApp(): boolean {
    return typeof window !== 'undefined' && !!(window as any).desktopApp?.isDesktop;
  }

  public getTwitterId(): Observable<string> {
    return of('twitter-integration-disabled');
  }
}
