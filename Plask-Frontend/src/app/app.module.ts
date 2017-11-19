//Import Basic Modules
import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';
import { XSRFStrategy, CookieXSRFStrategy } from '@angular/http';

//Import Components
import { AppComponent } from './app.component';
import { SignInComponent } from './signin.component';
import { SignUpComponent } from './signup.component';
import { MainComponent } from './main.component';
import { SettingsComponent } from './settings.component';
import { MainTabComponent } from './maintab.component';

//Import Service
import { UserService } from './user.service';
import { LocationService } from './location.service';

import { AppRoutingModule } from './app-routing.module';

import { APP_BASE_HREF } from '@angular/common';

import { Ng2AutoCompleteModule } from 'ng2-auto-complete';


@NgModule({
    declarations: [
        AppComponent,
        SignInComponent,
        SignUpComponent,
        MainComponent,
        SettingsComponent,
        MainTabComponent,
    ],
    imports: [
        BrowserModule,
        FormsModule,
        HttpModule,
        AppRoutingModule,
        Ng2AutoCompleteModule,
    ],
    providers: [
        UserService,
        LocationService,
        { provide: APP_BASE_HREF, useValue: '/' },
        { provide: XSRFStrategy, useFactory: cookieStrategy},

    ],
    bootstrap: [AppComponent]
})
export class AppModule { }

export function cookieStrategy(){
    return new CookieXSRFStrategy('csrftoken', 'X-CSRFToken');
    //return new CookieXSRFStrategy('_csrf', 'XSRF-TOKEN');
}