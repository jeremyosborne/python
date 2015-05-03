/**
 * All helpers in this file assume that the ember.js code has been loaded
 * prior to loading this file.
 */
//------------------------------------------------------------- Handlebars Patch
/*
 * Per wagenet's gist located at:
 * https://gist.github.com/1563710/d7f4300fb725b9f8e1fc1e546758c11bd6fa7057
 *
 * This patch allows for the creation of handlebar helpers that can be bound
 * to a property and autoupdate when the property updates.
 */
Ember.HandlebarsTransformView = Ember.View.extend(Ember._MetamorphView, {
    rawValue: null,
    transformFunc: null,

    value: function() {
        var rawValue = this.get('rawValue'), 
            transformFunc = this.get('transformFunc');
        
        return transformFunc(rawValue);
    }.property('rawValue', 'transformFunc').cacheable(),

    render: function(buffer) {
        var value = this.get('value');
        if (value) {
            buffer.push(value);
        }
    },
    
    needsRerender: function() {
        this.rerender();
    }.observes('value'),
});

Ember.HandlebarsTransformView.helper = function(context, property, transformFunc, options) {
    options = options || {};
    options.hash = {
        rawValueBinding: property,
        transformFunc: transformFunc
    };
    return Ember.Handlebars.ViewHelper.helper(context, Ember.HandlebarsTransformView, options);
};

/*
 * Example usage from the gist:

    Ember.Handlebars.registerHelper('format', function(property, options) {
        var transformFunc = function(value) {
            return (value && value.format) ? value.format() : value;
        };
        return Ember.HandlebarsTransformView.helper(this, property, transformFunc, options);
    });
    
    // This one is untested but should work
    Ember.Handlebars.registerHelper('datetime', function(property, options) {
        var format = options.hash.format,
            transformFunc = function(value) {
                return (value && value.format) ? value.format(format) : value;
            };
        return Ember.HandlebarsTransformView.helper(this, property, transformFunc, options);
    });

    // Then....
    var now = moment().add('days', 9);
    // In the template
    {{datetime now format="dddd, MMMM Do YYYY"}}
    // And the results should be auto updatable
    Friday, January 13th 2012

 *
 */



//------------------------------------------------------------- Bindable Helpers
/**
 * Extract the year portion of the date.
 * @param property {String} Path to a date object.
 * @return {String} Four digit date if the date exists, or "N/A" if the date
 * doesn't exist.
 */
Ember.Handlebars.registerHelper('boundDateYear', function(property, options) {
    var transformFunc = function(value) {
        if (value && value.getFullYear) {
            value = value.getFullYear();
        }
        return value || "N/A";
    };
    return Ember.HandlebarsTransformView.helper(this, property, transformFunc, options);
});

/**
 * Extract the zero filled month portion of the date.
 * @return {String} Two digit month if the date exists, or "N/A" if the date
 * doesn't exist.
 */
Ember.Handlebars.registerHelper('boundDateMonth', function(property, options) {
    var transformFunc = function(value) {
        if (value && value.getMonth) {
            value = value.getMonth() + 1;
            // Zero fill.
            value = ((""+value).length == 1) ? "0"+value : value;
        }
        return value || "N/A";
    };
    return Ember.HandlebarsTransformView.helper(this, property, transformFunc, options);
});

/**
 * Extract the zero filled day portion of the date.
 * @return {String} Two digit day if the date exists, or "N/A" if the date
 * doesn't exist.
 */
Ember.Handlebars.registerHelper('boundDateDay', function(property, options) {
    var transformFunc = function(value) {
        if (value && value.getDate) {
            value = value.getDate();
            // Zero fill.
            value = ((""+value).length == 1) ? "0"+value : value;
        }
        return value || "N/A";
    };
    return Ember.HandlebarsTransformView.helper(this, property, transformFunc, options);
});

/**
 * Provide one decimal of significance for a number.
 * @return {Number} A number with trimmed decimal.
 */
Ember.Handlebars.registerHelper('oneDecimalDigit', function(property, options) {
    // NOTE: We must accept and pass the options on, not just the property
    // like with regular handlebar helpers.
    
    var transformFunc = function(value) {
        // These new helpers get the values passed in for real.
        return (value && value.toFixed) ? value.toFixed(1) : value;
    };
    return Ember.HandlebarsTransformView.helper(this, property, transformFunc, options);
});



//-------------------------------------------------------------- Regular Helpers
/**
 * Equivalent to the Ember.js String .loc() method, but for templates.
 * 
 * Requires that Ember.STRINGS is correctly set before use.
 */
Handlebars.registerHelper('loc', function(property) {
    return property.loc();
});

/**
 * Extract the year portion of the date.
 * @return {String} Four digit year if the date exists, or "N/A" if the date
 * doesn't exist.
 */
Handlebars.registerHelper('dateYear', function(property) {
    var value = Ember.getPath(this, property);

    if (value && value.getFullYear) {
        value = value.getFullYear();
    }
    else {
        value = "N/A"
    }
    
    return value;
});


/**
 * Extract the zero filled month portion of the date.
 * @return {String} Two digit month if the date exists, or "N/A" if the date
 * doesn't exist.
 */
Handlebars.registerHelper('dateMonth', function(property) {
    var value = Ember.getPath(this, property);

    if (value && value.getMonth) {
        value = value.getMonth() + 1;
        // Zero fill.
        value = ((""+value).length == 1) ? "0"+value : value;
    }
    else {
        value = "N/A"
    }
    
    return value;
});

/**
 * Extract the zero filled day portion of the date.
 * @return {String} Two digit day if the date exists, or "N/A" if the date
 * doesn't exist.
 */
Handlebars.registerHelper('dateDay', function(property) {
    var value = Ember.getPath(this, property);

    if (value && value.getDate) {
        value = value.getDate();
        // Zero fill.
        value = ((""+value).length == 1) ? "0"+value : value;
    }
    else {
        value = "N/A"
    }
    
    return value;
});

/**
 * Check to see if a date is an even or odd month.
 * @return {String} The classname to be applied in the case of this item.
 */
Handlebars.registerHelper('isEvenMonth', function(property, evenClass, oddClass) {
    var value = Ember.getPath(this, property);

    if (value && value.getMonth) {
        // Failure of the mod means even.
        value = (value.getMonth()+1) % 2 ? evenClass : oddClass;
    }
    else {
        value = ""
    }
        
    return value;
});
