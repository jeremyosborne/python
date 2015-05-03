(function(exports) {



/**
 * @class Handles information displayed in the main content portion of the
 * page.
 * 
 * @example
 * // Create, and that's all there is to it.
 * // Assumes the container already and always exists in the DOM.
 * var pageBodyController = PageBodyController.create({
 *     "containerSelector": "#app-body",
 * });
 * 
 * @extends Ember.Object
 */
var PageBodyController = Ember.Object.extend({
    /**
     * CSS selector that corresponds to the container on the page.
     * This must be set at creation time or things won't work.
     * @type {String}
     */
    "containerSelector": null,

    /**
     * The container view managed by this controller.
     * Constructed within the init.
     * @type Ember.ContainerView
     */
    "_view": null,

    /**
     * Add a view that we wish to show in the content body.
     * @param view {Ember.View} A view to append to the content.
     */
    "addView": function(view) {
        this.get("_view").get("childViews").pushObject(view);
    },
    
    /**
     * Clears the body view. Also removes all references this controller, and
     * managed container view, have to any previously added views.
     */
    "clearViews": function() {
        var childViews = this.get("_view").get("childViews"),
            // Not sure how removeObject deals with the stack of views,
            // but assume removeObject is just like pop().
            childViewsCopy = [].concat(childViews),
            i;
        
        // Not sure if this is necessary with ember, but just in case
        
        for (i = 0; i < childViewsCopy.length; i++) {
            childViews.removeObject(childViewsCopy[i]);
        }
    },
    
    /**
     * Init phase.
     */
    "init": function() {
        var container = Ember.ContainerView.create();
        
        this._super();
        
        container.appendTo(this.get("containerSelector"));
        this.set("_view", container);
    },
        
});
// Export
exports.PageBodyController = PageBodyController;



})(window);
