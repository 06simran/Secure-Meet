import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { ModerationService, FlaggedMessage } from '../../services/moderation.service';

@Component({ selector:'app-admin-panel', templateUrl:'./admin-panel.component.html', styleUrls:['./admin-panel.component.scss'] })
export class AdminPanelPageComponent implements OnInit {
  messages: FlaggedMessage[] = []; stats: any = {};
  loading = true; filterAction = 'all'; search = '';

  constructor(private mod: ModerationService, public auth: AuthService, private router: Router) {}

  ngOnInit() {
    if (!this.auth.isAdmin) { this.router.navigate(['/dashboard']); return; }
    this.load();
  }

  load() {
    this.mod.getStats().subscribe({ next: s => this.stats = s, error: () => {} });
    this.mod.getHistory().subscribe({ next: r => { this.messages = r.history || []; this.loading = false; }, error: () => this.loading = false });
  }

  get filtered() {
    return this.messages.filter(m => {
      const okAction = this.filterAction === 'all' || m.action === this.filterAction;
      const okSearch = !this.search || m.message.toLowerCase().includes(this.search.toLowerCase());
      return okAction && okSearch;
    });
  }

  confColor(c: number) { return c > .85 ? '#fc8181' : c > .65 ? '#ed8936' : '#ecc94b'; }
}
