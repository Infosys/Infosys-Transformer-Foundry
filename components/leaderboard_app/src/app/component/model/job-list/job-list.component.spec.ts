import 'zone.js/dist/zone-testing';
import { ComponentFixture, TestBed, async } from "@angular/core/testing";
import { JobListComponent } from "./job-list.component";
import { RouterTestingModule } from "@angular/router/testing";
import { DatePipe } from "@angular/common";
import { HttpClientModule } from "@angular/common/http";
import { ConfigDataHelper } from "src/app/utils/config-data-helper";
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MessageInfo } from "src/app/utils/message-info";
import { NgbPaginationModule } from "@ng-bootstrap/ng-bootstrap";
import { FormsModule } from '@angular/forms';
import { AppMaterialModule } from 'src/app/modules/app-material.module';
import { By } from "@angular/platform-browser";

describe('Job list', () => {
    let component: JobListComponent;
    let fixture: ComponentFixture<JobListComponent>;

    beforeEach( async() => {
        await TestBed.configureTestingModule({
            declarations: [JobListComponent],
            imports: [ RouterTestingModule, BrowserAnimationsModule, HttpClientModule, AppMaterialModule, NgbPaginationModule, FormsModule],
            providers: [DatePipe, ConfigDataHelper, MessageInfo],
        }).compileComponents();
    });

    beforeEach(() => {
        fixture = TestBed.createComponent(JobListComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should create component', () => {
        expect(component).toBeTruthy();
    });

    //test case to call the resetFilter on click of reset button
    it('should call the resetFilter method on click of reset button', () => {
        spyOn(component, 'refreshExecutionIDStatus');
    
        let button = fixture.debugElement.query(By.css('.icon_Refresh'));
        button.triggerEventHandler('click', null);
    
        expect(component.refreshExecutionIDStatus).toHaveBeenCalled();
      });

      it('should call the onSort method on click of sort button', () => {
        spyOn(component, 'sortJobs');
    
        let button = fixture.debugElement.query(By.css('.sort-icon'));
        button.triggerEventHandler('click', null);
    
        expect(component.sortJobs).toHaveBeenCalled();
    });
});