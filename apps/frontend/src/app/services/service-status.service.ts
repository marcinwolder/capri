import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, forkJoin, of } from 'rxjs';
import { catchError, finalize, map, timeout } from 'rxjs/operators';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ServiceStatusService {
  private backendOfflineSubject = new BehaviorSubject<boolean>(false);
  private llamaOfflineSubject = new BehaviorSubject<boolean>(false);
  private checkingSubject = new BehaviorSubject<boolean>(false);

  private retryTimer?: ReturnType<typeof setTimeout>;
  private retryStartTime?: number;
  private retryDelayMs = 30000;
  private readonly retryWindowMs = 5 * 60 * 1000;

  backendOffline$ = this.backendOfflineSubject.asObservable();
  llamaOffline$ = this.llamaOfflineSubject.asObservable();
  checking$ = this.checkingSubject.asObservable();

  constructor(private http: HttpClient) {}

  markBackendOffline(): void {
    this.backendOfflineSubject.next(true);
    this.scheduleRetryIfNeeded();
  }

  markBackendOnline(): void {
    this.backendOfflineSubject.next(false);
    this.stopRetryIfOnline();
  }

  markLlamaOffline(): void {
    this.llamaOfflineSubject.next(true);
    this.scheduleRetryIfNeeded();
  }

  markLlamaOnline(): void {
    this.llamaOfflineSubject.next(false);
    this.stopRetryIfOnline();
  }

  retryNow(): void {
    if (this.retryTimer) {
      clearTimeout(this.retryTimer);
      this.retryTimer = undefined;
    }
    this.checkServices();
  }

  checkServices(): void {
    if (this.checkingSubject.value) {
      return;
    }
    this.checkingSubject.next(true);

    const backendUrl = `${environment.backendHost.replace(/\/$/, '')}/api/health`;
    const llamaUrl = `${environment.llamaHost.replace(/\/$/, '')}/v1/models`;

    const backendCheck$ = this.http.get(backendUrl, { observe: 'response' }).pipe(
      timeout(30000),
      map(() => true),
      catchError((error) => of(this.isOnlineFromError(error)))
    );

    const llamaCheck$ = this.http.get(llamaUrl, { observe: 'response' }).pipe(
      timeout(30000),
      map(() => true),
      catchError((error) => of(this.isOnlineFromError(error)))
    );

    forkJoin([backendCheck$, llamaCheck$]).pipe(
      finalize(() => {
        this.checkingSubject.next(false);
        if (this.backendOfflineSubject.value || this.llamaOfflineSubject.value) {
          this.scheduleRetryIfNeeded();
        }
      })
    ).subscribe({
      next: ([backendOnline, llamaOnline]) => {
        if (backendOnline) {
          this.markBackendOnline();
        } else {
          this.markBackendOffline();
        }

        if (llamaOnline) {
          this.markLlamaOnline();
        } else {
          this.markLlamaOffline();
        }
      }
    });
  }

  private scheduleRetryIfNeeded(): void {
    if (this.retryTimer || this.checkingSubject.value) {
      return;
    }
    if (!this.backendOfflineSubject.value && !this.llamaOfflineSubject.value) {
      this.clearRetryState();
      return;
    }

    const now = Date.now();
    if (!this.retryStartTime) {
      this.retryStartTime = now;
    }
    if (now - this.retryStartTime >= this.retryWindowMs) {
      this.clearRetryState();
      return;
    }

    const delay = this.retryDelayMs;
    this.retryTimer = setTimeout(() => {
      this.retryTimer = undefined;
      this.checkServices();
    }, delay);
    this.retryDelayMs = Math.min(this.retryDelayMs * 2, this.retryWindowMs);
  }

  private stopRetryIfOnline(): void {
    if (!this.backendOfflineSubject.value && !this.llamaOfflineSubject.value) {
      this.clearRetryState();
    }
  }

  private clearRetryState(): void {
    if (this.retryTimer) {
      clearTimeout(this.retryTimer);
      this.retryTimer = undefined;
    }
    this.retryStartTime = undefined;
    this.retryDelayMs = 30000;
  }

  private isOnlineFromError(error: unknown): boolean {
    const typedError = error as { status?: number; name?: string };
    if (typedError?.name === 'TimeoutError') {
      return false;
    }
    if (typedError?.status === 0 || typedError?.status === undefined) {
      return false;
    }
    return true;
  }
}
