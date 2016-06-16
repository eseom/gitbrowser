define([], function () {
  return function initialLoadingResolve($timeout,
                                        $rootScope,
                                        $animate) {
    return ({
      link: link,
      restrict: "A"
    });
    function link(scope, element, attributes) {
      $rootScope.$on('$stateChangeSuccess', function () {
        $animate.addClass(element, 'm-app-hide').then(function () {
          element.remove()
        });
      });
    }
  };
});