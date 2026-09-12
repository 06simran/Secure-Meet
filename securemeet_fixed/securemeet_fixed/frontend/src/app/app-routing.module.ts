import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomePageComponent } from './pages/home/home.component';
import { LoginPageComponent } from './pages/login/login.component';
import { RegisterPageComponent } from './pages/register/register.component';
import { DashboardPageComponent } from './pages/dashboard/dashboard.component';
import { MeetingRoomPageComponent } from './pages/meeting-room/meeting-room.component';
import { AdminPanelPageComponent } from './pages/admin-panel/admin-panel.component';
import { AuthGuard } from './guards/auth.guard';

const routes: Routes = [
  { path: '',           component: HomePageComponent },
  { path: 'login',      component: LoginPageComponent },
  { path: 'register',   component: RegisterPageComponent },
  { path: 'dashboard',  component: DashboardPageComponent,  canActivate: [AuthGuard] },
  { path: 'meeting/:id',component: MeetingRoomPageComponent,canActivate: [AuthGuard] },
  { path: 'admin',      component: AdminPanelPageComponent, canActivate: [AuthGuard] },
  { path: '**',         redirectTo: '' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
