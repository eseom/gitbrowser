define([], function () {
  'use strict';
  var getRepositories = function ($http) {
    return $http({
      url: '/repositories',
      method: 'GET'
    })
  };
  return {
    url: '/repository/:group',
    resolve: {
      repositories: function ($http) {
        return $http({
          url: '/repositories',
          method: 'GET'
        });
      }
    },
    controller: function repositoryCtrl($scope,
                                        $rootScope,
                                        $state,
                                        $http,
                                        $uibModal,
                                        $stateParams,
                                        repositories) {
      /**
       * remap repositories list
       * @type {{}}
       */
      var repositoriesMap = {};
      for (var key in repositories.data.repos) {
        var array = repositories.data.repos[key];
        array.map(function (it) {
          repositoriesMap[it.id] = {
            group: key,
            name: it.name,
            description: it.description
          }
        });
      }

      $rootScope.title = 'repository';
      $scope.repos = repositories.data.repos;

      var load = function (_repos) {
        $scope.groups = _repos.data.groups;
        $scope.repos = _repos.data.repos;
      };
      var reload = function () {
        getRepositories($http).then(load);
      };
      load(repositories);

      $scope.create = function () {
        $scope.open('sm');
      };

      $scope.edit = function (id) {
        var r = repositoriesMap[id];
        $scope.open('sm', {
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

      $scope.open = function (size, current) {
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
