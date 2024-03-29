define([], function () {
  'use strict';
  return {
    url: '/commit/:rgroup/:rname/:hexsha',
    resolve: {
      commit: function ($http, $stateParams) {
        var rgroup = $stateParams.rgroup,
          rname = $stateParams.rname,
          hexsha = $stateParams.hexsha;
        return $http({
          url: '/repositories/commit/' + rgroup + '/' + rname + '/' + hexsha,
          method: 'GET'
        });
      }
    },
    controller: function commitCtrl($scope,
                                    $rootScope,
                                    $state,
                                    $sce,
                                    $stateParams,
                                    $http,
                                    commit) {
      var rgroup = $stateParams.rgroup,
        rname = $stateParams.rname;
      $rootScope.title = rgroup + '/' + rname + ' <span class="sub">commit</span>';
      var hexsha = $stateParams.hexsha || '';
      commit.data.diff_contents.forEach(function (data) {
        angular.element(document.getElementById('diffContents')).append(
          diffview.buildView({
            baseTextLines: data.baseTextLines,
            newTextLines: data.newTextLines,
            opcodes: data.opcodes,
            baseTextName: data.baseTextName,
            newTextName: data.newTextName,
            contextSize: 3
          }));
      });
      $scope.truncated = commit.data.truncated;
      $scope.countOfDiffs = commit.data.count_of_diffs;
      $scope.parents = commit.data.parents.filter(function (it) {
        /* 4b825dc642cb6eb9a060e54bf8d69288fbee4904 is null commit hash */
        return it !== '4b825dc642cb6eb9a060e54bf8d69288fbee4904';
      });
      $scope.hexsha = hexsha;
      $scope.commit = commit.data.commit;
    }
  }
});
