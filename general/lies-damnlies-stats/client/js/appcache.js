(function(exports) {

/**
 * @class Handles interactions with the application cache events.
 *
 * @extends Ember.Object
 * @extends NotificationsMixin
 */
var AppCacheController = Ember.Object.extend(NotificationsMixin, {

    /**
     * Displayed as a notification when the application has updated code.
     * @type {String}
     */
    "updateMessage": "_This application has been updated. Please reload this page.",
    
    /**
     * Callback function fired when the appcache has been handled.
     * Override during create with the function that should be called after
     * the appcache has been handled (if any function should be called).
     * @type {Function}
     */
    "ready": function() {},
    
    /**
     * Initialize listeners on the application cache.
     */
    "init": function() {
        var self = this;
        
        this._super();
        
        // Setup applicationCache listeners
        if (window.applicationCache) {
            if (window.applicationCache.status == 0) {
                // According to the spec: 
                //    if status == 0 == UNCACHED
                // than we're not associated with any cache object and we should 
                // proceed like normal.
                self.ready();
            }
            else {
                // Otherwise, we have a cache and there will be events
                // associated with it.
                // Fix jquery (note: figure out if/why this is really needed.)
                jQuery.ajaxSetup({isLocal:true});
                
                // It looks like there are three final events, and only one
                // will fire:
                // Fired after the first cache of the manifest.
                window.applicationCache.addEventListener('cached', function() {
                    self.ready();
                }, false);
                // Fired after the first download of the manifest.
                window.applicationCache.addEventListener('noupdate', function() {
                    self.ready();
                }, false);
                // Fired when there is a cache update ready.
                window.applicationCache.addEventListener('updateready', function() {
                    self.notifyInfo(self.get("updateMessage").loc());
                    // Display a reload button.
                    App.pageBodyController.addView(AppCacheRefreshView.create());
                    self.ready();
                }, false);
            }
        }
        else {
            // No cache, proceed like we're online.
            self.ready();
        }

    },
});
// export
exports.AppCacheController = AppCacheController;



/**
 * @class Provides the user an opportunity to refresh the page when the
 * application cache has been updated.
 * 
 * @extends Ember.View
 */
var AppCacheRefreshView = Ember.View.extend({
    /**
     * Which template is used for the summary.
     * @type {String}
     */    
    "templateName": 'appcacherefresh',
    
    /**
     * Handle click events on the view to refresh the page.
     */
    "click": function() {
        // This should work, but on iOS using Ember, the window.location.reload
        // isn't causing a page refresh, even though this click callback is
        // being called. The refresh is embedded in the template for now since
        // it works quite well.
        //window.location.reload();
    },
});
// export
//exports.AppCacheRefreshView = AppCacheRefreshView;


})(window);
