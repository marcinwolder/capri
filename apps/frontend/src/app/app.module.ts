import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { CityComponent } from './screens/selection/city/city.component';
import { TimeComponent } from './screens/selection/time/time.component';
import {FormsModule} from "@angular/forms";
import { NextFooterComponent } from './components/next-footer/next-footer.component';
import { SelectionComponent } from './screens/selection/selection.component';
import { DetailsComponent } from './screens/selection/preferences/details/details.component';
import { TripComponent } from './screens/trip/trip.component';
import { SignupComponent } from './screens/signup/signup.component';
import { SigninComponent } from './screens/signin/signin.component';
import { NavbarComponent } from './components/navbar/navbar.component';
import { ErrorBoxComponent } from './components/error-box/error-box.component';
import { HomeComponent } from './screens/home/home.component';
import { ProfileComponent } from './screens/profile/profile.component';
import {NgOptimizedImage} from "@angular/common";
import {HttpClientModule} from "@angular/common/http";
import { LoadingComponent } from './screens/loading/loading.component';
import { SpinnerComponent } from './components/spinner/spinner.component';
import { MapComponent } from './components/map/map.component';
import { BackgroundComponent } from './components/background/background.component';
import { DatePickerComponent } from './components/date-picker/date-picker.component';
import { TextNoteComponent } from './screens/selection/preferences/text-note/text-note.component';
import { ChatComponent } from './screens/selection/preferences/chat/chat.component';
import { SocialMediaComponent } from './screens/selection/preferences/social-media/social-media.component';
import { RatingComponent } from './components/rating/rating.component';
import { TransportationComponent } from './components/transportation/transportation.component';
import { LoadingChecklistComponent } from './components/loading-checklist/loading-checklist.component';

@NgModule({
  declarations: [
    AppComponent,
    CityComponent,
    TimeComponent,
    NextFooterComponent,
    SelectionComponent,
    DetailsComponent,
    TripComponent,
    SignupComponent,
    SigninComponent,
    NavbarComponent,
    ErrorBoxComponent,
    HomeComponent,
    ProfileComponent,
    LoadingComponent,
    SpinnerComponent,
    MapComponent,
    BackgroundComponent,
    DatePickerComponent,
    TextNoteComponent,
    ChatComponent,
    SocialMediaComponent,
    RatingComponent,
    TransportationComponent,
    LoadingChecklistComponent,
  ],
    imports: [
        BrowserModule,
        AppRoutingModule,
        FormsModule,
        NgOptimizedImage,
        HttpClientModule,
    ],
  providers: [

  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
