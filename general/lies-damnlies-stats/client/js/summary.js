(function(exports) {



/**
 * @class Provides summary data from the statistics on hand.
 * 
 * @example
 * var summaryController = SummaryController.create({
 *     "cache": statsCache,
 * });
 * 
 * @extends Ember.Object
 */
var SummaryController = Ember.Object.extend({    
    /**
     * Points to the associated view, created at init.
     * @type {SummaryView}
     */
    "view": null,

    /**
     * Must point to a collection of statistics.
     * @type {StatsCache}
     */
    "cache": null,
    
    /**
     * Used to notify us when things have changed.
     * @type {Number}
     */
    "cacheChangedBinding": "*cache.revision",

    /**
     * The content that we have access to at the moment.
     * Data should be in chronological descending order.
     * @type {Stat[]}
     */
    "content": null,

    /**
     * Observes and prepares content for the summary.
     */
    "contentFactory": function() {
        // We trust that Ember will throttle how often this is fired.
        var hash,
            hashKeys,
            content;

        if (this.get("showView")) {
            hash = this.get("cache").get("cache");
            hashKeys = Object.keys(hash);
            content = [];
            
            // Put content into reverse chronology.
            hashKeys.sort();
            hashKeys.reverse();
            // Build the object references.
            for (i = 0; i < hashKeys.length; i++) {
                content[i] = hash[hashKeys[i]];
            }
            this.set("content", content);            
        }
    }.observes("cacheChanged", "showView"),

    /**
     * Whether or not we should show the associated view.
     * @type {Boolean}
     */
    "showView": false,

    /**
     * Those that wish a summary of statistics should observe this property.
     * 
     * The statistics provided are:
     * totals {Object[]} -> A list of the totals.
     *     Dates are counted (representing total number of days recorded).
     *     Numbers are summed.
     * averages {Object[]} ->. A list of the averages.
     *     Dates are ignored.
     *     Numbers are averaged across all records (days).
     * @type {Object}
     */
    "summary": Ember.computed(function() {
        var content = this.get("content"),
            numModels = content && content.length,
            summary = {
                "totals": [],
                "averages": [],
            },
            fields = this.get("cache").get("currentStatDescription").getFields(),
            i;
            
        if (content && numModels && this.get("showView")) {
            for (i in fields) {
                if (fields.hasOwnProperty(i)) {
                    if (fields[i] == "isocalendardate") {
                        // Totals only
                        summary.totals.push({
                            //"field": i.toTitleCase(),
                            // NOTE: Make the name better
                            "field": "# Stats",
                            // NOTE: Simple assumption.
                            "value": content.length,
                        });
                    }
                    else if (fields[i] == "uint") {
                        // Totals and averages.
                        summary.totals.push({
                            "field": i.toTitleCase(),
                            "value": content.reduce(function(a, b) {
                                return a + b.getField(i);
                            }, 0)
                        });
                        
                        summary.averages.push({
                            "field": i.toTitleCase(),
                            "value": (function() {
                                var total = 0,
                                    totalDays = 0;
                                
                                // For us, averages are always against days.
                                content.forEach(function(model) {
                                    total += model.getField(i);
                                    totalDays += 1;
                                });
                                
                                return total / totalDays;
                            })()
                        });
                    }
                }
            }                                    
        }

        return summary;
    }).property("content", "showView").cacheable(),

    /**
     * Initialize associated view.
     */
    "init": function() {
        this._super();

        this.set("view", SummaryView.create({
            "controller": this,
        }));
    },

});
// Export
exports.SummaryController = SummaryController;



/**
 * @class View a summary of the statistics.
 * 
 * @example
 * // To use, set the contentBinding to a summary controller.
 * var summaryView = SummaryView.create({
 *     "controllerBinding": "summaryController.content",
 * });
 * 
 * @extends Ember.View
 */
var SummaryView = Ember.View.extend({
    /**
     * The content for our view.
     * @type {SummaryController}
     */
    "contentBinding": "*controller.summary",

    /**
     * Whether or not we should compute and display the calendar view.
     * @type {Boolean}
     */
    "showViewBinding": "*controller.showView",

    /**
     * Which template is used for the summary.
     * @type {String}
     */
    "templateName": 'summary',
    
    /**
     * Listen for a click on the view.
     * @param e {jQuery.Event} A jQuery event object.
     */
    "click": function(e) {
        // The argument to the callback will be a jQuery Event object.
        // The "this" of our callback will point to our Ember.View instance.
        // If within our callback we wish to get access to a jQuery Object
        // version of the DOM container element for our view, use this.$().
        
        var action = e.target.getAttribute("data-button-role");
        if (action == "toggle-view") {
            this.set("showView", !this.get("showView"));
        }
    },
});
// Export
//exports.SummaryView = SummaryView;



})(window);
