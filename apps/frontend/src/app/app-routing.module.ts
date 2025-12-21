import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {CityComponent} from "./screens/selection/city/city.component";
import {TimeComponent} from "./screens/selection/time/time.component";
import {SelectionComponent} from "./screens/selection/selection.component";
import {DetailsComponent} from "./screens/selection/preferences/details/details.component";
import {TripComponent} from "./screens/trip/trip.component";
import {HomeComponent} from "./screens/home/home.component";
import {HistoryComponent} from "./screens/history/history.component";
import {TextNoteComponent} from "./screens/selection/preferences/text-note/text-note.component";
import {ChatComponent} from "./screens/selection/preferences/chat/chat.component";
import {SocialMediaComponent} from "./screens/selection/preferences/social-media/social-media.component";

const routes: Routes = [
  {
    path: 'selection', component: SelectionComponent,
    children: [
      {path: '', component: CityComponent},
      {path: 'time', component: TimeComponent},
      {path: 'details', component: DetailsComponent},
      {path: 'text-note', component: TextNoteComponent},
      {path: 'chat', component: ChatComponent},
      {path: 'social-media', component: SocialMediaComponent}
    ]
  },
  {path: 'trip', component: TripComponent},
  {path: 'history', component: HistoryComponent},
  {path: 'home', component: HomeComponent},
  {path: '', redirectTo: '/home', pathMatch: 'full'},
  {path: '**', component: HomeComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {
}
