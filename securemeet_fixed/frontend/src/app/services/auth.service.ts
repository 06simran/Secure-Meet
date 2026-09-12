import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, tap } from 'rxjs';
import { Router } from '@angular/router';
import { environment } from '../../environments/environment';

export interface User { id: number; username: string; email: string; role: 'admin'|'user'; violations?: number; }

@Injectable({ providedIn: 'root' })
export class AuthService {
  private apiUrl = environment.apiUrl;
  private _user  = new BehaviorSubject<User|null>(this.loadUser());
  currentUser$   = this._user.asObservable();

  constructor(private http: HttpClient, private router: Router) {}

  private loadUser(): User|null {
    try { return JSON.parse(localStorage.getItem('sm_user') || 'null'); } catch { return null; }
  }
  get currentUser()  { return this._user.value; }
  get token()        { return localStorage.getItem('sm_token'); }
  get isLoggedIn()   { return !!this.token; }
  get isAdmin()      { return this.currentUser?.role === 'admin'; }

  register(data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/auth/register`, data).pipe(tap((r:any) => this.setSession(r)));
  }
  login(email: string, password: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/auth/login`, { email, password }).pipe(tap((r:any) => this.setSession(r)));
  }
  private setSession(res: any) {
    localStorage.setItem('sm_token', res.token);
    localStorage.setItem('sm_user', JSON.stringify(res.user));
    this._user.next(res.user);
  }
  logout() {
    localStorage.removeItem('sm_token');
    localStorage.removeItem('sm_user');
    this._user.next(null);
    this.router.navigate(['/login']);
  }
}
