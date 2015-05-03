(function(exports) {



/**
 * @class Handles the information displayed in the header of the page. 
 * Insantiates the view directly.
 * 
 * @example
 * var pageHeaderController = PageHeaderController.create({
 *     "containerSelector": "#app-header",
 * });
 * 
 * @extends Ember.Object
 */
var PageHeaderController = Ember.Object.extend({
    /**
     * CSS selector that corresponds to the container on the page.
     * If not supplied, no visual header updates will occur.
     * @type {String}
     */
    "containerSelector": null,

    /**
     * The message to display in the header, .set() this to change the display
     * of the header.
     * Can be an HTML string.
     * @type {String}
     */
    "content": "",

    /**
     * Observes the content property and causes the heading on the page
     * to change when the content changes.
     */
    "contentObserver": Ember.observer(function() {
        var selector = this.get("containerSelector");
        if (selector) {
            // Only try to update if we have a selector.
            $(selector).empty().html(this.get("content"));
        }
    }, "content"),
        
});
// Export
exports.PageHeaderController = PageHeaderController;



})(window);
