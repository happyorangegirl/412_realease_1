# E2E config admin

This project is forked from [RDash rdash-angular](https://github.com/rdash/rdash-angular.git).

## Development Env:
10.102.6.40:8888/#/editor/show

## TODO
* Test our UI, generate coverage report with `npm install codecov --save-dev`
* Add business logic in next release. Such as retrive available vCenter FQDN from vro, Avamar-grid infomation from Redis
* Editor validation

## Usage
* Google-Chrome only

### Requirements
* [NodeJS >=5.0](http://nodejs.org/) (with [NPM](https://www.npmjs.org/))
* [Bower](http://bower.io)
* [Gulp](http://gulpjs.com)

`$ sudo sh install.sh`

### Installation
1. Clone the repository: `git clone https://fanm1@pie6.rtp.lab.emc.com/scm/~fanm1/e2e_ui.git`
2. Install the NodeJS dependencies: `sudo npm install`.
3. Install the Bower dependencies: `bower install`.
4. Run the gulp build task: `gulp build`.
5. Run the gulp default task: `gulp`. This will build and watch any changes made automatically, and also run a live reload server on [http://localhost:8888](http://localhost:8888).

Ensure your preferred web server points towards the `dist` directory.

### Configure
`cat gulp_ng_config.json`

### Development
Continue developing the dashboard further by editing the `src` directory. With the `gulp` command, any file changes made will automatically be compiled into the specific location within the `dist` directory.

### Test
* Units: `$ npm test`

#### Modules & Packages
By default, rdash-angular includes [`ui.bootstrap`](http://angular-ui.github.io/bootstrap/), [`ui.router`](https://github.com/angular-ui/ui-router) and [`ngCookies`](https://docs.angularjs.org/api/ngCookies). 

If you'd like to include any additional modules/packages not included with rdash-angular, add them to your `bower.json` file and then update the `src/index.html` file, to include them in the minified distribution output.

## Read more
* [https://github.com/jdorn/json-editor](https://github.com/jdorn/json-editor)
