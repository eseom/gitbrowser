define([], function () {
  'use strict';
  return {
    url: '/commits/:group/:repo/:branch/:take/:skip',
    resolve: {
      commits: function ($http, $stateParams) {
        var group = $stateParams.group,
          repo = $stateParams.repo,
          branch = $stateParams.branch,
          take = $stateParams.take,
          skip = $stateParams.skip;
        return $http({
          url: [
            '/repositories/commits', group, repo, branch, take, skip
          ].join('/'),
          method: 'GET'
        });
      }
    },
    controller: function commitsCtrl($scope,
                                     $rootScope,
                                     $state,
                                     $stateParams,
                                     $http,
                                     commits) {
      $rootScope.title = 'commits';
      $scope.branches = commits.data.branches;
      $scope.list = commits.data.commits;
      $scope.gotoAnotherBranch = function (branch) {
        $state.go('commits', {branch: branch})
      }
    }
  }
});