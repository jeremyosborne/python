(function(exports) {

/**
 * @class Notifications mixin specific to the stats application.
 * 
 * @example
 * // Within your application code, after initializing the notification
 * // controller, set the following:
 * NotificationsMixin.reopen({
 *     "notificationsControllerPath": "myApp.notificationsController",
 * });
 * 
 * @extends Ember.Mixin
 */
var NotificationsMixin = Ember.Mixin.create({
    /**
     * Path to the notification controller.
     * Set this to your notifications controller in your application or you
     * will not receive notifications.
     * Assumes the controller is a global singleton.
     * @type {String}
     */
    "notificationsControllerPath": null,
    
    /**
     * Implements the info notification mechanism.
     * @param message {String} Notification to display.
     */
    "notifyInfo": function(message) {
        var path = this.get("notificationsControllerPath");
        
        if (!path) {
            throw new Error("Must declare a notificationsControllerPath.");
        }

        var notificationController = Ember.getPath(window, path);
        
        if (notificationController) {
            notificationController.info(message);
        }
    },
    
    /**
     * Implements the error notification mechanism.
     * @param message {String} Notification to display.
     */
    "notifyError": function(message) {
        var path = this.get("notificationsControllerPath");
        
        if (!path) {
            throw new Error("Must declare a notificationsControllerPath.");
        }

        var notificationController = Ember.getPath(window, path);
        
        if (notificationController) {
            notificationController.error(message);
        }
    },
});
// Export
exports.NotificationsMixin = NotificationsMixin;



})(window);
