import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ViewDetailed } from './view-detailed';

describe('ViewDetailed', () => {
  let component: ViewDetailed;
  let fixture: ComponentFixture<ViewDetailed>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ViewDetailed]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ViewDetailed);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
