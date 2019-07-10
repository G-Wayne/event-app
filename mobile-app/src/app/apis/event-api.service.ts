import { Injectable } from '@angular/core';
// This is needed for http requests
import { HttpClient, HttpHeaders, HttpErrorResponse } from '@angular/common/http';
// design pattern
import { Observable, of, throwError } from 'rxjs';
import { catchError, tap, map } from 'rxjs/operators';
import { Event } from '../event';
import { Review } from '../review';

const httpOptions = {
  headers: new HttpHeaders({'Content-Type': 'application/json'})
  
};

 
//const endpointUrl = "http://172.16.208.82:5000/events";
  const endpointUrl = "http://127.0.0.1:5000/events";
  // const feedbackUrl = "http://127.0.0.1:5000/events";


@Injectable({
  providedIn: 'root'
})
// configured to access two methods for getTasks (using GET) and addTask
//(using POST)
export class EventApiService {
  //endpointUrl = "http://172.16.208.82:5000/events"; // <<--Your URL goes here
  endpointUrl = "http://127.0.0.1:5000/events"; // <<--Your URL goes here
  //endpoint = "http://127.0.0.1:5000/events/";

  //initialize constructor with class variable above
  constructor(private http: HttpClient) { }

  private handleError<T> (operation = 'operation', result?:T){
    return (error: any): Observable<T> => {
      //send the error to the remote logging infrastructure
      console.error(error);//log to console instead
      
      //Let the app keep running by returning an empty result.
      return of(result as T);
    };
  }

  // the methods for your API go below here -->>
 
  //GET
  getEvents(): Observable<any>
  {
    return this.http.get(`${this.endpointUrl}`).pipe(map(results => results['event']));// return array from json file object

  }

  searchData(name: string): Observable<any> {
    return this.http.get(`${this.endpointUrl}/s=${encodeURI(name)}`).pipe(
      map(results => {
        console.log('RAW: ', results['event']);
        return results['event']
      }),catchError(this.handleError<any>(`searchData name=${name}`))
      );// return array from json file object
 
  }


  getDetails(id){
    return this.http.get(`${this.endpointUrl}/details/${id}`);

  }

  //POST
  addEvent(data)
  {
    return this.http.post(`${this.endpointUrl}`,data);
  }

  //PUT
  updateEvent(id, event):Observable<any> {
    return this.http.put(`${this.endpointUrl}/${id}`, event, httpOptions).pipe(tap(_ => console.log(`updated event id=${id}`)),
    catchError(this.handleError<any>('updateEvent'))
    );

  }

//Reviews
  getReviews(id){
    return this.http.get(`${this.endpointUrl}/feedback/${id}`).pipe(map(results => results['feedback']));;

  }


  addReview (review): Observable<Review> {
    return this.http.post<Review>(endpointUrl, review, httpOptions).pipe(
      tap((review: Review) => console.log(`added review w/ id=${review.id}`)),
      catchError(this.handleError<Review>('addReview'))
    );
  }

}
