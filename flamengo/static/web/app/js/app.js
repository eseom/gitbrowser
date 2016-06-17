define([
  'angular',
  'angular-ui-router',
  'angular-sanitize',
  'angular-animate',
  'angular-bootstrap',
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
    'ui.bootstrap',
    'ngAnimate',
    'ngSanitize'
  ]).config(function ($httpProvider) {
    /**
     * http interceptor
     */
    $httpProvider.interceptors.push(['$rootScope', '$q', function ($rootScope, $q) {
      return {
        responseError: function (rejection) {
          /**
           * if not signed in, got o /auth/signin
           */
          if (rejection.status === 401) {
            if (rejection.data.code === 0) {
              window.location.href = '/auth/signin';
              return $q.reject(rejection);
            }
          }
          return $q.reject(rejection);
        }
      };
    }]);
  }).run(function ($rootScope, $stateParams) {
    /**
     * global event
     */
    $rootScope.$on('$stateChangeSuccess', function () {
      $rootScope.stateParams = $stateParams;
    });
  });
  return app;
});
