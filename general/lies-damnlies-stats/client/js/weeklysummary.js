(function(exports) {

/**
 * @class Content for the weekly summary view.
 * 
 * @extends Ember.Object
 */
var WeeklySummaryContent = Ember.Object.extend({
    /**
     * Date when this week starts.
     * @type {Date}
     */
    "from": null,
    
    /**
     * Date when this week ends.
     * @type {Date}
     */
    "to": null,
    
    /**
     * Key:value pairs of summarized data, specifically for the limited
     * capabilities of the templating.
     * Each object is a {"field": "blah", "value", blah} colleciton, much
     * friendly for an Ember.Template.
     * @type {Object[]}
     */
    "mappedSummary": Ember.computed(function() {
        // Getter only.
        var m = [],
            summary = this.get("summary"),
            i;
        
        for (i in summary) {
            if (summary.hasOwnProperty(i)) {
                m.push({
                    "field": i.toTitleCase(),
                    "value": summary[i],
                })
            }
        }
        
        return m;
    }).property("summary"),
    
    /**
     * Key:value pairs of summarized data for this week.
     * @type {Object}
     */
    "summary": null,
    
    /**
     * Initialize the summary array.
     */
    "init": function() {
        this._super();
        this.set("summary", {});
    }
});
// Export
//exports.WeeklySummaryContent = WeeklySummaryContent;



/**
 * @class Organizes data into weekly summaries.
 * 
 * @example
 * var weeklySummaryController = WeeklySummaryController.create({
 *     "cache": statsCache,
 * });
 * 
 * @extends Ember.ArrayProxy
 */
var WeeklySummaryController = Ember.ArrayProxy.extend({
    /**
     * Points to the associated view, created at init.
     * @type {WeeklySummaryView}
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
     * Reference collection of models.
     * 
     * Collection should be sorted in reverse chronological order.
     * 
     * @type {Stat[]}
     */
    "collection": null,
    
    /**
     * Observes and prepares content for the summary.
     */
    "collectionFactory": Ember.observer(function() {
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
            this.set("collection", content);
        }
    }, "cacheChanged", "showView"),
    
    /**
     * Whether or not we should show the associated view.
     * @type {Boolean}
     */
    "showView": false,
    
    /**
     * Content for view consumption.
     * 
     * To accomodate the expectations of the view, the array might be
     * populated with empty objects representating weeks with no data.
     * 
     * @type {Stat[]}
     */
    "content": Ember.computed(function() {
            // We need a mutable array for the view.
        var viewContent = [],
            // Copy of collection, don't want to mess it up.
            collectionCopy,
            // Will act as the boundaries of the week.
            weekBoundary,
            // summary content for the week.
            weeklySummaryContent,
            // loop counters
            stat,
            statFields,
            name,
            i;

        // NOTE: We assume that the collection data 
        if (this.get("collection") && this.get("collection").length && this.get("showView")) {
            // Copy of collection, don't want to mess it up.
            collectionCopy = [].concat(this.get("collection"));

            // Always start from most current week on the off chance that
            // dates are far into the future or past.
            weekBoundary = collectionCopy[0].getField("date").copy();                
            
            // Count backwards until finding data, filling in each week.
            // Stop when we're out of information from the collection.
            // NOTE: Maximum of 10 for now.
            for (i = 0; i < 10 && collectionCopy.length; i++) {                
                
                weeklySummaryContent = WeeklySummaryContent.create({
                    "from": weekBoundary.weekStartDate(),
                    "to": weekBoundary.weekEndDate(),
                });
                
                if (weekBoundary.isWithinWeek(collectionCopy[0].getField("date"))) {
                    do {
                        stat = collectionCopy.shift();
                        statFields = stat.get("description").getFields();
                        for (name in statFields) {
                            // FIX ME!!!
                            // Start from here. This is pretty fucked up,
                            // and slow. I think this needs to be paged,
                            // too, just like the daily summary view.
                            // FIX ME!!!!
                            
                            // NOTE: Ignore "date" fields.
                            // NOTE: Right now we assume only "uint" values.
                            if (statFields.hasOwnProperty(name) && (name !== "date")) {
                                if (weeklySummaryContent.get("summary")[name]) {
                                    weeklySummaryContent.get("summary")[name] +=
                                        stat.getField(name);                                        
                                }
                                else {
                                    weeklySummaryContent.get("summary")[name] = stat.getField(name);
                                }
                            }
                        }
                    } while (collectionCopy.length && 
                        weekBoundary.isWithinWeek(collectionCopy[0].getField("date")));
                }
                
                // Add the content for the week, empty or not.
                viewContent.push(weeklySummaryContent);
                // Previous week, see if we have any candidates next round.
                weekBoundary.weekDecrement();
                
            }
        }

        return viewContent;
    }).property("collection", "showView").cacheable(),

    /**
     * Initialize associated view.
     */
    "init": function() {
        this._super();

        this.set("view", WeeklySummaryView.create({
            "controller": this,
        }));
    },

});
// Export
exports.WeeklySummaryController = WeeklySummaryController;



/**
 * @class A presentation of statistics in a by-week format.
 * 
 * @example
 * // Initialize a view with the controller
 * var weeklySummaryView = WeeklySummaryView.create({
 *     "controller": weeklySummaryController,
 * });
 * 
 * @extends Ember.View
 */
var WeeklySummaryView = Ember.View.extend({
    /**
     * Which template is used for the summary.
     * @type {String}
     */    
    "templateName": 'weeklysummary',

    /**
     * Who is our daddy?
     * @type {WeeklySummaryController}
     */
    "controller": null,
    
    /**
     * The content for our view.
     * @type {WeeklySummaryController}
     */
    "contentBinding": "*controller",

    /**
     * Whether or not we should compute and display the calendar view.
     * @type {Boolean}
     */
    "showViewBinding": "*controller.showView",

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
//exports.WeeklySummaryView = WeeklySummaryView;

})(window);
