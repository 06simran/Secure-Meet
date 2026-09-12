import { Component, Input, Output, EventEmitter } from '@angular/core';
import { ModerationResult } from '../../services/moderation.service';
@Component({ selector:'app-moderation-alert', templateUrl:'./moderation-alert.component.html', styleUrls:['./moderation-alert.component.scss'] })
export class ModerationAlertComponent {
  @Input() result!: ModerationResult;
  @Output() dismissed = new EventEmitter<void>();
  get icon() { return this.result?.action==='ban'?'🚫':this.result?.action==='mute'?'🔇':this.result?.action==='filter'?'📛':'⚠️'; }
  get cls()  { return `sev-${this.result?.action}`; }
  dismiss()  { this.dismissed.emit(); }
}
