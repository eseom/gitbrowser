define([], function () {
  'use strict';
  return {
    url: '/trees/:group/:repo/{path:any}',
    resolve: {
      trees: function ($http, $stateParams) {
        var group = $stateParams.group,
          repo = $stateParams.repo,
          path = $stateParams.path || '';
        return $http({
          url: '/repositories/trees/' + group + '/' + repo + '/' + path,
          method: 'GET'
        });
      },
      commitCount: function ($http, $stateParams) {
        var group = $stateParams.group,
          repo = $stateParams.repo,
          path = $stateParams.path || '';
        return $http({
          url: '/repositories/commit/count/' + group + '/' + repo + '/' + path,
          method: 'GET'
        });
      }
    },
    controller: function treesCtrl($scope,
                                   $rootScope,
                                   $state,
                                   $stateParams,
                                   $http,
                                   trees,
                                   commitCount) {
      var group = $stateParams.group,
        repo = $stateParams.repo,
        path = $stateParams.path || '';

      $rootScope.title = 'source browser';
      $scope.branch = trees.data.current_branch;
      $scope.list = [];
      $scope.lastCommit = trees.data.last_commit;
      $scope.commitCount = commitCount.data.count;
      $scope.cloneUrl = 'http://localhost:5000/' + group + '/' + repo;
      $scope.paths = path.split('/').slice(1);

      /* */
      var first = [];
      if (path !== $scope.branch)
        first = [{type: 'system', name: '(parent directory)'}];
      var list = first.concat(trees.data.list);

      $scope.list = list;
      $scope.branches = trees.data.branches;

      $scope.back = function () {
        var p = path.split('/');
        var url = p.slice(0, p.length - 1).join('/');
        $state.go('trees', {group: group, repo: repo, path: url})
      };
      $scope.gotoAnotherBranch = function (branch) {
        $state.go('trees', {group: group, repo: repo, path: branch})
      };

      $scope.message = {
        existingProject: 'git remote add origin ' + $scope.cloneUrl + '\n\
git push --all',
        newProject: 'project=\'' + $stateParams.repo + '\'\n\
git clone ' + $scope.cloneUrl + '\n\
cd $project\n\
echo \\# $project > README.md\n\
git add README.md\n\
git commit -m "first commit"\n\
git push origin master'
      }
    }
  };
});
