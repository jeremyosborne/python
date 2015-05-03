(function(exports) {



/**
 * @class View for the footer menu.
 * 
 * @example
 * // To use, we need a reference to the state manager.
 * var summaryView = SummaryView.create({
 *     "stateManager": myStateManager,
 * });
 * 
 * @extends Ember.View
 */
var FooterMenuView = Ember.View.extend({
    /**
     * Which template is used for the summary.
     * @type {String}
     */
    "templateName": 'footermenu',
    
    /**
     * The state manager that we can use to respond to events.
     * @type {StateManager}
     */
    "stateManager": null,
    
    /**
     * Listen for a click on the view.
     * @param e {jQuery.Event} A jQuery event object.
     */
    "click": function(e) {
        // The argument to the callback will be a jQuery Event object.
        // The "this" of our callback will point to our Ember.View instance.
        // If within our callback we wish to get access to a jQuery Object
        // version of the DOM container element for our view, use this.$().
        
        var stateChange = e.target.getAttribute("data-state-change");
        if (stateChange) {
            this.get("stateManager").goToState(stateChange);
        }
    },
});
// Export
exports.FooterMenuView = FooterMenuView;



})(window);
