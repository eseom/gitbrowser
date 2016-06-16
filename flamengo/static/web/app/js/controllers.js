define([
  'angular',
  './controllers/blob',
  './controllers/commit',
  './controllers/commits',
  './controllers/dashboard',
  './controllers/tree'
], function (angular) {
  'use strict';
  /* new "controllers" sub modules */
  var controllers = angular.module('app.controllers', []),
    returnValue = {};
  for (var i = 1; i < arguments.length; i++) {
    var a = arguments[i];
    var controllerName = '';
    /* get the controller name */
    try {
      controllerName = a.controller.toString().split('(')[0].split(' ')[1];
    } catch (e) {
      console.error('invalid controller spec');
      return;
    }
    /* make resolve objects */
    returnValue[controllerName.replace('Ctrl', '')] = {
      url: a.url,
      resolve: a.resolve
    };
    /* register the controller */
    controllers.controller(controllerName, a.controller);
  }
  return returnValue;
});