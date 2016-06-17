define([], function () {
  'use strict';
  return {
    url: '/tree/:group/:repo/{path:any}',
    resolve: {
      tree: function ($http, $stateParams) {
        var group = $stateParams.group,
          repo = $stateParams.repo,
          path = $stateParams.path || '';
        return $http({
          url: '/tree/' + group + '/' + repo + '/' + path,
          method: 'GET'
        });
      },
      commitCount: function ($http, $stateParams) {
        var group = $stateParams.group,
          repo = $stateParams.repo,
          path = $stateParams.path || '';
        return $http({
          url: '/commit/count/' + group + '/' + repo + '/' + path,
          method: 'GET'
        });
      }
    },
    controller: function treeCtrl($scope,
                                  $rootScope,
                                  $state,
                                  $stateParams,
                                  $http,
                                  tree,
                                  commitCount) {
      var group = $stateParams.group,
        repo = $stateParams.repo,
        path = $stateParams.path || '';

      $scope.branch = tree.data.current_branch;
      $scope.list = [];
      $scope.commitCount = commitCount.data.count;

      /* */
      var first = [];
      if (path !== '')
        first = [{type: 'system', name: '(parent directory)'}];
      var list = first.concat(tree.data.list);

      $scope.list = list;
      $scope.branches = tree.data.branches;

      $scope.back = function () {
        var p = path.split('/');
        var url = p.slice(0, p.length - 1).join('/');
        $state.go('tree', {group: group, repo: repo, branch: branch, path: url})
      };
      $scope.gotoAnotherBranch = function (branch) {
        $state.go('tree', {group: group, repo: repo, path: branch})
      }
    }
  };
});
