(function(exports) {



/**
 * @class Singular model for one data point.
 * In this application, a single datapoint represents one full day's worth of
 * data.
 * 
 * @example
 * // Construct a single data point
 * var s = Stat.create({ 
 *     "content": jsonFromServer, 
 *     "description": someStatDescription,
 * });
 * 
 * @extends Ember.Object
 */
var Stat = Ember.Object.extend({
    
    /**
     * The raw data hash from the server, describing the contents of the
     * stat.
     * @type {Object}
     */
    "content": null,

    /**
     * The validation model describing this stat.
     * A falsey description is the equivalent of an unbound data model.
     * @type {StatDescription}
     */
    "description": null,

    /**
     * Is this a statistic data model?
     * Used to distinguish from plain old JSON object hashes.
     * @type {Boolean}
     */
    "isStat": true,
    
    /**
     * Name of the server side data model does this stat correspond to?
     * A falsey value is the equivalent of an unbound data model.
     * @type {String}
     */
    "name": Ember.computed(function() {
        var d = this.get("description");
        if (d) {
            return d.get("name");
        }
        else {
            return "";
        }
    }).property("description").cacheable(),
        
    /**
     * Get the unique identifier of this model, which is always assumed to
     * be the date.
     *
     * This is meant to be used to uniquely identify models in memory without
     * resorting to memory addresses.
     * @type {String}
     */
    "pkey": Ember.computed(function() {
        // NOTE: Models that do not yet have a date set are considered to
        // not have a pkey.
        // It is _possible_ for different models in memory to have the
        // same pkey, even though this will not happen on models on the
        // server, and even though this is Not A Good Thing.
        return this.get("content").date;
    }).property(),
    
    /**
     * Set a particular field on the underlying data hash, corrected to be
     * appropriate.
     * @param name {String} The name of the field to set.
     * @param value {mixed} The value to set the field to.
     * @return {Boolean} If the field was set correctly, return true,
     * otherwise return false.
     */
    "setField": function(name, value) {
        var type = this.get("description").getFieldType(name),
            converter = this.get("description").getToConverter(type);
            
        if (typeof converter == "function") {
            value = converter(value);
            if (value !== undefined) {
                this.get("content")[name] = value;
                return true;
            }
        }
        // else
        return false;
    },

    /**
     * Get the value of a particular field.
     * @param name {String} The name of the field to get the value of.
     * @return {mixed} The current value of the field. If undefined is
     * returned, the field requested is invalid, or the current value of the
     * underlying field has been invalidly set.
     */
    "getField": function(name) {
        var type = this.get("description").getFieldType(name),
            converter = this.get("description").getFromConverter(type);
        
        if (typeof converter == "function") {
            return converter(this.get("content")[name]);
        }
        // else
        return undefined;
    },

    /**
     * Returns an array of mapped fields and values.
     * This returns the raw values and does not validate along the way.
     * @param nokey {Boolean} If true, the primary key is not returned in the
     * list of described fields.
     * @return {Object[]} Each field is represented by a single object in the 
     * array containing a keyword "field" pointing to the field name and a 
     * keyword "value" pointing to the value of that field name.
     */
    "getFieldValueList": function(nokey) {
        // TODO: This should be a cached, computed property.
        var original = this.get("content"),
            list = [],
            i;
        for (i in original) {
            // NOTE: Hardcoded the primary key of "date".
            if (nokey && i == "date") {
                continue;
            }
            else if (original.hasOwnProperty(i)) {
                list.push({
                    "field": i,
                    "value": original[i],
                });
            }
        }
        return list;        
    },
        
    /**
     * Initialization function called when the object is created.
     */
    "init": function() {
        // NOTE: Init does not receive formal arguments, it is called only
        // as a convenience after the object has been constructed.
        
        // We need to call super.
        this._super();
        
        // If we didn't receive any content, set our content to an empty
        // hash.
        if (this.get("content") == null) {
            // Our empty hash.
            this.set("content", {});
        }
    },
});
// Export
exports.Stat = Stat;

})(window);
