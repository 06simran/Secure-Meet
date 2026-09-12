import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({ providedIn: 'root' })
export class MeetingService {
  private api = environment.apiUrl;
  constructor(private http: HttpClient) {}

  createMeeting(title: string):   Observable<any> { return this.http.post<any>(`${this.api}/meetings/create`, { title }); }
  joinMeeting(code: string):      Observable<any> { return this.http.post<any>(`${this.api}/meetings/join`, { code }); }
  getMyMeetings():                Observable<any> { return this.http.get<any>(`${this.api}/meetings/`); }
  getMeeting(id: number|string):  Observable<any> { return this.http.get<any>(`${this.api}/meetings/${id}`); }
  endMeeting(id: number|string):  Observable<any> { return this.http.post<any>(`${this.api}/meetings/${id}/end`, {}); }
}
