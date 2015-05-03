(function(exports) {



/**
 * @class Provides login opportunity to the user.
 * Insantiates the associated view programmatically.
 * 
 * @example
 * var loginController = LoginController.create();
 * // To get access to the associated view.
 * var loginView = loginController.get("view");
 * 
 * @extends Ember.Object
 * @extends LoggerMixin
 * @extends NotificationsMixin
 */
var LoginController = Ember.Object.extend(LoggerMixin, NotificationsMixin, {
    /**
     * Points to the login view, created at init.
     * @type {LoginView}
     */
    "view": null,
    
    /**
     * The username to authenticate with.
     * @type {String}
     */
    "username": "",

    /**
     * The password to authenticate with.
     * @type {String}
     */
    "password": "",

    /**
     * The current user profile, or null if the user is not logged in.
     * @type {Object}
     */
    "userProfile": null,

    /**
     * Which revision is the cache on?
     * 
     * This is really here because I can't find a reasonable way in Ember
     * 0.9.5 to manage a hash directly through observers.
     * Usage:
     * Have other objects bind observers to the revision property. When
     * revision changes, and it will only ever increase over time, it signals
     * that there was some change to the cache. It is the observers job to
     * figure out what to do with the changes, as no diff is provided.
     * @type {Number}
     */
    "revision": 0,

    /**
     * Whether or not the controller is attempting to submit data.
     * When not submitting, this is an empty string.
     * Valid values for submission are "login" or "logout".
     * @type {String}
     */
    "isSubmitting": "",
    
    /**
     * Check to see if the current user is authorized.
     */
    "checkAuth": function() {
        var self = this;
        
        // Test our authentication, we might be good to go.
        $.ajax(ldlsConf.authInfoURL, {
            "dataType": "json",
            "type": "POST",
            // No data.
            "success": function(data) {
                if (data && !data.error && data.auth) {
                    // Assume that we got user information back if we made it
                    // here. We want the code to explode if data.info is
                    // not populated, as at this point data.info should always
                    // be populated.
                    self.set("userProfile", data.info);
                    // This is our signal that we have a new revision and 
                    // that observers should update themselves.
                    self.set("revision", self.get("revision") + 1);
                }
                else {
                    // TODO: This will likely change when we have offline
                    // mode, which will likely be handled within the outer
                    // error callback.
                    
                    // Anything within this block signals a failed auth.
                    self.set("userProfile", null);
                    // This is our signal that we have a new revision and 
                    // that observers should update themselves.
                    self.set("revision", self.get("revision") + 1);
                    
                    if (data && data.error)  {
                        // Some form of benign error, but still an error.
                        // Really, shouldn't get here.
                        self.notifyError("_ERROR: in checkAuth: ".loc() + data.error.loc());
                    }
                    else if (!data) {
                        // More serious error. Shouldn't get here.
                        self.notifyError("_ERROR: in checkAuth: should never reach here. Please report.".loc());
                        // DEBUG
                        self.log("_ERROR: in checkAuth: should never reach here. Please report.".loc());
                        self.log(arguments);
                    }
                    // Otherwise, it's just a failed auth attempt.
                }
            },
            "error": function() {
                // We have a full blown error. Right now, don't attempt to
                // recover.
                self.notifyError("_ERROR: $.ajax error function being called during checkAuth.".loc());
                // DEBUG
                self.log("_ERROR: $.ajax error function being called during checkAuth.".loc());
                self.log(arguments);
            },
        });
    },
        
    /**
     * Attempt an authentication.
     */
    "login": Ember.observer(function() {
        var submit = this.get("isSubmitting"),
            self = this;
        
        if (submit == "login") {
            $.ajax(ldlsConf.authLoginURL, {
                "dataType": "json",
                "type": "POST",
                "data": {
                    "username": self.get("username"),
                    "password": self.get("password"),
                },
                "success": function(data) {
                    if (data && !data.error && data.auth) {                        
                        // Assume that we got user information back if we made it
                        // here. We want the code to explode if data.info is
                        // not populated, as at this point data.info should always
                        // be populated.
                        self.set("userProfile", data.info);
                        // This is our signal that we have a new revision and 
                        // that observers should update themselves.
                        self.set("revision", self.get("revision") + 1);
                    }
                    else {
                        // TODO: This will likely change when we have offline
                        // mode, which will likely be handled within the outer
                        // error callback.
                        
                        // Anything within this block signals a failed auth.
                        self.set("userProfile", null);
                        // This is our signal that we have a new revision and 
                        // that observers should update themselves.
                        self.set("revision", self.get("revision") + 1);

                        if (data && data.error) {
                            // Logins may cause errors, which is natural.
                            // Display sanitized server message.
                            self.notifyError(data.error.loc());
                        }
                        else {
                            // More serious error. Shouldn't get here,
                            // server should always return an error on a
                            // failed login attempt.
                            self.notifyError("_ERROR: in login: should never reach here. Please report.".loc());
                            // DEBUG
                            self.log("_ERROR: in login: should never reach here. Please report.".loc());
                            self.log(arguments);
                        }

                    }
        
                    // Signal that we're done, one way or another.
                    self.set("isSubmitting", "");
                },
                "error": function() {
                    self.notifyError("_ERROR: $.ajax error function being called during login.".loc());
                    // DEBUG
                    self.log("_ERROR: $.ajax error function being called during login.".loc());
                    self.log(arguments);

                    // Signal that we're done, one way or another.
                    self.set("isSubmitting", "");
                },
            });
        }
    }, "isSubmitting"),

    /**
     * Initialize associated view.
     */
    "init": function() {
        this._super();

        this.set("view", LoginView.create({
            "controller": this,
        }));
    },

});
// Export
exports.LoginController = LoginController;



/**
 * @class View to accept user login credentials.
 * 
 * @example
 * // The View binds to the controller we pass in, using two way bindings
 * // to update data.
 * var loginView = LoginView.create({
 *     "controller": myloginController,
 * });
 * 
 * @extends Ember.View
 */
var LoginView = Ember.View.extend({
    /**
     * Which template is used for this view.
     * @type {String}
     */
    "templateName": "login",

    /**
     * Controller we are working with.
     * @type {LoginController}
     */
    "controller": null,
    
    /**
     * Username claimed by user.
     * @type {String}
     */
    "usernameBinding": "*controller.username",
    
    /**
     * Password claimed by user.
     * @type {String}
     */
    "passwordBinding": "*controller.password",

    /**
     * Allows us to signal when a submission has been made.
     * When not submitting, this is an empty string.
     * @type {String}
     */
    "isSubmittingBinding": "*controller.isSubmitting",

    /**
     * Handle the submit process from the login form.
     */
    "click": function(e) {
        var el = this.$(),
            // Property names we wish to update from the form.
            // Assumes the form has named the input elements in the
            // template correctly.
            inputs = ["username", "password"],
            i;

        // Just in case the template doesn't kill the action.
        e.preventDefault();

        // Signal user attempted to submit, but only on a button click.
        if (!this.get("isSubmitting")) {

            // Update the values from the form.
            for (i = 0; i < inputs.length; i++) {
                // Prevent NaN, which for some reason seems to lock up ember.js.
                this.set(inputs[i], el.find("."+inputs[i]).val() || "");
            }

            this.set("isSubmitting", e.target.getAttribute("data-button-role"));
        }
    },
});
// Export
//exports.LoginView = LoginView;



})(window);
