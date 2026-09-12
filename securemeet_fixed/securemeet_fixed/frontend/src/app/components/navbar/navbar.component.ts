import { Component, OnInit } from '@angular/core';
import { AuthService, User } from '../../services/auth.service';
@Component({ selector:'app-navbar', templateUrl:'./navbar.component.html', styleUrls:['./navbar.component.scss'] })
export class NavbarComponent implements OnInit {
  user: User|null = null; menuOpen = false;
  constructor(public auth: AuthService) {}
  ngOnInit() { this.auth.currentUser$.subscribe(u => this.user = u); }
  logout() { this.auth.logout(); }
  toggleMenu() { this.menuOpen = !this.menuOpen; }
}
