define([
  'angular',
  'angular-ui-router',
  'angular-sanitize',
  'angular-animate',
  'controllers',
  'directives',
  'filters',
  'services'
], function (angular) {
  'use strict';
  var app = angular.module('flamengo', [
    'app.controllers',
    'app.directives',
    // 'app.services',
    // 'app.filters',
    'ui.router',
    'ngAnimate',
    'ngSanitize'
  ]).run(function ($rootScope, $stateParams) {
    var unregister = $rootScope.$on('$stateChangeSuccess', function () {
      $rootScope.stateParams = $stateParams;
    });
  });
  return app;
});
