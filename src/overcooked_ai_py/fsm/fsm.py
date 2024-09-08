class FiniteStateMachine:
    def __init__(self):
        """
        Initialize the FSM with an empty state and transitions.
        """
        self.state = None
        self.transitions = {}
        self.actions = {}

    def add_state(self, state_name, on_enter=None, on_exit=None):
        """
        Add a state to the FSM.

        Parameters:
        - state_name: The name of the state (string).
        - on_enter: Optional function to be executed when entering this state.
        - on_exit: Optional function to be executed when exiting this state.
        """
        self.transitions[state_name] = {}
        self.actions[state_name] = {
            'on_enter': on_enter,
            'on_exit': on_exit
        }

    def add_transition(self, from_state, to_state, condition):
        """
        Add a transition between two states based on a condition.

        Parameters:
        - from_state: The starting state (string).
        - to_state: The state to transition to (string).
        - condition: A function that evaluates to True or False, indicating
                     whether the transition should occur.
        """
        if from_state not in self.transitions:
            raise ValueError(f"State {from_state} does not exist")
        self.transitions[from_state][to_state] = condition

    def set_state(self, new_state):
        """
        Set the current state of the FSM, triggering any on_exit or on_enter functions.

        Parameters:
        - new_state: The new state to transition into.
        """
        if self.state is not None:
            self._exit_state(self.state)
        self.state = new_state
        self._enter_state(new_state)

    def _enter_state(self, state):
        """
        Call the on_enter function of the new state (if any).

        Parameters:
        - state: The state being entered.
        """
        on_enter = self.actions[state].get('on_enter')
        if on_enter:
            on_enter()

    def _exit_state(self, state):
        """
        Call the on_exit function of the old state (if any).

        Parameters:
        - state: The state being exited.
        """
        on_exit = self.actions[state].get('on_exit')
        if on_exit:
            on_exit()

    def update(self, *args):
        """
        Check the conditions for transitioning between states and make the transition if possible.

        Parameters:
        - *args: Additional arguments passed to condition functions (e.g., kitchen state, chef location).
        """
        current_state_transitions = self.transitions.get(self.state, {})
        for to_state, condition in current_state_transitions.items():
            if condition(*args):  # If the condition is true, transition to the new state
                self.set_state(to_state)
                break

    def get_state(self):
        """
        Get the current state of the FSM.

        Returns:
        - The current state (string).
        """
        return self.state
