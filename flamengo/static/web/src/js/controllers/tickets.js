define([], function () {
  'use strict';
  var getTickets = function ($http, rgroup, rname) {
    return $http({
      url: [
        '/issue/tickets', rgroup, rname
      ].join('/'),
      method: 'GET'
    });
  };
  return {
    url: '/tickets/:rgroup/:rname/:branch/:take/:skip',
    resolve: {
      tickets: function ($http, $stateParams) {
        var rgroup = $stateParams.rgroup,
          rname = $stateParams.rname;
        return getTickets($http, rgroup, rname);
      }
    },
    controller: function ticketsCtrl($scope,
                                     $rootScope,
                                     $uibModal,
                                     $state,
                                     $stateParams,
                                     $http,
                                     tickets) {
      $rootScope.title = 'tickets';

      var rgroup = $stateParams.rgroup,
        rname = $stateParams.rname;

      var load = function (tickets) {
        $scope.tickets = tickets.data.tickets;
      };

      var reload = function () {
        getTickets($http, rgroup, rname).then(load);
      };
      load(tickets);


      $scope.create = function () {
        $scope.openNewModal('sm');
      };

      $scope.openNewModal = function (size, current) {
        var modalInstance = $uibModal.open({
          animation: true,
          templateUrl: 'html/tickets/new.html',
          controller: 'ticketsNewCtrl',
          size: size,
          resolve: {
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
  }
});
