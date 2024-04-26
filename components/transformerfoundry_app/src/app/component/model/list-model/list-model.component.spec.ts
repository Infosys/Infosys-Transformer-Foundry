import { ComponentFixture, TestBed } from "@angular/core/testing";
import { RouterTestingModule } from "@angular/router/testing";
import { DatePipe } from "@angular/common";
import { HttpClientModule } from "@angular/common/http";
import { ConfigDataHelper } from "src/app/utils/config-data-helper";
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatFormFieldModule } from "@angular/material/form-field";
import { ListModelComponent } from "./list-model.component";
import { Router } from "@angular/router";
import { By } from '@angular/platform-browser';

describe('Models list', () => {
    let component: ListModelComponent;
    let fixture: ComponentFixture<ListModelComponent>;
    let router: Router;
    beforeEach( async() => {
        await TestBed.configureTestingModule({
            declarations: [ListModelComponent],
            imports: [ RouterTestingModule, BrowserAnimationsModule, HttpClientModule, MatFormFieldModule],
            providers: [DatePipe, ConfigDataHelper],
        }).compileComponents();
    });

    beforeEach(() => {
        fixture = TestBed.createComponent(ListModelComponent);
        component = fixture.componentInstance;
        router = TestBed.inject(Router);
        fixture.detectChanges();
    });

    //test case to check if the component is created.
    it('should create list model component', () => {
        expect(component).toBeTruthy();
    });

    //test case to check if the model card visible
    it('should have model cards', () => {
        const element = fixture.debugElement.queryAll(By.css('mat-card'));
        expect(element).toBeTruthy();
    });

    //test case to check if it contains the Fine tune and Deploy buttons
    it('should check if the buttons are visible', () => {
        fixture.detectChanges();
        const buttonElement = fixture.debugElement.queryAll(By.css('mat-button'));
        expect(buttonElement).toBeTruthy();
      });

});