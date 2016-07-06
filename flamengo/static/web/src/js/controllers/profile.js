define([], function () {
  'use strict';
  return {
    url: '/profile',
    resolve: {
    },
    controller: function profileCtrl($scope, $rootScope, $stateParams) {
      $rootScope.title = 'profile';
    }
  };
});
