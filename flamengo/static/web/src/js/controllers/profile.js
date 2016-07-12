define([], function () {
  'use strict';
  return {
    name: 'profile',
    url: '/profile',
    resolve: {
      profile: function ($http) {
        return $http.get('/auth/me');
      }
    },
    controller: function profileCtrl($scope,
                                     $rootScope,
                                     $http,
                                     $timeout,
                                     profile,
                                     Flash) {
      var $s = $scope;

      $rootScope.title = 'Profile';
      $s.user = profile.data.user;

      $s.editable = {
        username: false,
        nickname: profile.data.user.nickname.length === 0
      };
      $s.setUsernameEditable = function () {
        $s.editable.username = true;
      };
      $s.setNicknameEditable = function () {
        $s.editable.nickname = true;
        $s.user.nickname = '';
        $s.validateNickname();
      };

      $s.validate = {
        name: {
          result: '',
          status: $s.user.name !== ''
        },
        nickname: {
          result: '',
          status: $s.user.nickname !== '',
          loading: false
        }
      };

      /** validate the name */
      $s.validateName = function () {
        $s.validate.name.status = false;

        var n = $s.user.name.trim();
        if (n === '') {
          $s.validate.name.result = 'input your name.';
          $s.validate.nickname.status = false;
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

        $s.validate.name.result = 'available';
        $s.validate.name.status = true;
      };

      /** validate the nickname */
      var $timer = null;
      $s.validateNickname = function () {
        $s.validate.nickname.loading = false;
        $s.validate.nickname.status = false;

        if ($timer)
          $timeout.cancel($timer);

        var n = $s.user.nickname.trim();
        if (n === '') {
          $s.validate.nickname.result = 'input your nickname.';
          $s.validate.nickname.status = false;
          return;
        }
        if (n.length < 2) {
          $s.validate.nickname.result = 'the nickname is too short.';
          $s.validate.nickname.status = false;
          return;
        }
        if (n.length > 30) {
          $s.validate.nickname.result = 'the nickname is too long.';
          $s.validate.nickname.status = false;
          return;
        }
        if (n.indexOf(' ') !== -1) {
          $s.validate.nickname.result = 'the nickname must not have any space.';
          $s.validate.nickname.status = false;
          return;
        }

        $s.validate.nickname.status = false;
        $s.validate.nickname.loading = true;

        $timer = $timeout(function () {
          $http.post('/auth/nickname/' + n).success(function (response) {
            $s.validate.nickname.loading = false;
            $s.validate.nickname.result = 'not availiable';
            $s.validate.nickname.status = false;
          }).error(function (data, status) {
            $s.validate.nickname.loading = false;
            if (status !== 404)
              return;
            $s.validate.nickname.result = 'available';
            $s.validate.nickname.status = true;
          });
        }, 600);
      };

      /** save profile information */
      $s.save = function () {
        /* check validation */
        var targets = ['name', 'nickname'];
        for (var i = 0; i < targets.length; i++) {
          if (!$s.validate[targets[i]].status) {
            Flash.create('danger', $s.validate[targets[i]].result);
            return;
          }
        }

        var name = $s.user.name.trim();
        var nickname = $s.user.nickname.trim();
        var data = {
          id: $s.user.id,
          username: $s.user.username,
          nickname: $s.user.nickname,
          name: $s.user.name
        };
        if ($s.user.password !== '' && $s.user.password === $s.user.passwordConfirm)
          data.password = $s.user.password;
        $http({
          method: 'PUT',
          url: '/auth/save',
          data: data
        }).then(function (response) {
          $s.user.password = '';
          $s.user.passwordConfirm = '';

          Flash.create('success', 'Your information was saved.');
        });
      };

      if ($s.user.name === '') {
        $s.validateName();
      }
      if ($s.editable.nickname) {
        $s.validateNickname();
      }
    }
  };
});
