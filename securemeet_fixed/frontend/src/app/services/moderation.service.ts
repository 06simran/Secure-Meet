import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface ModerationResult { toxic: boolean; confidence: number; labels: string[]; action: string; model?: string; }
export interface FlaggedMessage   { _id: number; user_id: number; meeting_id: number; message: string; toxic: boolean; confidence: number; labels: string[]; action: string; timestamp: string; }

@Injectable({ providedIn: 'root' })
export class ModerationService {
  private api = environment.apiUrl;
  constructor(private http: HttpClient) {}

  predict(message: string, meetingId: any = ''): Observable<ModerationResult> {
    return this.http.post<ModerationResult>(`${this.api}/moderation/predict`, { message, meeting_id: meetingId });
  }
  getFlaggedMessages(meetingId?: number): Observable<any> {
    const q = meetingId ? `?meeting_id=${meetingId}` : '';
    return this.http.get<any>(`${this.api}/moderation/flagged${q}`);
  }
  getHistory():  Observable<any> { return this.http.get<any>(`${this.api}/moderation/history`); }
  getStats():    Observable<any> { return this.http.get<any>(`${this.api}/moderation/stats`); }
}
