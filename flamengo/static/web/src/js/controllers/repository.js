define([], function () {
  'use strict';
  var getRepositories = function ($http) {
    return $http({
      url: '/repositories',
      method: 'GET'
    }).then(function (response) {
      return response
    });
  };
  return {
    url: '/repository/:group',
    resolve: {
      repositories: function ($http, $state, Flash) {
        return $http({
          url: '/repositories',
          method: 'GET'
        }).then(function (response) {
          return response
        }, function (response) {
          if (response.status === 301) {
            /* no available nickname */
            Flash.create('info',
              'You have to make a <strong>nickname</strong> for creating your own repositories.');
            $state.go('profile');
            return false;
          }
        });
      }
    },
    controller: function repositoryCtrl($scope,
                                        $rootScope,
                                        $http,
                                        $uibModal,
                                        repositories) {
      var repositoriesMap = {};

      $rootScope.title = 'Repository';
      $scope.repos = repositories.data.repos;

      var load = function (_repos) {
        $scope.groups = _repos.data.groups;
        $scope.repos = _repos.data.repos;
        /**
         * remap repositories list
         * @type {{}}
         */
        for (var key in _repos.data.repos) {
          var array = _repos.data.repos[key];
          array.map(function (it) {
            repositoriesMap[it.id] = {
              group: key,
              name: it.name,
              description: it.description
            }
          });
        }
      };
      var reload = function () {
        getRepositories($http).then(load);
      };
      load(repositories);

      $scope.create = function () {
        $scope.openNewModal('sm');
      };

      $scope.edit = function (id) {
        var r = repositoriesMap[id];
        $scope.openEditModal('sm', {
          id: id,
          group: r.group,
          name: r.name,
          description: r.description
        })
      };

      $scope.delete = function (id) {
        return $http({
          url: '/repositories/' + id,
          method: 'DELETE'
        }).then(function (response) {
          reload();
        })
      };

      $scope.openNewModal = function (size, current) {
        var modalInstance = $uibModal.open({
          animation: true,
          templateUrl: 'html/repository/new.html',
          controller: 'repositoryNewCtrl',
          size: size,
          resolve: {
            repos: function () {
              return {
                groups: repositories.data.groups,
                current: current
              }
            },
            callback: function () {
              return reload;
            }
          }
        });

        modalInstance.result.then(function () {
        }, function () {
          // $log.info('dismiss');
        });
      };
      $scope.openEditModal = function (size, current) {
        var modalInstance = $uibModal.open({
          animation: true,
          templateUrl: 'html/repository/edit.html',
          controller: 'repositoryEditCtrl',
          size: size,
          resolve: {
            repos: function () {
              return {
                groups: repositories.data.groups,
                repos: repositories.data.repos,
                current: current
              }
            },
            callback: function () {
              return reload;
            }
          }
        });

        modalInstance.result.then(function () {
        }, function () {
          // $log.info('dismiss');
        });
      };
    }
  };
});
