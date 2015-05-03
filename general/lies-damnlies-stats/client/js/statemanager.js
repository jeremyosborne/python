(function(exports) {



/**
 * @class Controls the various application states.
 * 
 * @example
 * var stateManager = StateManager.create();
 * 
 * @extends Ember.StateManager
 * @extends Ember.NotificationsMixin
 */
var StateManager = Ember.StateManager.extend(NotificationsMixin, {

    // NOTE: At the time of writing, the Ember StateManager has very little
    // documentation and has very few examples on the internet. Implementation 
    // is educational and extra documentation is included to compensate.

    // If set, designates which state we start in (must match a defined
    // property that is a state).
    
    // Enable for debugging messages.
    //enableLogging: true,
    
    /**
     * Name of the initial state we start in.
     * @type {String}
     */
    "initialState": "initializeApplication",

    /**
     * Initialize the necessary application instances and singletons.
     * @type {Ember.State}
     */
    "initializeApplication": Ember.State.create({
        /**
         * Handles application cache upates.
         * @type {ApplicationCacheController}
         */
        "appCacheController": null,
        
        // Every state has a potential .enter() and .exit() callback that can
        // be set. The .enter() method is called when ever a state is entered,
        // usually via a call to .goToState().
        // The callback is passed:
        // manager {Ember.StateManager} -> The StateManager object that this
        // state belongs to.
        // [transition] {Transition} -> A transition object that... well, I'm
        // not exactly sure what it does at the moment.
        // The 'this' reference of a state message callback is the State.
        "enter": function(manager) {
            // The few code examples hint that I should always call ._super() 
            // in the .enter() and .exit() overrides.
            this._super();
            
            //------------------------------------ Empty state.
            
            // Add the footer menu automatically (for now).
            App.pageFooterController.addView(FooterMenuView.create({
                "stateManager": manager,
            }));

            // Check the application cache for updates.
            this.appCacheController = AppCacheController.create({
                "ready": function() {
                    // Trigger the first active state.
                    manager.goToState("checkAuth");
                },
            });           
        },
        
        /**
         * Clean up.
         */
        "exit": function(manager) {
            this._super();
            // This state is not a view state, no views to clear.
            
            // Remove the controller.
            this.appCacheController = undefined;
        },
      
    }),
    
    /**
     * Determine if the user credentials on the client are valid.
     * @type {Ember.State}
     */
    "checkAuth": Ember.State.create({
        /**
         * Handles the user auth logic and provides access to the view.
         * @type {LoginController}
         */
        "loginController": null,

        "enter": function(manager) {
            this._super();

            this.loginController = LoginController.create();

            // Configure the rest of the items after the load (this is due
            // to some binding problems I experienced back in ember 0.9.3).
            this.loginController.addObserver('revision', function() {
                // Remove ourselves from the observers (prevents accidental
                // multiple calls).
                this.removeObserver('revision', arguments.callee);
                
                if (this.get("userProfile")) {
                    // We determine that we are logged in.                    
                    this.notifyInfo("_Welcome back, %@".loc(
                        [this.get("userProfile").username]
                    ));
                    // Trigger the default view (change state).
                    manager.goToState("statsChooser");
                }
                else {
                    // We determine that we are not logged in.
                    manager.goToState("login");
                }
            });
            
            this.loginController.checkAuth();
        },
        /**
         * Clean up.
         */
        "exit": function(manager) {
            this._super();
            // There are no views on this page.

            // Remove the controller.
            this.loginController = undefined;
        },

    }),
    
    /**
     * Handles user authentication.
     * @type {Ember.State}
     */
    "login": Ember.State.create({
        /**
         * Handles the user auth logic and provides access to the view.
         * @type {LoginController}
         */
        "loginController": null,

        /**
         * Initialize the objects needed for login.
         */
        "enter": function(manager) {            
            this._super();

            this.loginController = LoginController.create();

            // Set page header to the correct title.
            App.pageHeaderController.set("content", "_Welcome to ldls".loc());
            
            App.pageBodyController.addView(this.loginController.get("view"));

            this.loginController.addObserver('revision', function() {                
                if (this.get("userProfile")) {
                    // Successful login.
                    // Remove ourselves from the observers (prevents accidental
                    // multiple calls).
                    this.removeObserver('revision', arguments.callee);
                
                    // We determine that we are logged in.                    
                    this.notifyInfo("_Welcome, %@".loc(
                        [this.get("userProfile").username]
                    ));

                    // We are now logged in.
                    manager.goToState("statsChooser");
                }
                // Else we are not logged in, just wait.
                // The loginController will echo server error messages
                // on failed login attempts.
            });


            // Bye bye iPhone toolbar in web mode... 
            // Due to the delay in building the DOM, need to pause a moment
            // before attempting to scroll.
            setTimeout(function() {
                window.scrollTo(0, 1);
            }, 5);
        },
        /**
         * Clean up.
         */
        "exit": function(manager) {
            this._super();
            // Clear any views we put on the page.
            App.pageBodyController.clearViews();
            // Clean up controllers.
            this.loginController = undefined;
        },
    }),
    
    /**
     * Provide an opportunity to choose which stats will be worked with.
     * @type {Ember.State}
     */
    "statsChooser": Ember.State.create({
        /**
         * Allows user to select the view that they wish to manipulate.
         * @type {StatsChooserView}
         */
        "statsChooserView": null,
        
        /**
         * Have we been to this state before?
         * Not sure if this jives with how ember works, but it works good
         * enough for me right now.
         * @type {Boolean}
         */
        "firstTimeThrough": true,
        
        /**
         * Should the entry through the statsChooser clear the views?
         * Kluge fix, as we may not want to clear the views on our first
         * run through.
         */
        "clearViews": true,
        
        /**
         * Initialize the objects needed for choosing a stat.
         */
        "enter": function(manager) {
            var thisState = this;
            
            this._super();

            App.pageHeaderController.set("content", "_Loading...".loc());

            // Load the available statistics names.
            // When the names of the stats groups have been loaded, display
            // the statsChooser (and change the title to _choose a stat).
            // When the user chooses a stat, transition out of this state
            // and into the statEntry state.
            this.statsChooserView = StatsChooserView.create({
                "controller": App.statsCache
            });
            App.statsCache.loadStatsDescriptions();
            
            App.statsCache.addObserver("statsDescriptions", function() {
                // During the selection process, currentStatName might be
                // a null value. Only change when we're set to something.
                if (this.get("statsDescriptions")) {
                    // Remove ourselves from the observers (prevents accidental
                    // multiple calls).
                    this.removeObserver("statsDescriptions", arguments.callee);
                }
                
                // TODO: This is a mess. Clean this up later by breaking this
                // into substates.
                
                if (App.statsCache.get("currentStatName") && 
                    thisState.get("firstTimeThrough")) {
                    // Don't clear the views.                    
                    thisState.set("clearViews", false);
                    // Send the user straight through to the statEntry state.
                    manager.goToState("statEntry");
                }
                else {
                    // otherwise, the user needs to choose their stat.
                    App.pageHeaderController.set("content", "_Choose a Statistics Group".loc());
                    App.pageBodyController.addView(thisState.statsChooserView);
                    // Set up the observer to the currentStatName (although this
                    // shouldn't fire until the names have loaded and the user
                    // tries to choose something).
                    App.statsCache.addObserver('currentStatName', function() {
                        // During the selection process, currentStatName might be
                        // a null value. Only change when we're set to something.
                        if (this.get("currentStatName")) {
                            // Remove ourselves from the observers (prevents accidental
                            // multiple calls).
                            this.removeObserver('currentStatName', arguments.callee);
                            // We have now chosen a statistic to enter/view.
                            manager.goToState("statEntry");
                        }
                    });
                }
                // No matter what, we've now been through here once.
                thisState.set("firstTimeThrough", false);                
            });
        },
        /**
         * Clean up.
         */
        "exit": function(manager) {
            this._super();
            
            // Clear any views we put on the page.
            if (this.get("clearViews")) {
                App.pageBodyController.clearViews();
            }
            
            // Reset to default.
            this.set("clearViews", true);
        },
    }),
    
    /**
     * Manages the main statistic entry view.
     * @type {Ember.State}
     */
    "statEntry": Ember.State.create({
        /**
         * Handles stat data entry logic.
         * @type {StatEntryController}
         */
        "statEntryController": null,
            
        /**
         * Logic controller for the complete summary.
         * @type {SummaryController}
         */
        "summaryController": null,
                
        /**
         * Logic controller for the weekly summary.
         * @type {WeeklySummaryController}
         */
        "weeklySummaryController": null,
            
        /**
         * Handles the daily summary computations.
         * @type {DailySummaryController}
         */
        "dailySummaryController": null,
        
        /**
         * Initialize the objects needed for stat entry.
         */
        "enter": function(manager) {
            var controller,
                view,
                self = this;
                
            this._super();
            
            App.pageHeaderController.set("content", "_Loading...".loc());
                        
            // StatEntry initialization.
            this.statEntryController = StatEntryController.create({
                "cache": App.statsCache,
            });
            // Summary controller/views.
            this.summaryController = SummaryController.create({
                "cacheBinding": Ember.Binding.oneWay("App.statsCache"),
            });
            this.weeklySummaryController = WeeklySummaryController.create({
                "cacheBinding": Ember.Binding.oneWay("App.statsCache"),
            });
            this.dailySummaryController = DailySummaryController.create({
                "cacheBinding": Ember.Binding.oneWay("App.statsCache"),
            });
            
            // Configure the rest of the items after the load (this is due
            // to some binding problems I experienced back in ember 0.9.3).
            App.statsCache.addObserver('isLoaded', function() {
                if (!this.get("isLoaded")) {
                    return;
                }
                // What to set the page title to.
                var pageTitle = this.get("currentStatName").toTitleCase();
                
                // Remove ourselves from the observers (prevents accidental
                // multiple calls).
                this.removeObserver('isLoaded', arguments.callee);
                
                //-------------------------------- Begin the display of views.    
                // Set page header to the correct title.
                App.pageHeaderController.set("content", pageTitle);
    
                // The following is just a reason to begin using the StateManager
                // and offloading some of the work from the App instance.
                App.pageBodyController.addView(self.statEntryController.get("view"));
                App.pageBodyController.addView(self.summaryController.get("view"));
                App.pageBodyController.addView(self.weeklySummaryController.get("view"));
                App.pageBodyController.addView(self.dailySummaryController.get("view"));
    
                // Bye bye iPhone toolbar in web mode... 
                // Due to the delay in building the DOM, need to pause a moment
                // before attempting to scroll.
                setTimeout(function() {
                    window.scrollTo(0, 1);
                }, 5);
            });
            // Load the stats and trigger the view change when the stats
            // are loaded.
            App.statsCache.load();
            
            // NOTE for future self:
            // What appeared on the outside to be a synchronous state 
            // transition via a pretty straightforward named "goToState" 
            // doesn't actually cause the state to transition
            // officially over to statEntry, as such we can't send a message
            // to our own state until we exit the enter function. This might
            // be as intended, as maybe enter is meant to reject a state
            // transition, but there are no docs that I can check.
            // In general, if the enter state is going to display things,
            // just make it a long procedure and have it display things.
            // NOTE 2: I just noticed I wasn't calling super originally on
            // the enter. I haven't test now that I'm calling the super
            // method, but i bet this will fix my previous problems of the
            // state not recognizing itself as being in the new state.
        },
        /**
         * Clean up.
         */
        "exit": function(manager) {
            this._super();
            // Clear any views we put on the page.
            App.pageBodyController.clearViews();
            // Clear out any controllers.
            this.statEntryController = undefined;
            this.summaryController = undefined;
            this.weeklySummaryController = undefined;
            this.dailySummaryController = undefined;
        },
    }),
});
// Export
exports.StateManager = StateManager;

})(window);
