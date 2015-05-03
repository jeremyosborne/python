(function(exports) {
/**
 * @class Basic logging functions designed to be mixed into objects.
 * 
 * @extends Ember.mixin
 * @name LoggerMixin
 */
var LoggerMixin = Ember.Mixin.create({
    /**
     * Basic logging mechanism.
     * @param message {String|Object} Item to send to output.
     */
    "log": function(message) {
        if (window.console && console.log) {
            console.log(message);
        }
    },
});
// Export
exports.LoggerMixin = LoggerMixin;

})(window);
