
/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/
 import { HttpClient, HttpHeaders,HttpErrorResponse ,HttpParams} from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable ,throwError} from 'rxjs';
import { catchError } from 'rxjs/operators';
import { ConfigDataHelper } from '../utils/config-data-helper';
import { CONSTANTS } from '../common/constants';
import { DataStorageService } from './data-storage.service';

@Injectable({
  providedIn: 'root'
})
export class DatasetService {
  private datasetUrl = 'http://localhost:8089/api/v1/datasets';

  private deleteUrl="http://localhost:8089/api/v1/datasets/datasetId";

  // private datasetUrl='http://localhost:8089/api/v1/datasets/docs#/';

  constructor(private http: HttpClient,public configDataHelper: ConfigDataHelper, private storageService: DataStorageService) { }

  
  register(userId:any): Observable<any> {
    const parent = this;
    const headerDict = {
      'Accept': 'application/json',
      'userId': parent.storageService.getData().userId,
      'Content-Type': 'application/json',
    }
    const requestOptions = {
      headers: new HttpHeaders(headerDict),
    };
    const url = parent.configDataHelper.getValue(CONSTANTS.CONFIG.PL_MGMT_SERVICE_BASER_URL_V1) +
      CONSTANTS.APIS.JOB_MGMT_SERVICE.POST_TRAIL_DATA;

    return this.http.post<any>(this.datasetUrl, userId, requestOptions)
      .pipe(
        catchError(this.handleError)
      );
  }

  private handleError(error: HttpErrorResponse) {
    console.log('An error occured',error.error.message);
    return throwError('Error! something went wrong please try again later.');
  }


 
  getData(projectId:string): Observable<any> {
    const parent = this;
    const headerDict = {
      'Accept': 'application/json',
      'userId': parent.storageService.getData().userId,
      'Content-Type': 'application/json',
    }
   
      const headers= new HttpHeaders(headerDict);
     const params = new HttpParams().set('projectId', projectId);
    const options={headers,params};
    console.log("options",options);
    return this.http.get<any>(this.datasetUrl,options)
      .pipe(
        catchError(this.handleError)
      );
  }

  deleteDataset(datasetId: string, userId: string): Observable<any> {
    // Define the headers with user ID
    const parent = this;
    const headerDict = {
      'Accept': 'application/json',
      'userId': parent.storageService.getData().userId,
      'Content-Type': 'application/json',
    }
   
      const headers= new HttpHeaders(headerDict);

    // Define the options with headers and query parameters
    const options = {
      headers: headers,
      params: { datasetId: datasetId }
    };
    // const url = `${this.datasetUrl}/dataset/${datasetId}`;

    // Send the DELETE request
    return this.http.delete(this.deleteUrl, options);
  }

  
  getDatasetById(datasetId: string): Observable<any> {
    const parent = this;
    const headerDict = {
      'Accept': 'application/json',
      'userId': parent.storageService.getData().userId,
      'Content-Type': 'application/json',
    }
   
      const headers= new HttpHeaders(headerDict);
      const options = {
        headers: headers,
        params: { datasetId: datasetId }
      };
      
  
      // Send the DELETE request
      return this.http.get(this.deleteUrl, options);

  }

  

  updateDataset(datasetId: string,data:any): Observable<any> {
    const parent = this;
    const headerDict = {
      'Accept': 'application/json',
      'userId': parent.storageService.getData().userId,
      'Content-Type': 'application/json',
    }
   
      const headers= new HttpHeaders(headerDict);
      const options = {
        headers: headers,
        params: { datasetId: datasetId }
      };
      const url=`${this.deleteUrl}`;
  
      // Send the DELETE request
      return this.http.patch(url, data,options);

  }

}

