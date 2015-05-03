(function(exports) {



/**
 * @class Minimal proxy for web storage. Allows JSON friendly objects, not
 * just strings.
 * 
 * The following keys have been claimed by other objects in the localStorage:
 * -> currentStatName {String} Used by the statsCache to remember what was the
 * last chosen stat to work with.
 * -> statsDescriptions {Object} Used by the statsCache to remember the
 * model descriptions for offline use.
 * 
 * @extends Ember.Object
 * @extends LoggerMixin
 * @extends NotificationsMixin
 */
var DataCache = Ember.Object.extend(LoggerMixin, NotificationsMixin, {
    
    /**
     * Places the key:value pair into localStorage. The value will be run
     * through JSON.stringify prior to being placed into localStorage.
     * 
     * Will deliver and log a warning if the save to localStorage failed.
     * 
     * @param key {String} Key on which to store within localStorage.
     * @param value {mixed} A JSON friendly object to store within 
     * localStorage.
     * @return {Boolean} true if the write was successful, false if not.
     */
    "put": function(key, value) {
        try {
            value = JSON.stringify(value);
            localStorage[key] = value;
            // success
            return true;
        } catch(e) {
            // user notification.
            this.notifyError("_ERROR saving key:value to cache: %@:%@".loc(
                [key, value]
            ));
            // And log the output for debugging.
            this.log("_ERROR saving key:value to cache: %@:%@".loc(
                [key, value]
            ));
            // fail
            return false;
        }
    },
    
    /**
     * Returns the value of a particular key from localStorage. The value
     * will be run through JSON.parse prior to being returned.
     * 
     * @param key {String} Key from which to retrieve localStorage data.
     * @return {mixed} The JSON friendly datatype, or undefined, for the 
     * particular key.
     */
    "pull": function(key) {
        var value = localStorage[key];
        if (value !== undefined) {
            // JSON.parse doesn't like undefined.
            value = JSON.parse(value);
        }
        return value;
    },
    
    /**
     * Removes a particular key and associated value from the localStorage.
     * @param key {String} Key which to remove from localStorage, along with
     * any associated value.
     */
    "del": function(key) {
        localStorage.removeItem(key);
    },
    
    /**
     * Clears all values stored in localStorage.
     */
    "drop": function() {
        localStorage.clear();
    },
    
    /**
     * Initialize listeners on the application cache.
     */
    "init": function() {
        this._super();
    },
});
// export
exports.DataCache = DataCache;



})(window);
