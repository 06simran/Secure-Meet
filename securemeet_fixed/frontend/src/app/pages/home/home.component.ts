import { Component } from '@angular/core';
@Component({ selector:'app-home', templateUrl:'./home.component.html', styleUrls:['./home.component.scss'] })
export class HomePageComponent {
  features = [
    { icon:'🧠', title:'AI Toxicity Detection',    desc:'NLP model detects toxic, abusive, and hate-speech messages in milliseconds.' },
    { icon:'🚨', title:'Real-Time Alerts',         desc:'Instant moderation warnings delivered to admins and participants.' },
    { icon:'📊', title:'Analytics Dashboard',      desc:'Track moderation history, confidence scores and flagged activity.' },
    { icon:'🔒', title:'JWT Authentication',       desc:'Secure login with role management for admins and regular users.' },
    { icon:'👁️', title:'Behavioral Monitoring',   desc:'Isolation Forest anomaly detection flags suspicious patterns.' },
    { icon:'⚡', title:'Spam Filtering',           desc:'Multi-layer spam and abuse filters protect your meeting chat.' },
  ];
}
