import { Injectable } from '@angular/core';
// This is needed for http requests
import { HttpClient } from '@angular/common/http';
// design pattern
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
// configured to access two methods for getTasks (using GET) and addTask
//(using POST)
export class EventApiService {
  endpointUrl = "http://172.16.168.229:5000/events"; // <<--Your URL goes here


  //initialize constructor with class variable above
  constructor(private http: HttpClient) { }

  // the methods for your API go below here -->>
 
  //GET
  getEvents(): Observable<any>
  {
    return this.http.get(`${this.endpointUrl}`).pipe(map(results => results['event']));// return array from json file object

  }

  //POST
  addEvent(data)
  {
    return this.http.post(`${this.endpointUrl}`,data);
  }
}
