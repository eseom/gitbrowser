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
    controller: function dashboardCtrl($scope, $stateParams, repos) {
      var group = $stateParams.group;
      $scope.isGroups = group === '';
      $scope.repos = repos.data.repos;
    }
  };
});
