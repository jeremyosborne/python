(function(exports) {



/**
 * @class Handles the input of a calendar date. Intended to be included
 * in a container view acting as an input form.
 * 
 * @example
 * // Within the templates, one way of using this is to include
 * {{view UserInput_CalendarDate}}
 * // where the name value is available when iterating over the childViews
 * // of the parent view.
 * // If the default "name" value is not good enough for the form, it can be
 * // changed at creation time in the templates with:
 * {{view UserInput_CalendarDate name="otherDate"}}
 * 
 * @extends Ember.View
 */
var UserInput_CalendarDate = Ember.View.extend({
    /**
     * The template.
     * @type {String}
     */
    "templateName": "userinput_calendardate",
        
    /**
     * Prevent user input?
     * @type {Boolean}
     */
    "isDisabled": false,
    
    /**
     * The display label for this view.
     * @type {String}
     */
    "label": "_Date:".loc(),
    
    /**
     * The default "name" of this view, usually designed to correspond with
     * the field name of the stat that this data will be input into.
     * @type {String}
     */
    "name": "date",
    
    /**
     * Four digit representation of year.
     * Defaults to the current year.
     * @type {Number}
     */
    "year": null,
    
    /**
     * Numeric month (1 through 12).
     * Defaults to the current month.
     * @type {Number}
     */
    "month": null,
    
    /**
     * Day of month (1 through 31).
     * Defaults to the current day of the month.
     * @type {Number}
     */
    "day": null,
    
    /**
     * Date, in ISO Calendar Date format, formed from the user input.
     * If the input is obviously invalid on the form, or the view has never
     * been exposed to the user, the value of this will be null.
     * @type {String|Null}
     */
    "value": Ember.computed(function() {
        // The bindings of the view are one way only so we scrape the actual
        // HTML for the values.
        var year = this.$().find(".year").val(),
            month = parseInt(this.$().find(".month").val()) - 1,
            day = this.$().find(".day").val(),
            date = ExtendedDate(new Date(year, month, day));
        
        // Dates can return bad values, double check before returning.
        if (date.valueOf()) {
            return date.toISOCalendarDate();
        }
        else {
            return null;
        }
    }),
    
    /**
     * Increment the date by one day.
     */
    "increment": function() {
        // Get the date.
        var d = this.get("value");
        if (!d) {
            // If broken, reset to today before operating.
            this.resetDate();
            d = this.get("value");
        }
        // Convert ISO calendar date to an extended date.
        // Clean up the time to prevent dayling savings time problems.
        d = d.split("-");
        var d = ExtendedDate( new Date(d[0], d[1]-1, d[2], 12, 0, 0, 0) );
        
        d.dayIncrement();
                
        // Reset the date.
        this.set("year", d.getFullYear());
        // JavaScript months are 0-11, and we want human understandable.
        this.set("month", d.getMonth() + 1);
        this.set("day", d.getDate());
    },
    
    /**
     * Decrement the date by one day.
     */
    "decrement": function() {
        // Get the date.
        var d = this.get("value");
        if (!d) {
            // If broken, reset to today before operating.
            this.resetDate();
            d = this.get("value");
        }
        // Convert ISO calendar date to an extended date.
        // Clean up the time to prevent dayling savings time problems.
        d = d.split("-");
        var d = ExtendedDate( new Date(d[0], d[1]-1, d[2], 12, 0, 0, 0) );
        
        d.dayDecrement();
                
        // Reset the date.
        this.set("year", d.getFullYear());
        // JavaScript months are 0-11, and we want human understandable.
        this.set("month", d.getMonth() + 1);
        this.set("day", d.getDate());
    },
    
    /**
     * Sets the date of this field to a daylight savings immune date
     * (hopefully).
     */
    "resetDate": function() {
        // Set date to the local today.
        var d = new Date();
        
        // Set to noon time, which we hope circumvents missing gaps of time
        // when Daylight Savings time is enacted.
        d.setHours(12);
        
        this.set("year", d.getFullYear());
        // JavaScript months are 0-11, and we want human understandable.
        this.set("month", d.getMonth() + 1);
        this.set("day", d.getDate());
    },
    
    /**
     * Handle clicks on this control.
     * 
     * @param e {jQuery.Event} A jQuery event object.
     */
    "click": function(e) {
        // this points to our Ember.View instance.
        // this.$() points to the container (jQuery object) of our ember view.
        
        if ($(e.target).attr("data-button-role") == "decrement") {
            this.decrement();
        }
        else if ($(e.target).attr("data-button-role") == "increment") {
            this.increment();
        }
    },
    
    /**
     * Initialize the date in a way that should avoid any daylight savings
     * problems.
     */
    "init": function() {
        this._super();
        
        this.resetDate();
    },
});
// Export
exports.UserInput_CalendarDate = UserInput_CalendarDate;



})(window);
