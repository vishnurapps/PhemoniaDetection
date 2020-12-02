import { Component } from '@angular/core';
import { NgModule, OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';
import { Observable } from 'rxjs';
import { map, startWith } from 'rxjs/operators';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { analyzeAndValidateNgModules } from '@angular/compiler';
import { HttpParams, HttpHeaders, HttpClient } from '@angular/common/http';
import { element } from 'protractor';
import { areAllEquivalent } from '@angular/compiler/src/output/output_ast';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  searchfile: any;
  filename: any;
  myControl = new FormControl();
  naveena1: string[] = ['One', 'Two', 'Three'];
  jsonsearch: any
  constructor(private http: HttpClient) { }

  naveena: any;
  selectedfile: any;
  selectedsearch: any;

  onselectedsearch(event: string) {

    this.selectedsearch = event;


    this.displaysearch()
  }
  searchname: any
  displaysearch() {

    this.searchname = this.selectedsearch

    // if ((this.searchname == 'one')) {
    //   this.naveena = [
    //     {
    //       "id": '1',
    //       "name": 'naveena',
    //       "address": "andhrapradesh",
    //       "bio": "age :23",
    //       "image": "assets/images/mri.jpg",
    //       "scantype": "mri",
    //       "result": "pass",
    //       "interpretation": "none"

    //     }
    //   ];

    // }
    // else {

    //   this.naveena = [{
    //     "id": '2',
    //     "name": 'chinni',
    //     "address": "andhrapradesh",
    //     "bio": "age :22",
    //     "image": "assets/images/naveenaimg.jpg",
    //     "scantype": "heart",
    //     "result": "pass",
    //     "interpretation": "none"
    //   }

    //   ];

    // }



    let studyParams = new HttpParams();
    studyParams = studyParams.append("patientId", this.searchname)
    let header = new HttpHeaders();
    header.append('Content-type', 'application/json');
    console.log("***Get Study", this.searchname);
    return this.http.get("http://localhost:4500/getStudy", { headers: header, params: studyParams }).subscribe((response: any) => {

      if (response && response.length > 0) {

        response.forEach((element: { name: any; address: any; bio: any; image: any; scantype: any; result: any; interpretation: any; }) => {
          this.naveena.push({

            "name": element.name,
            "address": element.address,
            "bio": element.bio,
            "image": element.image,
            "scantype": element.scantype,
            "result": element.result,
            "interpretation": element.interpretation

          })
        });


      }

    })
  }

  displayfile() {

    // this.naveena = [
    //   {
    //     "id": '2',
    //     "name": 'naveena',
    //     "address": "andhrapradesh",
    //     "bio": "age :23",
    //     "image": "assets/images/naveenai.jpg",
    //     "scantype": "mri",
    //     "result": "pass",
    //     "interpretation": "none"

    //   }
    // ];
    let header = new HttpHeaders();
    let params1 = new HttpParams();
    header.append('Content-type', 'application/json');
    console.log("Study : ", this.selectedfile)


    this.http.post("http://127.0.0.1:5000/sendimage", this.selectedfile, { headers: header })
      .subscribe((result) => {
        console.warn("result", result)
      })


    this.sleep(10000).then(() => {  

      console.log("naveena")
    return this.http.get("http://127.0.0.1:5000/search", { headers: header }).subscribe((response: any) => {

      if (response && response.length > 0) {

        response.forEach((element: { name: any; address: any; bio: any; image: any; scantype: any; result: any; interpretation: any; }) => {
          this.naveena.push({

            "name": element.name,
            "address": element.address,
            "bio": element.bio,
            "image": element.image,
            "scantype": element.scantype,
            "result": element.result,
            "interpretation": element.interpretation

          })
        });
     


      }

    })
  });
  }
  onselectedfile(event: any) {
    this.selectedfile = event.target.files[0];


  }
   sleep(ms: number) {
     alert("naveena")
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}


