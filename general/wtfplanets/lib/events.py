"""Publisher/subscriber system.

General usage:

    from events import EventPublisher
    
    pub = EventPublisher()
    
    # Event listeners are functions assigned to an arbitrary event name:
    def my_listener(evobj):
        # Event listeners should accept one and only 1 argument.
        # The argument passed is an event object.
        print "The name of the event is", evobj.name
        # Event specific data is passed in the data dictionary.
        if score in evobj.data:
            print "The current game score is:", evobj.score
    
    # Subscribe the listener...
    pub.sub("score-change", my_listener)
    
    # ...do other stuff in the code...
    
    # ...and sometime in the future:
    pub.pub("score-change", score=100)
    
    # This will call the callback (and any others) subscribed to this event and
    # will pass the data.

"""



class EventObject(dict):
    """A bare object for passing event data to event listeners.
    
    The following properties are provided:

    name {str} The name of the event.
    source {object} The object that is marked as the cause of the event
    being published.
    data {dict} Event specific data to be passed to the listener.
    """
    def __init__(self, name="unnamed", source=None, data=None):
        self.name = name
        self.source = source
        self.data = data or {}



class EventPublisher(object):
    """Implements a simple pub/sub interface.
    
    Suitable as an instance (simple publisher) or a class mixin.

    Requires call to __init__ from inheritor to initialize if used as a
    mixin.
    """
    _listener_id = 0L
    def __init__(self, *args, **kwargs):
        """Initializer.
        
        Accepts all arguments only as a convenience to subclasses. All
        arguments are ignored.        
        """
        # Make it mixin friendly.
        super(EventPublisher, self).__init__(*args, **kwargs)
        # Listeners get organized as a hash of hashes.
        self._event_listeners = {}
    
    def countsubs(self):
        """Total number of event subscribers.
        """
        return sum(len(event_list) for event, event_list in self._event_listeners.items())

    def _next_listener_id(self):
        """Return the next key available with which to id a listener.
        """
        EventPublisher._listener_id += 1
        return EventPublisher._listener_id

    def sub(self, event, callback):
        """Subscribe to a named event.
        
        event {str} Name of the event to listen to.
        callback {function} Callback function that will be passed one argument:
        the EventObject.
        
        return {tuple} A key that can be used to unsubscribe this listener 
        from this event.
        """
        listener_id = self._next_listener_id()
        if event not in self._event_listeners:
            self._event_listeners[event] = {}
        self._event_listeners[event][listener_id] = callback
        
        # Should be considered opaque outside of the pub/sub world.
        return event, listener_id
    
    def pub(self, event, **kwargs):
        """Publish an event by name to any listeners listening.
        
        event {str} Name of the event to publish.
        target {mixed} Reference to object that should act as the target of
        the event.
        data {dict} Dictionary of data to be passed on to the listener.
        """
        if event in self._event_listeners:
            listeners = self._event_listeners[event]
            for listener_id in listeners:
                listeners[listener_id](EventObject(name=event, source=self, data=kwargs.copy()))

    def clear_one(self, event_key):
        """Remove a specific event listener by key.
        
        event_key {tuple} An opaque key for removing events.
        """
        try:
            del self._event_listeners.get(event_key[0])[event_key[1]]
        except Exception:
            # If there is no event to remove, don't explode.
            pass

    def clear_many(self, event=None):
        """Remove all event listeners, or a particular group of event listeners
        by name.
        
        event {str} The name of the group of event listeners to remove. 
        If not passed all event listeners are removed.
        """
        if not event:
            # nominate all listeners for garbage collection
            self._event_listeners = {}
        else:
            try:
                del self._event_listeners[event]
            except KeyError:
                # allow silent fail for unsubscribed names.
                pass

    def audit(self):
        """Debug and diagnostic of events currently subscribed.
        
        returns {dict} with a "count" item listing current total listeners,
        and a shallow copied "listeners" dictionary of all listeners
        currently subscribed.
        """
        return {
                "count": self.countsubs(),
                "listeners": self._event_listeners.copy()
                }


class EventSubscriber(object):
    """Convenience class that aids in the removal of event listeners that 
    this object has subscribed to.
    
    For use with objects that only intend to be listeners, not publishers,
    although will not conflict with EventPublisher.
    
    Requires call to __init__ from inheritor to initialize.
    """
    def __init__(self, *args, **kwargs):
        """Initializer.

        Accepts all arguments only as a convenience to subclasses. All
        arguments are ignored.
        """
        # Make it mixin friendly.
        super(EventSubscriber, self).__init__(*args, **kwargs)
        # A hash of lists of event keys to specific event subscriptions.
        self._event_subs = {}
        
    def subto(self, source, event, callback):
        """Subscribe to a particular event and allow for easy removal of
        the listener at a later date.
        
        source {EventPublisher} Instance that publishes events.
        event {str} Name of the event to listen to.
        callback {function} Callback function that will be passed one argument:
        the EventObject.
        
        Raises TypeError if source does not subclass EventPublisher.
        """
        if isinstance(source, EventPublisher):
            if event not in self._event_subs:
                self._event_subs[event] = []
            subscription_key = source.sub(event, callback)
            self._event_subs[event].append({
                                            "subscription_key": subscription_key,
                                            "source": source
                                            })
        else:
            raise TypeError("source must subclass EventPublisher")
        
    def unsubfrom(self, event=None):
        """Unsubscribe from a list of events.
        
        event {str} The name of the group of event listeners to remove. 
        If not passed all event listeners are removed that we have tracked.
        """
        # Allow for one type of iteration loop.
        if event == None:
            # All events.
            event_listeners = ((evname, subs) for evname, subs in self._event_subs.items())
        elif event in self._event_subs:
            # All events of a particular name.
            event_listeners = ((event, self._event_subs[event]),)
        else:
            # No event, quit out.
            return
        
        for evname, subs in event_listeners:
            while subs:
                # Unsubscribe each event.
                subscriber_dict = subs.pop()
                subscriber_dict["source"].clear_one(subscriber_dict["subscription_key"])
            # Get rid of the event list now that it is empty.
            del self._event_subs[evname]


