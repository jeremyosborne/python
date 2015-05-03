(function(exports) {



/**
 * @class Handles the input of number greater than or equal to zero. 
 * Intended to be included in a container view acting as an input form.
 * 
 * @example
 * // Within the templates, one way of using this is to include
 * {{view UserInput_Number}}
 * // where the name value is available when iterating over the childViews
 * // of the parent view.
 * // If the default "name" value is not good enough for the form, it can be
 * // changed at creation time in the templates with:
 * {{view UserInput_Number label="# of things" name="thisNumber"}}
 * 
 * @extends Ember.View
 */
var UserInput_Number = Ember.View.extend({
    /**
     * The template.
     * @type {String}
     */
    "templateName": "userinput_number",
        
    /**
     * Prevent user input?
     * @type {Boolean}
     */
    "isDisabled": false,
    
    /**
     * The display label for this view.
     * @type {String}
     */
    "label": "_Number:".loc(),
    
    /**
     * The default "name" of this view, usually designed to correspond with
     * the field name of the stat that this data will be input into.
     * @type {String}
     */
    "name": "number",
    
    /**
     * The value of the field.
     * @type {Number}
     */
    "number": "",

    /**
     * The value of the field.
     * If the input is obviously invalid on the form, or the view has never
     * been exposed to the user, the value of this will be null.
     * @type {Number|Null}
     */
    "value": Ember.computed(function() {
        // The bindings of the view are one way only so we scrape the actual
        // HTML for the values.
        // NOTE: This garbage parsing is to goad iOS Safari 5.1.1 into
        // displaying a numeric keyboard, and at the same time make sure that
        // if the browser inserts any commas for long numbers that the
        // commas are removed.
        var number = parseInt((this.$().find(".number").val() + "").replace(",", ""));
        
        // Dates can return bad values, double check before returning.
        if (!isNaN(number) && number >= 0) {
            return number;
        }
        else {
            return null;
        }
    }),

    /**
     * Increment the number by one.
     */
    "increment": function() {
        // Get the number
        var n = this.get("value");
        if (!n) {
            // If broken, set to a min of zero.
            n = 0;
        }
        n += 1;                
        this.set("number", n);
    },

    /**
     * Decrement the number by one, with a minimum of zero.
     */
    "decrement": function() {
        // Get the number
        var n = this.get("value");
        if (!n) {
            // If broken, set to a min of zero.
            n = 0;
        }
        n -= 1;
        
        // Unsigned integers only.
        n = n > 0 ? n : 0;
        
        this.set("number", n);
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

});
// Export
exports.UserInput_Number = UserInput_Number;



})(window);
