define([], function () {
  'use strict';
  return {
    controller: function ticketsNewCtrl($scope,
                                        $timeout,
                                        $stateParams,
                                        $uibModalInstance,
                                        $http,
                                        callback) {
      var $s = $scope;

      $s.new = {
        summary: '',
        content: '',
      };

      $s.validate = {
        summary: {
          result: '',
          status: false,
        },
        content: {
          result: '',
          status: false,
        }
      };

      /** validate the summary */
      var $timer = null;
      $s.validateSummary = function () {
        $s.validate.summary.status = false;

        if ($timer)
          $timeout.cancel($timer);

        var n = $s.new.summary.trim();
        if (n === '') {
          $s.validate.summary.result = 'input a summary.';
          $s.validate.summary.status = false;
          return;
        }
        if (n.length > 256) {
          $s.validate.summary.result = 'the summary is too long.';
          $s.validate.summary.status = false;
          return;
        }

        $s.validate.summary.result = 'available';
        $s.validate.summary.status = true;
      };

      $s.ok = function () {
        var rgroup = $stateParams.rgroup,
          rname = $stateParams.rname;
        /* make a ticket */
        $http({
          method: 'POST',
          url: [
            '/issue/tickets', rgroup, rname
          ].join('/'),
          data: {
            summary: $s.new.summary,
            content: $s.new.content,
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
