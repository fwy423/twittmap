/**
 * Created by zebinwang on 3/10/17.
 */
import { Injectable } from '@angular/core';
import { Headers, RequestOptions, Http } from '@angular/http';
import 'rxjs/add/operator/toPromise';
import {tweet_Response_1} from './mock-data/mock-tweet';

@Injectable()
export class TweetService {

  private url = '';

  async  searchForTweets(KeyWord : string): Promise<any> {
    let headers = new Headers({'Content-Type': 'application/json'});
    let options = new RequestOptions({ headers: headers });

    try {
      //let res = await this.http.post(this.url, { KeyWord : KeyWord }, options).toPromise();
      //console.log(res.json());
      //return res.json();
      console.log(KeyWord);
      return tweet_Response_1;
    } catch (ex) {
      this.handleError(ex);
    }
  }

  private handleError(error: any): Promise<any> {
    console.error('An error occurred', error); // for demo purposes only
    return Promise.reject(error.message || error);
  }

  constructor (private http: Http) {}

}
