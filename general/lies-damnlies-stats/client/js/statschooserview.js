(function(exports) {

/**
 * @class View for choosing which stat the user will be dealing with.
 * 
 * @example
 * // The View binds to the controller we pass in, using two way bindings
 * // to update data.
 * var statsChooserView = StatsChooserView.create({
 *     "controller": myApp.statsCache,
 * });
 * 
 * @extends Ember.View
 */
var StatsChooserView = Ember.View.extend({
    /**
     * Which template is used for the summary.
     * @type {String}
     */
    "templateName": "statschooser",

    /**
     * Controller object we are working with.
     * @type {StatsCache}
     */
    "controller": null,

    /**
     * A list of the available stats by name.
     * @type {String[]}
     */
    "availableStatsNames": Ember.computed(function() {
        // We assume that statsDescriptions always exists as at least an
        // empty object.
        return Object.keys(this.get("controller").get("statsDescriptions"));
    }).property(),
    
    /**
     * Listen for a click on the form, and then handle it according to the
     * target that was clicked.
     * 
     * @param e {jQuery.Event} A jQuery event object.
     */
    "click": function(e) {
        // NOTE: When a view contains a callable property that matches a possible 
        // event type for the view -- "click", "submit", etc. -- ember will
        // intercept the original DOM event and delegate the event to our
        // callback function of the same name. 
        // The argument to the callback will be a jQuery Event object.
        // The "this" of our callback will point to our Ember.View instance.
        // If within our callback we wish to get access to a jQuery Object
        // version of the DOM container element for our view, use this.$().

        var el = this.$();
        var statName;

        // Just in case the template doesn't kill the action.
        e.preventDefault();
        
        // Walk through the childviews.
        // Signal user attempted to submit, but only on a button click.
        if (e.target.getAttribute("data-button-role") == "choose") {
            // Get the select element.
            statName = el.find("select.userinput :selected").val();
            
            // We force observers to fire by changing the statName to
            // null first.
            this.get("controller").set("currentStatName", null);
            this.get("controller").set("currentStatName", statName);
            
            /*
                TEST CODE for testing this view.
            
                var s = StatsCache.create();
                s.loadStatsDescriptions();
                scv = StatsChooserView.create({ "controller": s });
                scv.append();
            
             */
        }
    },
});
// Export
exports.StatsChooserView = StatsChooserView;

})(window);
