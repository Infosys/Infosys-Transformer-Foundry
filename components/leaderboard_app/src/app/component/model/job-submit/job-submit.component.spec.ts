import { ComponentFixture, TestBed, async } from "@angular/core/testing";
import { JobSubmitComponent } from "./job-submit.component";
import { RouterTestingModule } from "@angular/router/testing";
import { DatePipe } from "@angular/common";
import { HttpClientModule } from "@angular/common/http";
import { ConfigDataHelper } from "src/app/utils/config-data-helper";
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MessageInfo } from "src/app/utils/message-info";
import { AppMaterialModule } from "src/app/modules/app-material.module";
import { FormsModule } from "@angular/forms";
import { By } from "@angular/platform-browser";

describe('Job submit', () => {
    let component: JobSubmitComponent;
    let fixture: ComponentFixture<JobSubmitComponent>;

    beforeEach( async() => {
        await TestBed.configureTestingModule({
            declarations: [JobSubmitComponent],
            imports: [ RouterTestingModule, BrowserAnimationsModule, HttpClientModule, AppMaterialModule, FormsModule],
            providers: [DatePipe, ConfigDataHelper, MessageInfo],
        }).compileComponents();
    });

    beforeEach(() => {
        fixture = TestBed.createComponent(JobSubmitComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should create component', () => {
        expect(component).toBeTruthy();
    });

    it('should have a modality dropdown', () => {
        let dropdown = fixture.debugElement.query(By.css('modality'));
        expect(dropdown).toBeTruthy();
      });
    
      it('should have the correct options in the modality dropdown', () => {
        component.modality = ['code', 'text', 'embedding'];
        fixture.detectChanges();
    
        let options = fixture.debugElement.queryAll(By.css('modality mat-option'));
        expect(options.length).toBe(3);
        expect(options[0].nativeElement.textContent.trim()).toBe('code');
        expect(options[1].nativeElement.textContent.trim()).toBe('text');
        expect(options[2].nativeElement.textContent.trim()).toBe('embedding');
      });

      it('should have a task dropdown', () => {
        let dropdown = fixture.debugElement.query(By.css('task'));
        expect(dropdown).toBeTruthy();
      });
    
      //test case to check if the arguments section is visible for modality text only
      it('should show the arguments section only for modality text', () => {
        component.modality = ['code'];
        fixture.detectChanges();
      
        let argumentsSection = fixture.debugElement.query(By.css('.modelArgs'));
        expect(argumentsSection.styles['visibility']).toBe('hidden');
      
        component.modality = ['text'];
        fixture.detectChanges();
      
        argumentsSection = fixture.debugElement.query(By.css('.modelArgs'));
        expect(argumentsSection.styles['visibility']).toBe('visible');
      });
});