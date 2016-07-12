define([], function () {
  'use strict';
  return {
    controller: function repositoryNewCtrl($scope,
                                           $timeout,
                                           $uibModalInstance,
                                           $http,
                                           repos,
                                           callback) {
      var $s = $scope;

      $s.availableGroups = repos.groups;
      $s.new = {
        type: 'public',
        group: '',
        name: '',
        description: ''
      };

      $s.validate = {
        name: {
          result: '',
          status: false,
          loading: false
        }
      };

      /** validate the name */
      var $timer = null;
      $s.validateName = function () {
        $s.validate.name.loading = false;
        $s.validate.name.status = false;

        if ($timer)
          $timeout.cancel($timer);

        var n = $s.new.name.trim();
        if ($s.new.group === '') {
          $s.validate.name.result = 'select the group.';
          $s.validate.name.status = false;
          return;
        }
        if (n === '') {
          $s.validate.name.result = 'input your name.';
          $s.validate.name.status = false;
          return;
        }
        if (n.length < 2) {
          $s.validate.name.result = 'the name is too short.';
          $s.validate.name.status = false;
          return;
        }
        if (n.length > 30) {
          $s.validate.name.result = 'the name is too long.';
          $s.validate.name.status = false;
          return;
        }
        if (n.indexOf(' ') !== -1) {
          $s.validate.name.result = 'the name must not have any space.';
          $s.validate.name.status = false;
          return;
        }

        $s.validate.name.status = false;
        $s.validate.name.loading = true;

        $timer = $timeout(function () {
          $http.get('/repositories/show/' + $s.new.group + '/' + n).success(function (response, status) {
            if (status === 200) {
              $s.validate.name.loading = false;
              $s.validate.name.result = 'not availiable';
              $s.validate.name.status = false;
            } else {
              $s.validate.name.loading = false;
              $s.validate.name.result = 'available';
              $s.validate.name.status = true;
            }
          });
        }, 600);
      };

      $s.ok = function () {
        /* make repository */
        $http({
          method: 'POST',
          url: '/repositories',
          data: {
            type: $s.new.type,
            group: $s.new.group,
            name: $s.new.name,
            description: $s.new.description
          }
        }).then(function (response) {
          callback && callback();
          $uibModalInstance.close(response.data);
        });
      };

      $s.cancel = function () {
        $uibModalInstance.dismiss('cancel');
      };
    }
  };
});
