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
      $rootScope.flashMessage = function (text) {
        $rootScope.flash.error = '';
        $rootScope.flash.message = text;
      };
      $rootScope.flashError = function (text) {
        $rootScope.flash.message = '';
        $rootScope.flash.error = text;
      };
      /** flash message */
      $rootScope.flash = {
        message: '',
        error: ''
      };

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
      /** flash message */
      $rootScope.flash = {
        message: '',
        error: ''
      };

      /** stateParams */
      $rootScope.stateParams = $stateParams;
    });
    $rootScope.$on('$stateChangeError', function (e, toState, toParams, fromState, fromParams, error) {
      if (fromState.name === '') {
        e.preventDefault();
        return false;
      }
    });
  });
  return app;
});
