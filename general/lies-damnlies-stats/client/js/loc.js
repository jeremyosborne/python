//----------------------------------------------------------------- Localization
/**
 * Ember.js offers a localization extension to the String prototype.
 * Set the dictionary of strings to Ember.STRINGS and then call .loc() on any
 * string that should be translated via the Ember.STRINGS key:value pairs.
 * 
 * The underscore in the key is not required, it just makes finding
 * untranslated strings easier.
 *
 * See:
 * http://stackoverflow.com/questions/8762456/does-ember-support-localization-like-sc-1-x
 * 
 * By default Handlebar strings are not localized. Should you wish to put
 * localizable strings in Handlebar templates, use the the loc helper like so:
 * {{loc "_this is my string to localize"}}
 * 
 * @type {String{}}
 */
Ember.STRINGS = {
    //---------------------------------------------------------- JS Code Strings
    // DataCache
    "_ERROR saving key:value to cache: %@:%@":
        "ERROR saving key:value to cache: %@:%@",
    
    "_Choose a Statistics Group":
        "Choose a Statistics Group",
    "_ERROR: Could not load available stats descriptions.":
        "ERROR: Could not load available stats descriptions.",
    "_ERROR: $.ajax error function being called during loadStatsDescriptions.":
        "ERROR: $.ajax error function being called during loadStatsDescriptions.",

    "_Loading...":
        "Loading...",
    "_ERROR: Could not load stats.":
        "ERROR: Could not load stats.",
    "_ERROR: $.ajax error function being called during load":
        "ERROR: $.ajax error function being called during load",
    // Server messages
    "_Authentication required to retrieve data.":
        "Authentication required to retrieve data.",
        
    "_Saving...":
        "Saving...",
    "_Saved Successfully":
        "Saved Successfully",
    "_ERROR: During save call to server.":
        "ERROR: During save call to server.",
    "_ERROR: $.ajax error function being called during save":
        "ERROR: $.ajax error function being called during save",
    // Server messages.
    "_Could not save the data. Please check your input.":
        "Could not save the data. Please check your input.",

    "_Deleting...":
        "Deleting...",
    "_Deleted Successfully":
        "Deleted Successfully",
    "_ERROR: During delete call to server.":
        "ERROR: During delete call to server.",
    "_ERROR: $.ajax error function being called during delete":
        "ERROR: $.ajax error function being called during delete",
    // Server messages.
    "_No record to delete.":
        "No record to delete.",
    
    // Application cache
    "_This application has been updated. Please reload this page.":
        "This application has been updated. Please reload this page.",
    
    // UserInput fields
    "_Date:":
        "Date:",
    "_Number:":
        "Number:",
    
    // Authentication: client messages.
    "_Welcome to ldls":
        "Welcome to ldls",
    // Authentication: server messages.
    "_Service only accepts HTTP POST requests.":
        "Service only accepts HTTP POST requests.",
    "_Incorrect username or password.":
        "Incorrect username or password.",
    // Takes one argument, that is the name of the user we are welcoming,
    // or welcoming back.
    "_Welcome, %@":
        "Welcome, %@",
    "_Welcome back, %@":
        "Welcome back, %@",
    // checkAuth - validating current authorization, or lack thereof.
    // Potentially benign code breakage, prefixes server messages.
    "_ERROR: in checkAuth: ":
        "ERROR: in checkAuth: ",
    // Serious code breakage.
    "_ERROR: in checkAuth: should never reach here. Please report.":
        "ERROR: in checkAuth: should never reach here. Please report.",
    "_ERROR: $.ajax error function being called during checkAuth.":
        "ERROR: $.ajax error function being called during checkAuth.",
    // active login attempt
    "_Login successful.":
        "Login successful.",
    "_ERROR: in login: should never reach here. Please report.":
        "ERROR: in login: should never reach here. Please report.",
    "_ERROR: $.ajax error function being called during login.":
        "ERROR: $.ajax error function being called during login.",


    // Egg tracking.
    // page title
    "_Egg Tracking":
        "Egg Tracking",
};
