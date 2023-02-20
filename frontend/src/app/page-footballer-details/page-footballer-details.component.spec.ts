import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PageFootballerDetailsComponent } from './page-footballer-details.component';

describe('PageFootballerDetailsComponent', () => {
  let component: PageFootballerDetailsComponent;
  let fixture: ComponentFixture<PageFootballerDetailsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PageFootballerDetailsComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PageFootballerDetailsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
