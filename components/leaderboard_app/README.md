# MFE-TF-Leaderboard Application

## Steps to Integrate MFE Application with Parent Application

To Integrate MFE Application with a Parent Application we are making use **@angular/elemenets**. 
This package is used to convert the Angular Application into a Custom Element. This Custom Element can be used in any other application.

### Step 1: Create a new angular project and install the necessary dependencies according to the angular version.
````
@angular-extensions/elements
ngx-build-plus
webpack-merge
@angular/elements
jquery
bootstrap
http-server
````

### Step 2: Add/Change the necessary configurations in the required files.

#### 1. Replace **@angular-devkit/build-angular** with **ngx-build-plus**(4 places) in angular.json file

#### 2. Change the below two scripts in your **package.json**

````
"build": "ng build --output-hashing none && node {{concatenated file}}.js"
````
--output-hashing none : This is used to remove hashing in the dist files names when the application is built.

node concat.js: This is used to concatanet the dist files into a single file.

````
"start": "npm run build && http-server ./{{Dist Folder}}/ -p {{PortNumber}}"
````
http-server: ./{{Dist Folder}}/ -p {{PortNumber}}: This is used to run the application in a server on the given port number.

#### 3. Check if the project has a **polyfills.ts** in src folder. 
If not create a new file with the same name and add the below import statement in it.
````
import 'zone.js'
````
Also add **"src/polyfills.ts"** in the **tsconfig.app.json** under files array.

### Step 3: Create a new file concat.js in the root folder of the application.

This file is used to concatenaet the dist folder files generated after the application in built into a single file.

The required files that we should concatenate are:
````
runtime.js
polyfills.js
main.js
````
The order of these files should be the same as given in index.html file in dist folder
The path and name of the concatenated file should also be mentioned in the file.

### Step 4: Create a custom element for passing to the parent application.
In the **app.module.ts** file import the below dependencies
````
import { ApplicationRef, Injector } from '@angular/core';
import { createCustomElement } from '@angular/elements';
````
In the @NgModule decorator keep the Bootstrap array as empty:
````
bootstrap: [],
````
Then add the constructor for Injector & Application Reference
Add a ngDoBootstarp method, inside that method

We can create a custom element using the createCustomElement for integration in to the parent application.
and/or
We can pass the AppComponent to bootstarp by createElement and append it to the body of the document using application Reference for running the mfe as a standalone application.

### Step 5: In Your Parent Application add/change the following

#### 1. Install the below dependencies in your parent application
````
@angular-extensions/elements 
bootstrap
jquery
````

#### 2. Add the below import statement in your **app.module.ts** file
````
import { LazyElementsModule} from '@angular-extensions/elements';
import { CommonModule } from '@angular/common';
````

#### 3. Identify the parent component where you want to integrate the mfe application.
In the component that you want to integrate the mfe

In the ~component.ts:
Add a variable which points to the link the mfe application is running on:
````
http://{{server:port number}}/{{concatenated file}}.js
````
In the ~component.html
Add the mfe application tag and using axLazyElement directive pass the link of the mfe application

#### 4. Run and Test
Run and test if the Mfe Application is integrated with the Parent Application and/or is running as a standalone application.

To install dependencies use the below commands:
````
pnpm install 
or
npm install --legacy-peer-deps
````

If there is an issue where the parent application is not loading the new mfe content after any changes are made to the mfe application, it might me an issue with browser caching.
To resolve this issue we can use cache busting methods like appending date/time at the end of the concatenated file so that the browser will not cache the file and load the concatenated file everytime.
