define([
  'angular',
  './directives/show-during-resolve',
  './directives/initial-loading-resolve',
  './directives/branch-indicator',
  './directives/clone-indicator',
  './directives/commit-card'
], function () {
  'use strict';
  /* new "directives" sub modules */
  var directives = angular.module('app.directives', []);
  for (var i = 1; i < arguments.length; i++) {
    var a = arguments[i];
    var directiveName = '';
    /* get the controller name */
    try {
      directiveName = a.toString().split('(')[0].split(' ')[1];
    } catch (e) {
      console.error('invalid directive spec', a);
      return;
    }
    /* register the directives */
    directives.directive(directiveName, a);
  }
});