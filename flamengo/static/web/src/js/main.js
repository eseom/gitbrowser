require.config({
  paths: {
    domReady: '../bower_components/domready/ready',
    angular: '../bower_components/angular/angular',
    'angular-sanitize': '../bower_components/angular-sanitize/angular-sanitize',
    'angular-ui-router': '../bower_components/angular-ui-router/release/angular-ui-router',
    'angular-animate': '../bower_components/angular-animate/angular-animate',
    'angular-bootstrap': '../bower_components/angular-bootstrap/ui-bootstrap-tpls',
    'angular-flash': '../bower_components/angular-flash-alert/dist/angular-flash',
    jquery: '../bower_components/jquery/dist/jquery',
    bootstrap: '../bower_components/bootstrap/dist/js/bootstrap',
    diffview: '../vendor/diffview/diffview',

    /** markdown editor */
    'markdown-converter': '../bower_components/pagedown/Markdown.Converter',
    'markdown-sanitizer': '../bower_components/pagedown/Markdown.Sanitizer',
    'markdown-extra': '../bower_components/pagedown/Markdown.Extra',
    'markdown-editor': '../bower_components/pagedown/Markdown.Editor',
    'markdown-angular-pagedown': '../bower_components/angular-pagedown/angular-pagedown'
  },
  shim: {
    angular: {exports: 'angular'},
    bootstrap: {deps: ['jquery']},
    'angular-sanitize': {deps: ['angular']},
    'angular-ui-router': {deps: ['angular']},
    'angular-animate': {deps: ['angular']},
    'angular-bootstrap': {deps: ['angular']},
    'angular-flash': {deps: ['angular']},

    /** markdown editor */
    'markdown-angular-pagedown': {
      deps: ['markdown-converter', 'markdown-sanitizer', 'markdown-extra', 'markdown-editor']
    },
    'markdown-editor': {deps: ['markdown-extra']},
    'markdown-extra': {deps: ['markdown-sanitizer']},
    'markdown-sanitizer': {deps: ['markdown-converter']}
  }
});

define([
  'require',
  'angular',
  'app',
  'routes',
  'jquery', 'bootstrap', 'diffview'
], function (require, angular) {
  'use strict';
  angular.bootstrap(document, ['flamengo']);
});
