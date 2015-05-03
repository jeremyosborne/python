(function(exports) {



/**
 * @class The content of each day of the week in the daily summary view.
 * 
 * @extends Ember.Object
 */
var DailySummaryContent = Ember.Object.extend({    
    /**
     * The date this content is representing.
     * @type {ExtededDate}
     */
    "date": null,

    /**
     * List of objects of the form {"field": "blah", "value", blah} which
     * represent the stat names and values to show within the daily summary.
     * @type {Object[]}
     */
    "content": null,
        
    /**
     * Initialize properties.
     */
    "init": function() {
        this._super();
        if (!this.get("content")) {
            // Always make an array.
            this.set("content", [])
        }
    },
});
//window.DailySummaryContent = DailySummaryContent;



/**
 * @class Groups the daily content together by week.
 * 
 * @extends Ember.Object
 */
var DailySummaryContentByWeek = Ember.Object.extend({
    /**
     * Date when this week starts.
     * @type {ExtendedDate}
     */
    "from": null,
    
    /**
     * Date when this week ends.
     * @type {ExtendedDate}
     */
    "to": null,
        
    /**
     * One DailySummaryContent per day of the week.
     * [0] is Sunday, [6] is Saturday.
     * Must be set after construction via one of the population methods.
     * @type {DailySummaryContent[]}
     */
    "days": null,

    /**
     * Resets the content of the days property to be full of empty
     * DailySummaryContents.
     */
    "resetDays": function() {
            // Filled in order from Sunday [0] to Saturday [6].
        var days = [],
            // Counters
            dateCounter = this.get("from").copy(),
            i;
            
        for (i = 0; i < 7; i++) {
            days.push(DailySummaryContent.create({
                "date": dateCounter.copy()
            }));
            dateCounter.dayIncrement();
        }
        
        this.set("days", days);
    },
    
    /**
     * Populates this particular week of the daily summary content with
     * items from a passed in array.
     * 
     * @param collection {Stat[]} A clone of a stat collection that can be
     * modified by this particular method. Will populate this week with
     * the stats within the collection that fall within the week. Assumes that
     * collection is ordered in descending order, and will stop processing
     * on the first date that falls outside of the date boundaries of this
     * week. Side effect to the collection: elements will be removed from
     * the collection (shifted) if they fit within the week boundaries.
     * 
     * It is assumed all items in the collection have a "date" computed
     * property.
     * 
     * Will always reset the "days" property when called, with either a week
     * of empty DailySummaryContent objects, a mixed week of some empty
     * DailySummaryContent objects and some populated, or a full week of
     * populated DailySummaryContent objects.
     */
    "populate": function(collection) {
            // During computation, the days will be in inverse order 
            // (Saturday in index 0, Sunday in index 6).
        var days,
            // Counters
            i,
            weekToBoundary = this.get("to").copy(),
            date = collection[0].getField("date"),
            nextDateToFill;
        
        // If the first item in the collection does not fall into the
        // week brackets, then exit.
        if (weekToBoundary.isWithinWeek(date)) {
            // First figure out which day of the week we are on and pad any
            // days of the week in the array up to the day of the week.
            days = this._buildPaddedDayList(date);
            
            // Keep filling while we have items in the collection to fill
            // the week with and they are within our week and they are the
            // preceeding days.
            while (days.length < 7 && collection.length) {
                // On the first round, nextDateToFill is the date we're
                // starting with.
                // We rely on it being undefined on the first time through.
                nextDateToFill = (!nextDateToFill) ? date : nextDateToFill.copy().dayDecrement();
                
                if (nextDateToFill.isSameCalendarDate(date)) {
                    // The day previous to the date we just added is now.
                    days.push(DailySummaryContent.create({
                        // Date should be a copy here.
                        "date": nextDateToFill,
                        "content": collection.shift().getFieldValueList(true),
                    }));
                }
                else {
                    // We have an empty day, no statistics.
                    days.push(DailySummaryContent.create({
                        // Date should be a copy here.
                        "date": nextDateToFill,
                    }));
                }
                // Get the next date. If we've run out of items, this will
                // fail out on the next go round.
                date = collection.length && collection[0].getField("date");
            }
            
            // Fill with missing days, just in case we ran out of items in
            // our collection.
            while (days.length < 7) {
                nextDateToFill = days[days.length-1].get("date")
                    .copy().dayDecrement();
                days.push(DailySummaryContent.create({
                    // Date should be a copy here.
                    "date": nextDateToFill,
                }));
            }

            // Reverse the order of the days back to Sunday through Saturday.
            days.reverse();
            this.set("days", days);
        }
        else {
            // Fill with empty date containers.
            this.resetDays();
        }        
    },
    
    /**
     * Builds a list of days, padded with empty summary objects.
     * 
     * @param d {ExtendedDate} The date representing the day of the week
     * our days will begin on. NOTE: This function will not check to see
     * if d falls within our week boundaries, as it is assumed the caller of
     * the function has performed that necessary check.
     * @return {DailySummaryContent[]} A partially padded array of
     * DailySummaryContent objects, returned in inverse order 
     * (Saturday in index 0, Sunday in index 6). However, the array will
     * never be full of objects, as it will assume at least Sunday needs
     * to be filled in: at most the array will contain 6 objects.
     */
    "_buildPaddedDayList": function(d) {
            // JavaScript counts days from 0-6.
        var fillMax = 6,
            fillFrom = d.getDay(),
            // Always fill from Saturday
            dayCounter = d.weekEndDate();
            days = [];

        for (i = 0; i < (fillMax - fillFrom); i++) {
            // Start with saturday, and work backwards.
            days.push(DailySummaryContent.create({
                "date": dayCounter.copy(),
            }));
            dayCounter.dayDecrement();
        }
        
        // Remember, this is in inverse order with Saturday at [0].
        return days;
    },
        
    /**
     * Sets the date bookends. If a date argument is passed, the date
     * bookends will be set via the data argument.
     * @param d {ExtendedDate} The date around which to wrap the boundaries
     * of the week.
     */
    "setDateBoundaries": function(d) {
        this.set("from", d.weekStartDate());
        this.set("to", d.weekEndDate());
    },
    
    /**
     * Spawns another DailySummaryContentByWeek object that immediately
     * preceeds this particular week.
     * @return {DailySummaryContentByWeek} An instance with the week 
     * boundaries preset to the week preceeding the one represented by this
     * instance.
     */
    "spawnPreviousWeekInstance": function() {
        var prevWeekSeed = this.get("from").copy().dayDecrement();
        return DailySummaryContentByWeek.create({
            "from": prevWeekSeed.weekStartDate(),
            "to": prevWeekSeed.weekEndDate(),
        });
    },
    
    /**
     * Initialize the summary array.
     */
    "init": function() {
        this._super();
    },
});
// Export
exports.DailySummaryContentByWeek = DailySummaryContentByWeek;



/**
 * @class Formats the collection correctly so that empty days can be filled in 
 * as blanks in the view.
 * 
 * @example
 * var dailySummaryController = DailySummaryController.create({
 *     "cache": statsCache,
 * });
 * 
 * @extends Ember.ArrayProxy
 */
var DailySummaryController = Ember.ArrayProxy.extend({
    /**
     * Points to the associated view, created at init.
     * @type {DailySummaryView}
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
     * Subset of data made available for the view.
     * Data set is prepared and organized in reverse chronology.
     * @type {Stat[]}
     */
    "collection": null,
    
    /**
     * Observes and prepares content for the summary.
     */
    "collectionFactory": function() {
        // We trust that Ember will throttle how often this is fired.
        var hash,
            hashKeys,
            content,
            // Maximum number of days to view.
            // TODO: Need to add ability of view to see previous months.
            // or
            // need the ability to request a bracketed group of data from
            // the cache.
            maximumVisibleEntries = 30;

        if (this.get("showView")) {
            hash = this.get("cache").get("cache");
            hashKeys = Object.keys(hash);
            content = [];
            
            // Put content into reverse chronology.
            hashKeys.sort();
            hashKeys.reverse();
            // Build the object references.
            for (i = 0; i < hashKeys.length && i < maximumVisibleEntries; i++) {
                content[i] = hash[hashKeys[i]];
            }
            this.set("collection", content);  
        }
    }.observes("cacheChanged", "showView"),
    
    /**
     * Whether or not we should show the associated view.
     * @type {Boolean}
     */
    "showView": false,
    
    /**
     * Content for view consumption.
     * 
     * To accommodate the expectations of the view, the array might be
     * populated with empty objects representating days of the week that
     * have not yet occurred, but need to be made visible.
     * 
     * @type {Stat[]}
     */
    "content": Ember.computed(function() {
            // We need a mutable array for the view.
        var content = [],
            // Copy of collection, don't want to mess it up.
            collectionCopy,
            weeklyCollection,
            // Maximum number of weeks we'll show.
            totalWeeksShown = 4,
            i;
                        
        if (this.get("collection") && this.get("showView")) {
            // Copy of collection, don't want to mess up the original.
            collectionCopy = [].concat(this.get("collection"));
            
            for (i = 0; i < 4 && collectionCopy.length; i++) {
                // If first time, create new.
                if (!weeklyCollection) {
                    weeklyCollection = DailySummaryContentByWeek.create();
                    weeklyCollection.setDateBoundaries(collectionCopy[0].getField("date"));
                }
                else {
                    weeklyCollection = weeklyCollection.spawnPreviousWeekInstance();
                }
                // Populate will pop stats off of the collection copy.
                weeklyCollection.populate(collectionCopy);
                content.push(weeklyCollection);
            }
        }

        return content;
    }).property("collection", "showView").cacheable(),

    /**
     * Initialize associated view.
     */
    "init": function() {
        this._super();

        this.set("view", DailySummaryView.create({
            "controller": this,
        }));
    },

});
// Export
exports.DailySummaryController = DailySummaryController;



/**
 * @class A daily view that presents the available data across its
 * entire range of dates.
 * 
 * @example
 * // Initialize a view with the controller.
 * var dailySummaryView = DailySummaryView.create({
 *     "controller": dailySummaryController,
 * });
 * 
 * @extends Ember.View
 */
var DailySummaryView = Ember.View.extend({
    /**
     * Which template is used for the summary.
     * @type {String}
     */    
    "templateName": "dailysummary",

    /**
     * Who is our daddy?
     * @type {DailySummaryController}
     */
    "controller": null,
    
    /**
     * The content for our view.
     * @type {DailySummaryController}
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
//exports.DailySummaryView = DailySummaryView;



})(window);
