import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { ModerationService } from '../../services/moderation.service';
import { MeetingService } from '../../services/meeting.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardPageComponent implements OnInit {
  stats: any = {};
  meetings: any[] = [];
  flagged: any[] = [];
  loading = true;
  showCreate = false;
  showJoin = false;
  newTitle = '';
  joinCode = '';
  createError = '';
  joinError = '';

  constructor(
    public auth: AuthService,
    private mod: ModerationService,
    private meet: MeetingService,
    private router: Router
  ) {}

  ngOnInit() { this.loadAll(); }

  loadAll() {
    this.loading = true;
    this.mod.getStats().subscribe({ next: s => this.stats = s, error: () => {} });
    this.meet.getMyMeetings().subscribe({ next: r => this.meetings = r.meetings || [], error: () => {} });
    this.mod.getFlaggedMessages().subscribe({
      next: r => {
        this.flagged = (r.flagged_messages || []).slice(0, 5);
        this.loading = false;
      },
      error: () => this.loading = false,
    });
  }

  goToMeeting(m: any) {
    this.router.navigate(['/meeting', m._id]);
  }

  createMeeting() {
    if (!this.newTitle.trim()) return;
    this.createError = '';
    this.meet.createMeeting(this.newTitle.trim()).subscribe({
      next: r => {
        this.newTitle = '';
        this.showCreate = false;
        this.loadAll();
        this.router.navigate(['/meeting', r.meeting._id]);
      },
      error: e => this.createError = e.error?.error || 'Failed to create meeting',
    });
  }

  joinMeeting() {
    if (!this.joinCode.trim()) return;
    this.joinError = '';
    this.meet.joinMeeting(this.joinCode.trim().toUpperCase()).subscribe({
      next: r => {
        this.joinCode = '';
        this.showJoin = false;
        this.router.navigate(['/meeting', r.meeting._id || r.meeting.id]);
      },
      error: () => this.joinError = 'Meeting not found. Check the code.',
    });
  }
}
