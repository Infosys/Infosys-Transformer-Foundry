import { ComponentFixture, TestBed, async, fakeAsync, tick } from "@angular/core/testing";
import { ModelHomeComponent } from "./model-home.component";
import { RouterTestingModule } from "@angular/router/testing";
import { DatePipe } from "@angular/common";
import { HttpClientModule } from "@angular/common/http";
import { ConfigDataHelper } from "src/app/utils/config-data-helper";
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatFormFieldModule } from "@angular/material/form-field";
import { ModelService } from "src/app/services/models.service";

describe('Models home', () => {
    let component: ModelHomeComponent;
    let fixture: ComponentFixture<ModelHomeComponent>;

    beforeEach( async() => {
        await TestBed.configureTestingModule({
            declarations: [ModelHomeComponent],
            imports: [ RouterTestingModule, BrowserAnimationsModule, HttpClientModule, MatFormFieldModule],
            providers: [DatePipe, ConfigDataHelper, ModelService],
        }).compileComponents();
    });

    beforeEach(() => {
        fixture = TestBed.createComponent(ModelHomeComponent);
        component = fixture.componentInstance;
        spyOn(component, 'checkIfModelZoo').and.returnValue(true);
        fixture.detectChanges();
    });

    //to check if the component is created
    it('should create home component', () => {
        expect(component).toBeTruthy();
    });

     //to check if it contains models tab
     it('should contain Models tab', () => {
        component.model.isDataLoaded = true;
        fixture.detectChanges();
        const compiled = fixture.nativeElement;
        const tabName = compiled.querySelector('mat-tab-group mat-tab').getAttribute('label');
        expect(tabName).toBe('Models');
    });

    //to check if it contains leaderboard tab
    it('should contain leaderboard tab', fakeAsync(() => {
        component.model.isDataLoaded = true;
        tick();
        fixture.detectChanges();
        const compiled = fixture.nativeElement;
        expect(compiled.innerHTML).toContain('Leaderboard');
    }));

});