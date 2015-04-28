


class State(object):
    """Singular state.
    
    Abstract-baseclass-like object. Does not need init'ing.
    """
    
    # {str} Human friendly name. Used for reference and indexing. Must be
    # set and unique among all states.
    name = None
    
    def process(self, time_passed=None):
        """Called each moment this state can be processed.
        
        time_passed {float} Number of seconds since this function was last
        called.
        
        returns {str|None} can return a str as a message, otherwise return
        None for no massage (and no transition).
        """
        pass

    def enter(self):
        """Called when this state is entered.
        """
        pass    
    
    def exit(self):
        """Called when the brain transitions out of this state into a new one.
        """
        pass



class StateManager(object):
    """Simple, finite state machine.
    """
    def __init__(self):
        """Initialize.
        """
        # Available states indexed by name.
        self.states = {}
        # What is the currently set state?
        self.active_state = None
    
    def add_state(self, state):
        """Place another state under management.
        """
        self.states[state.name] = state
        
    def process(self, time_passed=None):
        """Process the current state and determine if there is a state
        transition.
        
        time_passed {float} Number of seconds since the last time this was
        called.
        """
        if self.active_state is None:
            return

        # Message returned is treated as a state transition attempt.
        new_state_name = self.active_state.process(time_passed)
        if new_state_name is not None:
            self.set_state(new_state_name)
        
    def set_state(self, new_state_name):
        """Transition from one state to the next.
        
        Should be called to set the first active_state.
        
        new_state_name {str} Key to the new state. Must be a valid state name,
        or None which will make the current state nothing.
        """
        if self.active_state is not None:
            self.active_state.exit()
        
        if new_state_name is not None:
            self.active_state = self.states[new_state_name]        
            self.active_state.enter()
        else:
            self.active_state = None


