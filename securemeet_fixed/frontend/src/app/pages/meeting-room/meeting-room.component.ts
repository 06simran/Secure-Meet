import { Component, OnInit, OnDestroy } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { ModerationService, ModerationResult } from '../../services/moderation.service';
import { MeetingService } from '../../services/meeting.service';

interface ChatMsg { id:number; user:string; text:string; time:Date; mod?:ModerationResult; }

@Component({ selector:'app-meeting-room', templateUrl:'./meeting-room.component.html', styleUrls:['./meeting-room.component.scss'] })
export class MeetingRoomPageComponent implements OnInit, OnDestroy {
  meeting: any = null; messages: ChatMsg[] = [];
  newMessage = ''; alert: ModerationResult|null = null;
  loading = true; alertTimer: any; msgId = 0;
  participants = [{ name:'You', online:true }, { name:'Alice', online:true }, { name:'Bob', online:false }];

  constructor(private route: ActivatedRoute, private meetSvc: MeetingService,
              private modSvc: ModerationService, public auth: AuthService) {}

  ngOnInit() {
    const id = this.route.snapshot.paramMap.get('id')!;
    this.meetSvc.getMeeting(id).subscribe({ next: r => { this.meeting=r.meeting; this.loading=false; }, error: ()=>this.loading=false });
    this.messages.push({ id:this.msgId++, user:'🤖 SecureMeet', text:'Welcome! AI moderation is active for this meeting.', time:new Date() });
  }
  ngOnDestroy() { if(this.alertTimer) clearTimeout(this.alertTimer); }

  send() {
    const text = this.newMessage.trim();
    if(!text) return;
    this.newMessage = '';
    const msg: ChatMsg = { id:this.msgId++, user:this.auth.currentUser?.username||'You', text, time:new Date() };
    this.modSvc.predict(text, this.meeting?._id||'').subscribe({
      next: r => {
        msg.mod = r;
        if(r.action !== 'ban') this.messages.push(msg);
        if(r.toxic) { this.alert=r; if(this.alertTimer) clearTimeout(this.alertTimer); this.alertTimer=setTimeout(()=>this.alert=null,5000); }
      },
      error: ()=>this.messages.push(msg),
    });
  }

  onKey(e: KeyboardEvent) { if(e.key==='Enter' && !e.shiftKey){ e.preventDefault(); this.send(); } }
  dismissAlert() { this.alert=null; }
}
