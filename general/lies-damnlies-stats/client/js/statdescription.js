(function(exports) {


    
/**
 * @class Allows simple validation of data on the client side.
 * 
 * @example
 * // Construct.
 * var sd = StatDescription.create({ 
 *     "name": "theNameOfThisDataModel",
 *     "content": jsonFromServer,
 * });
 * 
 * @extends Ember.Object
 */
var StatDescription = Ember.Object.extend({
    /**
     * The name of the stat, which correspondes to the name of the server
     * side data model.
     * A falsey value is considered an unbounded StatDescription.
     * @type {String}
     */
    "name": "",
    
    /**
     * The raw data hash from the server used to describe the data model.
     * Will be initialized to an empty object if not
     * @type {Object}
     */
    "content": null,
    
    /**
     * Access to the provided data validators.
     * @type {DataValidator}
     */
    // DEPENDENCY: For the ease of coding, just depend on DataValidator.
    // It's a shared reference, who cares if it is part of the prototype.
    "validators": DataValidator,

    /**
     * Access to the provided data converters.
     * @type {DataConverter}
     */
    // DEPENDENCY: For the ease of coding, just depend on DataConverter.
    // It's a shared reference, who cares if it is part of the prototype.
    "converters": DataConverter,
        
    /**
     * Returns a copy of all of the fields for use by other objects.
     * @return {Object} Associative array of fields and types.
     */
    "getFields": function() {
        var original = this.get("content"),
            copy = {},
            i;
        for (i in original) {
            if (original.hasOwnProperty(i)) {
                copy[i] = original[i];
            }
        }
        return copy;
    },
    
    /**
     * Gets the type of a particular field.
     * @param name {String} The name of the field to check.
     * @return {String|Undefined} The name of the field type, or undefined
     * if the requested field doesn't exist.
     */
    "getFieldType": function(name) {
        return this.get("content")[name];
    },
    
    /**
     * Gets the default value for a field.
     * @return {mixed} The default value of a field type, or undefined if
     * the requested field doesn't exist.
     */
    "getFieldDefaultValue": function(name) {
        var defaultValueGenerator = this.get("converters")["default"+name];
        
        if (defaultValueGenerator) {
            return defaultValueGenerator();
        }
        // else
        // return undefined;
    },
    
    /**
     * Get the associated "from" converter for a type.
     * @param type {String} The name of the type to retrieve a from converter
     * for.
     * @return {Function|Undefined} Either the correct converter function,
     * or undefined, will be returned.
     */
    "getFromConverter": function(type) {
        return this.get("converters")["from"+type];
    },

    /**
     * Get the associated "to" converter for a type.
     * @param type {String} The name of the type to retrieve a from converter
     * for.
     * @return {Function|Undefined} Either the correct converter function,
     * or undefined, will be returned.
     */
    "getToConverter": function(type) {
        return this.get("converters")["to"+type];
    },
    
    /**
     * Validate a name and value against the model definition.
     * @param name {String} The name of the field to validate against.
     * @param value {mixed} The value to validate.
     * @return {Boolean} true if the key and value match the expectations
     * set forth by the description, false if not.
     */
    "validateField": function(name, value) {
        var description = this.get("content"),
            validator;
                
        if (description) {
            // The keys in the descriptions, if valid, point to names of
            // validator functions in the validators hash.
            validator = this.get("validators")[description[name]];
            // NOTE: this will fail silently if we get a datatype not
            // supported.
            if (typeof validator == "function") {
                // Compare the expected value against the datatype.
                return validator(value);
            }
        }
        // If we get here, it always signals a failure.
        return false;
    },
    
    /**
     * Performs a validation against the provided object/associative array.
     * @param data {Object} Associative array to validate.
     * @return {Boolean} true if the entire object validates successfully,
     * false if not.
     */
    "validateAll": function(data) {
        var field,
            outcome = true;
        for (field in data) {
            if (data.hasOwnProperty(field)) {
                console.log()
                outcome = this.validateField(field, data[field]);
                if (!outcome) {
                    break;
                }
            }
        }
        return outcome;
    },
    
    /**
     * Initialization.
     */
    "init": function() {
        this._super();
        
        if (!this.get("content")) {
            this.set("content", {});
        }
    },
});
exports.StatDescription = StatDescription;


})(window);
