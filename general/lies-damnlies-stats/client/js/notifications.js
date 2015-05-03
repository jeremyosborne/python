(function(exports) {

/**
 * @class Model for the notifications.
 *
 * @example
 * // Build a notification set to expire in the future.
 * var notification = Notification.create({
 *     "message": "Hello world!",
 * });
 *  
 * @extends Ember.Object
 * @name Notification
 */
var Notification = Ember.Object.extend({
    /**
     * The message.
     * @type {String}
     */
    "message": "",
    
    /**
     * The type of message. Defaults to "info".
     * @type
     */
    "classification": "info",

    /**
     * Minimum amount of time milliseconds will a notification last?
     * @type {Number}
     */
    "lifetime": 3300,
    
    /**
     * When should this message expire (ms since the epoch)?
     * @type {Number}
     */
    "expires": 0,
    
    /**
     * Initialize the expiration.
     */
    "init": function() {
        var expires = Date.now() + this.get("lifetime");
        this.set("expires", expires);
        
        this._super();
    },
});
// Export
exports.Notification = Notification;



/**
 * @class Display notifications within the application.
 * 
 * @example
 * // By default, the controller will initiate it's own view into the page.
 * var notificationsController = NotificationsController.create();
 * 
 * @extends Ember.ArrayProxy
 * @name NotificationsController
 */
var NotificationsController = Ember.ArrayProxy.extend({
    /**
     * The content managed by this controller.
     * @type {Notification[]}
     */
    "content": null,

    /**
     * The view serviced by this controller.
     * @type {NotificationsView}
     */
    "view": null,
    
    /**
     * How many milliseconds between expiration checks?
     * @type {Number}
     */
    "_expirationTimeout": 1000,
    
    /**
     * The setTimeout id of any timeout .
     * @type {String}
     */
    "_timerId": null,
    
    /**
     * Log an info level message to the notification queue.
     * @param message {String} A message to display, HTML strings are 
     * acceptable.
     */
    "info": function(message) {
        this.pushObject(Notification.create({
            "message": message,
        }));
        
        this.countdown();
    },
    
    /**
     * Log an error level message to the notification queue.
     * @param message {String} A message to display, HTML strings are 
     * acceptable.
     */
    "error": function(message) {
        this.pushObject(Notification.create({
            "message": message,
            "classification": "error",
        }));
        
        this.countdown();
    },

    /**
     * When triggered, will attempt to expire the notification at the
     * top of the stack.
     */
    "expire": function() {
        var now = Date.now();
        
        // Remove any previously set timeout id.
        this.set("_timerId", null);
                
        // NOTE: to access content via proxy and by index, use objectAt.
        if (this.get("length") && (this.objectAt(0).expires < now)) {
            // Only remove one notification at a time.
            this.shiftObject();
        }
        
        // Call again to begin the cycle.
        this.countdown();
    },
    
    /**
     * Call to begin the countdown on the list of notifications.
     * Can be called multiple times.
     */
    "countdown": function() {
        var timerId,
            // Ooops, iOS doesn't support .bind. Damnit.
            self = this;
        
        // Only initiate the countdown if we aren't already within a countdown
        // and only if we have content.
        if (this.get("length") > 0 && !this.get("_timerId")) {
            timerId = setTimeout(function() {
                    self.expire();
                },
                // Add a bit of a fudge factor to increase the likelihood of
                // expiring notifications each cycle.
                this.get("_expirationTimeout")
            );
            this.set("_timerId", timerId)
        }
    },
    
    /**
     * By default, the controller will initiate it's own view, as it is
     * assumed that there will be only one notification view in the page.
     */
    "init": function() {
        // Annoying, unless I'm misunderstanding the code, I have to set
        // the content myself to an array.
        this.set("content", []);
        
        // The ArrayController/ArrayProxy is just that: an array with
        // added helper methods.
        this._super();

        // Bind the relationship between view and controller.
        var view = NotificationsView.create({
            "controller": this,
        });
        this.set("view", view);
    },
});
// Export
exports.NotificationsController = NotificationsController;



/**
 * @class Display notifications within the application.
 * 
 * @example
 * // Build this view.
 * var view = NotificationsView.create({
 *     "controller": notificationControllerInstance,
 * });
 * 
 * @extends Ember.View
 * @name NotificationsView
 */
var NotificationsView = Ember.View.extend({
    /**
     * The name of the template.
     * @type {String}
     */
    "templateName": "notifications",
    
    /**
     * The controller bound to this view.
     * @type {NotificationsController}
     */
    "controller": null,
    
    /**
     * Pointer to the list of messages.
     */
    "contentBinding": "*controller",
    
    /**
     * Add ourself to the page.
     */
    "init": function() {
        this._super();
        
        this.appendTo("#app-body");
    },
});
// Export
exports.NotificationsView = NotificationsView;

})(window);
