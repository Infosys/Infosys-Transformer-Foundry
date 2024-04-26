import { ComponentFixture, TestBed, async } from "@angular/core/testing";
import { CodeLeaderboardComponent } from "./code-leaderboard.component";
import { RouterTestingModule } from "@angular/router/testing";
import { DatePipe } from "@angular/common";
import { HttpClientModule } from "@angular/common/http";
import { ConfigDataHelper } from "src/app/utils/config-data-helper";
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MessageInfo } from "src/app/utils/message-info";
import { NgbPaginationModule } from "@ng-bootstrap/ng-bootstrap";
import { FormsModule } from '@angular/forms';
import { AppMaterialModule } from "src/app/modules/app-material.module";
import { By } from "@angular/platform-browser";

describe('Code Leaderboard', () => {
    let component: CodeLeaderboardComponent;
    let fixture: ComponentFixture<CodeLeaderboardComponent>;

    beforeEach(() => {
        TestBed.configureTestingModule({
            declarations: [CodeLeaderboardComponent],
            imports: [ RouterTestingModule, BrowserAnimationsModule, HttpClientModule, AppMaterialModule, FormsModule, NgbPaginationModule],
            providers: [DatePipe, ConfigDataHelper, MessageInfo],
        }).compileComponents();
    });

    beforeEach(() => {
        fixture = TestBed.createComponent(CodeLeaderboardComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should create component', () => {
        expect(component).toBeTruthy();
    });

        //test case to call the resetFilter on click of reset button
        it('should call the resetFilter method on click of reset button', () => {
            spyOn(component, 'resetFilter');
        
            let button = fixture.debugElement.query(By.css('.icon_Refresh'));
            button.triggerEventHandler('click', null);
        
            expect(component.resetFilter).toHaveBeenCalled();
          });
    
            //test case to call the resetFilter on click of reset button
        it('should call the search method on click of search button', () => {
            spyOn(component, 'onSearchClick');
        
            let button = fixture.debugElement.query(By.css('.search-icon'));
            button.triggerEventHandler('click', null);
        
            expect(component.onSearchClick).toHaveBeenCalled();
          });
    
        it('should call the onSort method on click of sort button', () => {
            spyOn(component, 'updateMetricName');
        
            let button = fixture.debugElement.query(By.css('.sort-icon'));
            button.triggerEventHandler('click', null);
        
            expect(component.updateMetricName).toHaveBeenCalled();
        });
    
        it('should call the onPageChange method when page changes', () => {
            spyOn(component, 'onPageChange');
        
            let pagination = fixture.debugElement.query(By.css('ngb-pagination'));
            pagination.componentInstance.page = 2;  // Change the page
            pagination.componentInstance.pageChange.emit(2);  // Emit the pageChange event
        
            expect(component.onPageChange).toHaveBeenCalledWith(2);
          });

});