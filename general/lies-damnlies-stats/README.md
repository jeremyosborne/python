# lies, damn lies, and statistics

This is an app I pulled together a number of years ago to track the eggs our backyard chickens were laying. It will probably never change, as the Ember code I was using (and not using well) on the client is old and not supported, and the Django version used on the server is now also old.

It was a fun project and I don't have the heart to delete it, so here it lies.



# Requirements
* Python 2.x (tested on 2.6.x and 2.7.x).
* Django 1.3.x
* node.js (for building the client, only used for development)



# Dev Setup
* cd to the server directory
    # Create/update the database. If changing models, it is better to dump
    # the database and rebuild everything.
    python manage.py syncdb
    # Add in some dummy data (you'll need to quit the sqlite3 client after each 
    # data entry).
    sqlite3 -init dummy_data/eggs.sql ldls.db3
    sqlite3 -init dummy_data/weight.sql ldls.db3
    # Run the server for localhost access only.
    python manage.py runserver
    # OR make the server accessible to non-localhost on the network.
    python manage.py runserver 0.0.0.0:8000

* Run Automated test for the server side code
    # Include the django default tests.
    python manage.py test
    # For just the stats app.
    python manage.py test stats

* cd to the client directory
    # Build a client that has non-minified code.
    node build dev
    # Build a client with minified code.
    node build
    # Build a client with minified code, and copy into the dist/ folder
    # for source code checkin.
    node build dist

* Point your web browser to (index.html not optional with Django setup):

    http://localhost:8000/static/build/index.html



# (Sort of) Prod notes 
* File changes (NOTE: Not currently in use on the home server):
    * server/settings.py -> set DEBUG to False.
    * server/settings.py -> set TEMPLATE_DEBUG to False.
    * server/settings.py -> set STATICFILES_DIRS to an empty tuple.
    * server/auth/views.py -> Set the expiration of the session cookie to
      something less than a year. 



# Things I meant todo but probably never will this point
* Authentication
    * Add logout link to the footer.
    * Show user information in the footer.
* AllSummariesView
    * Make a new page state that gives access to the summaries for the
      current view. This will separate the StatEntry from needing to
      know anything about cached data, and will make it easier to 
      use in an offline mode.
* StatCollection
    * RETHINK: The flow is broken with the add method. Any stat can be
      added, although it might not be the "current" stat. Need the add
      to drive the statDescription. The statsDescriptions property needs to
      return a cached set of StatDescriptions, not a cached set of plain old
      objects. Good enough (for now) answer: The StatsCache and DataCache will keep
      only one set of stats at a time. If the currentStatName ever changes,
      dump all the cached stats and load the new stats. That way 
      currentStatDescription can be set to cacheable.
      For now, one stat type is allowed on the device at a time. Probably
      good, keeps it under the 5MB limit for caches.
* Stat (models)
    * Stats are responsible for modifying themselves (create/update) and
      syncing with the server.
    * Stats delete themselves from the server/cache.
    * Dummy stats should probably be allowed an empty stat description.
* App
    * Do some sort of basic feature detection and alert if something is
      missing.
* DailySummary
    * Allow for changing the view based on the month being shown. Right now, 
      the number of days is hardcoded to the past 60 
* l10n and i18n
    * Capture all server errors and localize them.
* Offline Capabilities
    * Sometime, someday, move the HTTP requests to their own layer to prepare
      for app usage offline. The HTTP request layer should be an opaque proxy
      that will either return live data, or return data from the dataCache,
      or simply return dummy information.



# TODO - server
* Response Message - standardize the message object that comes back from the 
  server:
    * There should be an auth flag, and authorization failures should
      be quick fails, accompanied by an error code. Auth errors should
      be the highest level error, even over request GET|POST errors.
    * There should be sanitized server messages on errors.
* auth change
    * Remove the dependency on jsonserial.py by building a UserInfo object
      that also applies the JSONSerializerMixin.
* Upgrade to Django 1.4
    * Upgraded accidentally on laptop, and realized that the upgrade
      breaks things. In particular, it seems that the upgrade breaks
      the jsonserial parser. Ugg, I should have never used that code.
