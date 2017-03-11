import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';
import { AgmCoreModule } from 'angular2-google-maps/core';

import { AppComponent } from './app.component';
import { TwitterSearchComponent } from './twitter-search/twitter-search.component';
import { TweetService } from './tweet.service';

@NgModule({
  declarations: [
    AppComponent,
    TwitterSearchComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule,
    AgmCoreModule.forRoot({
      apiKey: 'AIzaSyCAqD75YwMxiLRbopdaD_BpBXqdLHO-aBY'
    })
  ],
  providers: [TweetService],
  bootstrap: [AppComponent]
})
export class AppModule { }
