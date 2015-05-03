(function(exports) {



/**
 * @class Controller for the data entry form.
 * 
 * @example
 * // Need to be bound to the collection.
 * var statEntryController = StatEntryController({
 *     "cache": statsCache,
 * });
 * 
 * @extends Ember.Object
 * @extends LoggerMixin
 * @extends NotificationsMixin
 */
var StatEntryController = Ember.Object.extend(LoggerMixin, NotificationsMixin, {
    /**
     * Points to the associated view, created at init.
     * @type {StatEntryView}
     */
    "view": null,
    
    /**
     * Cache we are bound to.
     * @type {StatsCache}
     */
    "cache": null,

    /**
     * Used to notify us when things have changed.
     * @type {Number}
     */
    "cacheChangedBinding": "*cache.revision",
    
    /**
     * Describes the fields associated with this stat.
     * @type {StatDescription}
     */
    "statDescription": null,
    
    /**
     * The set of potential values for this statistic, mapped to the field
     * names.
     * @type {Object}
     */
    "statValues": null,
        
    /**
     * Whether or not the controller is attempting to submit data.
     * When not submitting, this is an empty string.
     * Valid values for submission are "save" or "delete".
     * @type {String}
     */
    "isSubmitting": "",
    
    /**
     * Watches for the most recent number of layers.
     */
    "layerUpdate": Ember.observer(function() {
        /* 
         * TODO: Rewrite to set default values based on the last entered
         * cache values.
        var hash = this.get("cache").get("cache"),
            hashKeys = Object.keys(hash),
            i;
        
        // Find the largest value, ascending order.
        hashKeys.sort();
        
        // We assume that the collection is sorted in reverse chronology.
        if (hashKeys && hashKeys.length) {
            // Only reset the layers with the most recently saved number
            // of layers.
            this.set("layers", hash[hashKeys[hashKeys.length-1]].get("layers"));
        }
         */
    }, "cacheChanged"),

    /**
     * Perform a save if and when we are signaled that it is time to save.
     */
    "send": Ember.observer(function() {
        var self = this,
            submit = self.get("isSubmitting"),
            dataPackage;
            
        if (submit == "save") {
            // A create and an update still "saves" to this app.
            self.notifyInfo("_Saving...".loc());
            // Need the stat values and the statName
            dataPackage = this.get("statValues");
            dataPackage["statName"] = this.get("cache").get("currentStatName");
            $.ajax(ldlsConf.saveURL, {
                "dataType": "json",
                "type": "POST",
                "data": dataPackage,
                "success": function(data) {
                    if (data.stat && !data.error) {
                        self.get("cache").add(data.stat);                        
                        self.notifyInfo("_Saved Successfully".loc());
                    }
                    else {
                        self.notifyError("_ERROR: During save call to server.".loc())
                        self.notifyError(data.error);
                    }

                    // Signal that we're done, one way or another.
                    self.set("isSubmitting", "");
                },
                "error": function() {
                    self.notifyError("_ERROR: $.ajax error function being called during save".loc());
                    // DEBUG
                    self.log("_ERROR: $.ajax error function being called during save".loc());
                    self.log(arguments);
                },
            });
        }     
        else if (submit == "delete") {
            // Removes a record from the database.
            self.notifyInfo("_Deleting...".loc());
            $.ajax(ldlsConf.deleteURL, {
                "dataType": "json",
                "type": "POST",
                "data": self.get("statValues"),
                "success": function(data) {
                    
                    if (data.stat && !data.error) {
                        self.get("cache").remove(data.stat.date);                        
                        self.notifyInfo("_Deleted Successfully".loc());
                    }
                    else if (data.error) {
                        self.notifyError("_ERROR: During delete call to server.".loc())
                        self.notifyError(data.error);
                    }
                    // Else, do nothing if there was nothing to actually delete.
                    
                    // Signal that we're done, one way or another.
                    self.set("isSubmitting", "");
                },
                "error": function() {
                    self.notifyError("_ERROR: $.ajax error function being called during delete.".loc());
                    // DEBUG
                    self.log("_ERROR: $.ajax error function being called during delete.".loc())
                    self.log(arguments);
                },
            });
        }
    }, "isSubmitting"),
    
    /**
     * Initialize associated view.
     */
    "init": function() {
        var schema = this.get("cache").get("currentStatDescription"),
            fields = schema.getFields(),
            i;
        
        this._super();
        
        // Validator and general schema.
        this.set("statDescription", schema);
        
        // Convert the fields to default values for use in the view.
        for (i in fields) {
            if (fields.hasOwnProperty(i)) {
                // Convert the type of the field and map over the field
                // value descriptors with actual default values.
                fields[i] = schema.getFieldDefaultValue(fields[i]);
            }
        }
        this.set("statValues", fields);        

        this.set("view", StatEntryView.create({
            "controller": this,
        }));
    },

});
// Export
exports.StatEntryController = StatEntryController;



/**
 * @class View for entering new data points.
 * 
 * @example
 * // The View binds to the controller we pass in, using two way bindings
 * // to update data.
 * var statEntryView = StatEntryView.create({
 *     "controller": myApp.statEntryController,
 * });
 * 
 * @extends Ember.View
 */
var StatEntryView = Ember.View.extend({
    /**
     * Which template is used for the summary.
     * @type {String}
     */
    "templateName": "statentry",

    /**
     * Controller we are working with.
     * @type {StatEntryController}
     */
    "controller": null,

    /**
     * Container for our user inputs.
     * Created within init.
     * @type {Ember.ContainerView}
     */
    "userInputContainer": null,

    /**
     * Allows us to signal when a submission has been made.
     * When not submitting, this is an empty string.
     * Valid values for submission are "save" or "delete".
     * @type {String}
     */
    "isSubmittingBinding": "*controller.isSubmitting",

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

            // Did we click a submit button?
        var action = e.target.getAttribute("data-button-role"),
            type = e.target.type,
            // Property names we wish to update from the form.
            childViews,
            // Go directly to the controller to get the hash.
            values,
            i;

        // Just in case the template doesn't kill the action.
        e.preventDefault();
                
        // Walk through the childviews.
        if (type == "submit" && action && !this.get("isSubmitting")) {
            // Define here not above. Seems to help performance on iPhone,
            // or maybe I'm hallucinating.
            childViews = this.get("userInputContainer").get("childViews");
            values = this.get("controller").get("statValues");

            // Signal user attempted to submit, but only if we've clicked
            // a submit button.
            for (i = 0; i < childViews.length; i++) {
                values[childViews[i].get("name")] = childViews[i].get("value");
            }
            
            // Push information back to controller.
            this.get("controller").set("fieldValues", values);
            this.set("isSubmitting", action);
        }
    },
    
    "didInsertElement": function() {
        // This is a bit janky, but if I want dynamic, gotta work for it.
        this.get("userInputContainer").appendTo("#stat-entry-user-input");
    },
    
    /**
     * Initialize properties.
     */
    "init": function() {
        this._super();

        var containerView = Ember.ContainerView.create(),
            // Fucking bindings aren't ready yet, god damnit. Go straight to 
            // the controller to get the data. Do not pass go. Which makes
            // me question why do I need the bindings?
            // NOTE: Got rid of the corresponding bindings before checking
            // in this new code, hence this comment probabably seems a bit
            // out of place.
            fields = this.get("controller").get("statDescription").getFields(),
            // We assume the values are set going into the function.
            values = this.get("controller").get("statValues"),
            name;
        
        this.set("userInputContainer", containerView);
        
        // Setup the dynamic user inputs required for this stat.
        
        // Date always goes at the top, and we always expect a date.
        if (fields["date"]) {
            // NOTE: We're assuming the date is always today for now,
            // and that it always has the default label.
            containerView.get("childViews").pushObject(
                UserInput_CalendarDate.create()
            );
            // Fields had better be a copy.
            delete fields["date"];
        }
        
        for (name in fields) {
            if (fields.hasOwnProperty(name)) {
                // Map fields to field types.
                if (fields[name] == "uint") {
                    containerView.get("childViews").pushObject(
                        UserInput_Number.create({
                            "label": name.toTitleCase(),
                            "name": name
                        })
                    );                    
                }
                else {
                    // Should never get here.
                    throw new Error("StatEntryView recieved unknown key/value " + name + ": " + fields[name])
                }
            }
        }
        
    },
});
// Export
//exports.StatEntryView = StatEntryView;



})(window);
