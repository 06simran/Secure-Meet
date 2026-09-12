import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterPageComponent {
  username = '';
  email = '';
  password = '';
  role = 'user';
  loading = false;
  error = '';

  constructor(private auth: AuthService, private router: Router) {}

  register() {
    if (!this.username || !this.email || !this.password) {
      this.error = 'Please fill in all fields.'; return;
    }
    this.loading = true; this.error = '';
    this.auth.register({ username: this.username, email: this.email, password: this.password, role: this.role }).subscribe({
      next: () => this.router.navigate(['/dashboard']),
      error: e => { this.error = e.error?.error || 'Registration failed'; this.loading = false; }
    });
  }
}
