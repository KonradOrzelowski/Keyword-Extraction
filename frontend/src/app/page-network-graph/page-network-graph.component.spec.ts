import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PageNetworkGraphComponent } from './page-network-graph.component';

describe('PageNetworkGraphComponent', () => {
  let component: PageNetworkGraphComponent;
  let fixture: ComponentFixture<PageNetworkGraphComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PageNetworkGraphComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PageNetworkGraphComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
