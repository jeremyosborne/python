(function(exports) {



/**
 * @class Stats appication object.
 * 
 * See the StateManager initialization for where the majority of the 
 * properties are initialized for this object.
 * 
 * @static
 * @extends Ember.Application
 */
var App = Ember.Application.create({
    //--------------------------------------------------- General Use objects
    /**
     * The state manager responsible for this application, essentially the
     * main procedure that makes everything work.
     * @type {StateManager}
     */
    "stateManager": null,

    /**
     * Access to client side persisted data.
     * @type {DataCache}
     */
    "dataCache": null,

    /**
     * Memory map of relevant statistics.
     * @type {StatsCache}
     */
    "statsCache": null,
    
    //---------------------------------------------------------- Page Objects
    /**
     * Controls the message in the page header.
     * @type {PageHeaderController}
     */
    "pageHeaderController": null,
    
    /**
     * Controls the view container for the main content display.
     * @type {PageBodyController}
     */
    "pageBodyController": null,
    
    /**
     * Controls the view container for the footer display.
     * @type {PageFooterController}
     */
    "pageFooterController": null,

    /**
     * Handles the display, and removal of, notifications made by the
     * various application objects.
     * The path to this controller needs to be known by the notification
     * mixin.
     * @type {NotificationsController}
     */
    "notificationsController": null,
    
    //----------------------------------------------------------- int main(void)
    /**
     * Called when the page has loaded (like a DOM Ready event).
     * Initialize all of the app singletons.
     */
    "ready": function() {
        // Most class-like functions in ember have a _super() method that can
        // be invoked.
        // And we need to call it if we're going to override ready.
        this._super();

        // Need to initialize the NotificationsController and Mixin first.
        this.notificationsController = NotificationsController.create();
        // The NotificationsMixin requires knowledge of the notifications
        // controller singleton.
        NotificationsMixin.reopen({
            "notificationsControllerPath": "App.notificationsController",
        });

        this.pageHeaderController = PageHeaderController.create({
            "containerSelector": ldlsConf.pageHeaderSelector,
        });
        this.pageBodyController = PageBodyController.create({
            "containerSelector": ldlsConf.pageBodySelector,
        });
        this.pageFooterController = PageFooterController.create({
            "containerSelector": ldlsConf.pageFooterSelector,
        });
        
        this.dataCache = DataCache.create();

        this.statsCache = StatsCache.create({
            dataCache: this.dataCache,
        });

        // Used to manage the various application states.
        // The creation of the StateManager kicks off the initialization
        // of the application. See the StateManager code for the initialState.
        this.stateManager = StateManager.create();        
    },
});
// Export
exports.App = App;



})(window);
