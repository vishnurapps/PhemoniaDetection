import { Component } from '@angular/core';
import { NgModule, OnInit } from '@angular/core';
import {FormControl} from '@angular/forms';
import {Observable} from 'rxjs';
import {map, startWith} from 'rxjs/operators';
import {MatAutocompleteModule} from '@angular/material/autocomplete';
import { analyzeAndValidateNgModules } from '@angular/compiler';
import { HttpParams, HttpHeaders, HttpClient } from '@angular/common/http';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent   {
 
  // constructor(private http: HttpClient){}
  myControl = new FormControl();
// options: string[] = ['One', 'Two', 'Three'];


naveena: any[]=[
  {
    "id" :'1',
    "file" : 'assets/dicomfiels/dicomfile1.pdf'

  },
  {
    "id" :'2',
    "file" : 'assets/dicomfiels/dicomfile2.pdf'
  }
];

displaySeries(id: any,file: any){
  
  alert(id);
  alert(file);

//   this.http.get(file).subscribe(data => {
//     console.log(data);
// })
}
}
