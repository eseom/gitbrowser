require.config({
  paths: {
    domReady: '../bower_components/domready/ready',
    angular: '../bower_components/angular/angular',
    'angular-sanitize': '../bower_components/angular-sanitize/angular-sanitize',
    'angular-ui-router': '../bower_components/angular-ui-router/release/angular-ui-router',
    'angular-animate': '../bower_components/angular-animate/angular-animate',
    jquery: '../bower_components/jquery/dist/jquery',
    bootstrap: '../bower_components/bootstrap/dist/js/bootstrap',
    diffview: '../vendor/diffview/diffview'
  },
  shim: {
    angular: {
      exports: 'angular'
    },
    'angular-sanitize': {
      deps: ['angular']
    },
    'angular-ui-router': {
      deps: ['angular']
    },
    'angular-animate': {
      deps: ['angular']
    },
    bootstrap: {
      deps: ['jquery']
    }
  },
  deps: [
    './boot'
  ]
});
