import { Component, OnInit } from '@angular/core';
import { LoadingController, AlertController } from '@ionic/angular';
import { EventApiService } from './../../../apis/event-api.service';
import { ActivatedRoute, Router } from '@angular/router';
import { FormControl, FormGroupDirective, FormBuilder, FormGroup, NgForm, Validators } from '@angular/forms';
import { Observable } from 'rxjs';
import { Event } from '../../../event';

@Component({
  selector: 'app-update',
  templateUrl: './update.page.html',
  styleUrls: ['./update.page.scss'],
})
export class UpdatePage implements OnInit {
  results: Observable<any>;
  res: Observable<any>;

  eventForm: FormGroup;
  _id:any='';
  title:string='';
  name:string='';
  //public_name:string='';
  description:string='';
  category:string='';
  start_date:string='';
  start_time:string='';
  end_date:string='';
  end_time:string='';
  //flyer:string;
  cost:number=null;
  venue:string='';
  //visible:string='';
  //creator:number=null;

  constructor(private eventApiService: EventApiService, private loadingController: LoadingController, private alertController: AlertController, private route: ActivatedRoute, private router: Router, private formBuilder: FormBuilder) { }


  ngOnInit() {
    this.getDe(this.route.snapshot.params['id']);
    this.eventForm = this.formBuilder.group({
      'title' : [null,Validators.required],
      'name' : [null,Validators.required],
      //'public_name' : [null,Validators.required],
      'description' : [null,Validators.required],
      'category' : [null,Validators.required],
      'start_date' : [null,Validators.required],
      'start_time' : [null,Validators.required],
      'end_date' : [null,Validators.required],
      'end_time' : [null,Validators.required],
      //'flyer' : [null,Validators.required],
      'cost' : [null,Validators.required],
      'venue' : [null,Validators.required],
      'visible' : [null,Validators.required],
      //'creator' : [null,Validators.required],

    })
  }

  async getDe(id) {
    const loading = await this.loadingController.create({
      message: 'Loading...'
    });
    await loading.present();
    await this.eventApiService.getDetails(id)
    .subscribe(results => {
      this._id = results['event'].id;
      this.eventForm.setValue({
        title:results['event'].title,
        name:results['event'].name,
        //public_name:results['event'].public_name,
        description:results['event'].description,
        category:results['event'].category,
        start_date:results['event'].start_date,
        start_time:results['event'].start_time,
        end_date:results['event'].end_date,
        end_time:results['event'].end_time,
        //flyer:results['event'].flyer,
        cost:results['event'].cost,
        venue:results['event'].venue,
        visible:results['event'].visible,
        //creator:results['event'].creator,
      });
      console.log(results);
      loading.dismiss();
    },err => {
      console.log(err);
      loading.dismiss();
    });
  }

  async onFormSubmit(form:NgForm){
    await this.eventApiService.updateEvent(this._id, form)
    .subscribe(res => {//res is from json in api
      //let id = this.route.snapshot.params['id'];
        let id = this._id;
        // return to list of events
        this.router.navigate(['/list'])
        //this.router.navigate(['/details/'+`${id}`])
       console.log(this._id);

    }, (err) => {
      console.log(err);
    });
  }

  async presentAlertConfirm(msg: string){
    const alert = await this.alertController.create({
      header: 'Warning!',
      message: msg,
      buttons: [
        {
          text: 'Okay',
          handler: () => {
            this.router.navigate(['']);

          }
        }
      ]
    });
    await alert.present();
  }
    
  }


