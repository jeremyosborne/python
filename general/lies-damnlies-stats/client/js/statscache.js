(function(exports) {



/**
 * @class A cache of individual stat models. Should consist of all of the
 * models in memory, whether synced with the server or not.
 * 
 * In general, components should interact with the StatsCache for creation,
 * querying, and deleting of individal stat models.
 * 
 * @example
 * // Proper construction
 * var scache = StatsCache.create({
 *     dataCache: App.dataCache,
 * });
 * // For each stat structure, pass JSON data hash to the .add() method.
 * for (var i = 0; i < stats.length; i++) {
 *     scache.add(stats[i]);
 * }
 * 
 * @extends Ember.Object
 * @extends LoggerMixin
 * @extends NotificationsMixin
 */
var StatsCache = Ember.Object.extend(LoggerMixin, NotificationsMixin, {
    /**
     * Pointer to the persistent data cache to which we should save our
     * data too.
     * @type {DataCache}
     */
    "dataCache": null,
    
    /**
     * Memory cache of stats.
     * Will always be an associative array (created after initialization).
     * Models will be keyed to this by their "pkey" value.
     * @type {Stat{}}
     */
    "cache": null,

    /**
     * Are the statistics loaded?
     * (This is sort of a kluge fix to deal with what seems to be a problem
     * of binding observers prior to having real models to bind to).
     * @type {Boolean}
     */
    "isLoaded": false,
    
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
     * The name of the current stat being handled by this instance.
     * If set, it should match the name of a stat locatable by key in
     * the statsDescriptions associative array.
     * 
     * Will be a falsey value if there isn't a currentStatName cached.
     * 
     * @type {String}
     */
    "currentStatName": Ember.computed(function(key, value) {
        var currentStatName,
            isValid;
        
        if (arguments.length === 1) {
            // get
            currentStatName = this.get("dataCache").pull("currentStatName");
            isValid = currentStatName in this.get("statsDescriptions");
            return isValid ? currentStatName : null;
        }
        else {
            // set
            // make JSON friendly
            // NOTE: any currentStatName can be set, but that doesn't mean
            // it will be returnable if there isn't a matching description
            // for it in statsDescriptions.
            value = value || null;
            this.get("dataCache").put("currentStatName", value);
        }
    }).property(),

    /**
     * The object describing the current stat.
     * 
     * Getter only.
     * 
     * @type {StatDescription}
     */
    "currentStatDescription": Ember.computed(function() {
        var description,
            name;
            
        name = this.get("currentStatName");
        return this.get("statsDescriptions")[name];
        
        // NOTE: This seems to work right now in my limited usage.
        // .cacheable() seems to be returning the same object at the same
        // memory address, so we've at least memoized the call and can
        // reference the same descriptor over and over.
    }).property("currentStatName").cacheable(),
        
    /**
     * An associative array of the stats and model descriptions made 
     * available by the server.
     * 
     * Initialized in the init function.
     * 
     * Set with plain old JSON objects, but the hash returned will contain
     * StatDescriptions.
     * 
     * @type {StatDescription{}}
     */
    "statsDescriptions": Ember.computed(function(key, value) {
        var sd,
            i;
        if (arguments.length === 1) {
            // get
            sd = this.get("dataCache").pull("statsDescriptions") || {}
            for (i in sd) {
                if (sd.hasOwnProperty(i)) {
                    // remap plain objects to StatDescription.
                    sd[i] = StatDescription.create({
                        "name": i,
                        "content": sd[i],
                    });
                }
            } 
            return sd;
        }
        else {
            // set
            // make JSON friendly
            value = value || {};
            this.get("dataCache").put("statsDescriptions", value);
        }
    }).property(),

    /**
     * Load the list, and model descriptions, of statistics supported by the 
     * server.
     * 
     * This will refresh any cached stats descriptions.
     */
    "loadStatsDescriptions": function() {
        var self = this;

        $.ajax(ldlsConf.describeURL, {
            "dataType": "json",
            "success": function(data) {
                if (!data.error && data.description) {
                    self.set("statsDescriptions", data.description);
                }
                else {
                    self.notifyError("_ERROR: Could not load available stats descriptions.".loc())
                    if (data.error && (typeof data.error == "string")) {
                        self.notifyError(data.error.loc());
                    }
                }                
            },
            "error": function() {
                self.notifyError("_ERROR: $.ajax error function being called during loadStatsDescriptions.".loc());
                // DEBUG
                self.log("_ERROR: $.ajax error function being called during loadStatsDescriptions.".loc());
                self.log(arguments);
            },            
        });
    },


    /**
     * Adds a model to the cache, but only if the model does not yet exist.
     * If the model already exists, this will perform an update of the
     * existing model.
     * @param model {Object|Stat} The model to add, either in a raw JSON
     * form (direct from server) or as a pre-created Stat.
     */
    "add": function(model) {
        var existingModel,
            cache = this.get("cache");

        if (!model.isStat) {
            // We only deal with models from here on out.
            model = Stat.create({
                "description": this.get("currentStatDescription"),
                "content": model,
            });
        }

        // Do we have an existing model?
        existingModel = cache[model.get("pkey")];        
        if (!existingModel) {
            // Create in cache.
            cache[model.get("pkey")] = model;
        }
        else {
            // Update in cache.
            
            // NOTE: getting weird ember.js errors doing direct attribute
            // settings. Dropping the content of the updated model into
            // the old model seems to work just fine.
            existingModel.set("content", model.get("content"));
        }

        // This is our signal that we have a new revision and that observers
        // of the cache should update themselves.
        this.set("revision", this.get("revision") + 1);
    },
    
    /**
     * Delete a model from this collection.
     * @param pkey {String} Removes a model according to it's pkey.
     */
    "remove": function(pkey) {
        // Remove shouldn't be called except when notified by server,
        // just nuke the model from the cache.
        delete this.get("cache")[pkey];

        // This is our signal that we have a new revision and that observers
        // of the cache should update themselves.
        this.set("revision", this.get("revision") + 1);
    },

    /**
     * Perform an initial load of the stats into this collection.
     */
    "load": function() {
        var self = this;
        // This might now be called more than once.
        this.set("isLoaded", false);
        // Nuke any previously existing cache.
        this.set("cache", {});

        $.ajax(ldlsConf.getURL, {
            "dataType": "json",
            "data": {
                "statName": this.get("currentStatName"),
            },
            "success": function(data) {
                var i,
                    stats,
                    numStats;
                    
                if (!data.error && data.stats) {
                    stats = data.stats;
                    numStats = data.stats.length;
                    
                    for (i = 0; i < numStats; i++) {
                        self.add(stats[i]);
                    }
                    // Assume that whatever stats we have at the moment is
                    // good enough.
                    self.set("isLoaded", true);
                }
                else {
                    self.notifyError("_ERROR: Could not load stats.".loc())
                    if (data.error && typeof data.error == "string") {
                        self.notifyError(data.error.loc());
                    }
                }                
            },
            "error": function() {
                self.notifyError("_ERROR: $.ajax error function being called during load".loc());
                // DEBUG
                self.log("_ERROR: $.ajax error function being called during load".loc());
                self.log(arguments);
            },            
        });
    },
    
    /**
     * Initializes the cache.
     */
    "init": function() {
        this._super();        

        // Add hash.
        this.set("cache", {});        
    },

});
// Export
exports.StatsCache = StatsCache;



})(window);
