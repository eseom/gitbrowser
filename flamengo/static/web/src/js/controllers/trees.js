define([], function () {
  'use strict';
  return {
    url: '/trees/:rgroup/:rname/{path:any}',
    resolve: {
      trees: function ($http, $stateParams) {
        var rgroup = $stateParams.rgroup,
          rname = $stateParams.rname,
          path = $stateParams.path || '';
        return $http({
          url: '/repositories/trees/' + rgroup + '/' + rname + '/' + path,
          method: 'GET'
        });
      },
      commitCount: function ($http, $stateParams) {
        var rgroup = $stateParams.rgroup,
          rname = $stateParams.rname,
          path = $stateParams.path || '';
        return $http({
          url: '/repositories/commit/count/' + rgroup + '/' + rname + '/' + path,
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
      var rgroup = $stateParams.rgroup,
        rname = $stateParams.rname,
        path = $stateParams.path || '';

      $rootScope.title = 'source browser';
      $scope.branch = trees.data.current_branch;
      $scope.list = [];
      $scope.lastCommit = trees.data.last_commit;
      $scope.commitCount = commitCount.data.count;
      $scope.cloneUrl = 'http://localhost:5000/' + rgroup + '/' + rname;
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
        $state.go('trees', {rgroup: rgroup, rname: rname, path: url})
      };
      $scope.gotoAnotherBranch = function (branch) {
        $state.go('trees', {rgroup: rgroup, rname: rname, path: branch})
      };

      $scope.message = {
        existingProject: 'git remote add origin ' + $scope.cloneUrl + '\n\
git push --all',
        newProject: 'project=\'' + $stateParams.rname + '\'\n\
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
