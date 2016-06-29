define([], function () {
  'use strict';
  return {
    url: '/dashboard/:group',
    resolve: {
      repos: function ($http, $stateParams) {
        var group = $stateParams.group;
        return $http({
          url: '/repos' + (group ? '/' + group : ''),
          method: 'GET'
        });
      }
    },
    controller: function dashboardCtrl($scope, $rootScope, $stateParams, repos) {
      var group = $stateParams.group;
      console.log(12312)
      $rootScope.title = 'dashboard';
      $scope.isGroups = group === '';
      $scope.repos = repos.data.repos;
    }
  };
});
