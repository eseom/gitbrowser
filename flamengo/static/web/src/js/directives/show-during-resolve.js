define([], function () {
  return function showDuringResolve($rootScope,
                                    $timeout) {
    return {
      restrict: 'C',
      link: function (scope, element) {
        $(element).addClass('ng-hide');
        var unregister1 = $rootScope.$on('$stateChangeStart', function () {
            element.removeClass('ng-hide');
            $timeout(function () {
              element.addClass('ng-hide');
            }, 10000);
          }),
          unregister2 = $rootScope.$on('$stateChangeSuccess', function () {
            element.addClass('ng-hide');
          });
        scope.$on('$destroy', function () {
          unregister1();
          unregister2();
        });
      }
    };
  }
});
