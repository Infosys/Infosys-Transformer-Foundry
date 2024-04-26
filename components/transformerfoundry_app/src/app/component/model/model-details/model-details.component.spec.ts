import { ComponentFixture, TestBed } from "@angular/core/testing";
import { RouterTestingModule } from "@angular/router/testing";
import { DatePipe } from "@angular/common";
import { HttpClientModule } from "@angular/common/http";
import { ConfigDataHelper } from "src/app/utils/config-data-helper";
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatFormFieldModule } from "@angular/material/form-field";
import { ModelDetailsComponent } from "./model-details.component";
import { By } from '@angular/platform-browser';

describe('Model Details', () => {
    let component: ModelDetailsComponent;
    let fixture: ComponentFixture<ModelDetailsComponent>;

    beforeEach( async() => {
        await TestBed.configureTestingModule({
            declarations: [ModelDetailsComponent],
            imports: [ RouterTestingModule, BrowserAnimationsModule, HttpClientModule, MatFormFieldModule],
            providers: [DatePipe, ConfigDataHelper],
        }).compileComponents();
    });

    beforeEach(() => {
        fixture = TestBed.createComponent(ModelDetailsComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    //test case to check if the component is created.
    it('should create list model component', () => {
        expect(component).toBeTruthy();
    });

    //to check if it contains the metadata and benchmarks tab
    it('should have 2 tabs with labels "Metadata" and "Benchmarks"', () => {
        fixture.whenStable().then(() => { 
            fixture.detectChanges();
            const tabGroupDebugElement = fixture.debugElement.query(By.css('mat-tab-group'));
            const tabDebugElements = tabGroupDebugElement.queryAll(By.css('mat-tab'));
            const tabLabels = tabDebugElements.map(de => de.nativeElement.textContent.trim());
            
            expect(tabLabels.length).toBe(2);
            expect(tabLabels).toContain('Metadata');
            expect(tabLabels).toContain('Benchmarks');
        });
      });

});