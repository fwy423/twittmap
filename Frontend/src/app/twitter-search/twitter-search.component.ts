/**
 * Created by zebinwang on 3/10/17.
 */

import { Component } from '@angular/core';
import { TweetService } from '../tweet.service';
import { tweet } from '../tweet';

@Component({
  selector : 'twitter-search',
  templateUrl : './twitter-search.component.html',
  styleUrls: ['./twitter-search.component.css']
})
export class TwitterSearchComponent {

  lat: number = 40.8075;
  lng: number = -73.9626;
  tweets : tweet = new tweet(
  "They gave me a talk show watch me make noise out my mouth whole!!!\u2026 https://t.co/5xNK7A9HZL",
  [-73.9626, 40.8075],
);

  constructor(
    private tweetservice : TweetService,
  ){}

  title : string = 'Search Tweets'

  keyWords = ['springbreak', 'cloud computing', 'columbia university'];

  async searchTwitter(searchKey : string) : Promise <any> {
    console.log(searchKey);
    try{
      let tweetsresult = await this.tweetservice.searchForTweets(searchKey);
      console.log(tweetsresult);
      this.tweets = tweetsresult;
      // this.showTweet(tweetsresult);
    } catch(ex) {
      console.error('An error occurred', ex);
    }
  }


  // public showTweet(tweets : tweet) {
  //   console.log("showtweets");
  //   console.log(tweets);
  // }

}
