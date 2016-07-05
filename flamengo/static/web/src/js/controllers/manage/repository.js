define([], function () {
  'use strict';
  var getRepos = function ($http) {
    return $http({
      url: '/manage/repos',
      method: 'GET'
    })
  };
  return {
    url: '/manage/repository',
    resolve: {
      repos: function ($http) {
        return getRepos($http);
      }
    },
    controller: function manageRepositoryCtrl($scope,
                                              $rootScope,
                                              $state,
                                              $http,
                                              $uibModal,
                                              $stateParams,
                                              repos) {
      $rootScope.title = 'repositories management';
      var load = function (_repos) {
        $scope.groups = _repos.data.groups;
        $scope.repos = _repos.data.repos;
      };
      var reload = function () {
        getRepos($http).then(load);
      };
      load(repos);

      $scope.create = function () {
        $scope.open('sm');
      };
      $scope.edit = function (group, name) {
        $scope.open('sm', {group: group, name: name})
      };
      $scope.delete = function (group, name) {
        var data = {
          group: group,
          name: name
        };
        return $http({
          url: '/manage/repo/delete',
          method: 'DELETE',
          data: data
        }).then(function (response) {
          reload();
        })
      };

      $scope.open = function (size, repo) {
        var modalInstance = $uibModal.open({
          animation: true,
          templateUrl: 'myModalContent.html',
          controller: 'ModalInstanceCtrl',
          size: size,
          resolve: {
            repos: function () {
              return {
                groups: repos.data.groups,
                repos: repos.data.repos,
                current: repo
              }
            },
            callback: function () {
              return reload;
            }
          }
        });

        modalInstance.result.then(function (selectedItem) {
          $scope.selected = selectedItem;
        }, function () {
          // $log.info('Modal dismissed at: ' + new Date());
        });
      };
    }
  };
});
