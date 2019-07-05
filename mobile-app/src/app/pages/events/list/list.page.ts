import { Component, OnInit } from '@angular/core';

//Import API Service here
//Access app directory level then apis folder
import { EventApiService } from './../../../apis/event-api.service';

//A class that allows us to access the data coming
// our web service asynchronously
import { Observable } from 'rxjs';

@Component({
  selector: 'app-list',
  templateUrl: './list.page.html',
  styleUrls: ['./list.page.scss'],
})
export class ListPage implements OnInit {

  results: Observable<any>;

  // added eventAPiService to the constructor so that it automaically recieves
  // a copy of an instance (i.e "dependency injection") which is something ionic
  // does for us hence no need to worry about it
  constructor(private eventApiService: EventApiService) {
    // call getEvents() and store in results: Observable<any> class variable 
    // which is accesible on the page
    this.results = this.eventApiService.getEvents();

    // This is how we would invoke the add method
     this.eventApiService.addEvent({description: "hello world!"});

   }

  ngOnInit() {
  }

}
