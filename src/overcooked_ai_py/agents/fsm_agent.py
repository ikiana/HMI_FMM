from overcooked_ai_py.agents.agent import Agent  # Assuming you have a base Agent class
from overcooked_ai_py.fsm.fsm import FiniteStateMachine
from overcooked_ai_py.fsm.fsm_utils import initialize_chef_fsm


class FSMChefAgent(Agent):
    """
    A chef agent that operates based on a Finite State Machine (FSM).
    The FSM dictates the agent's state transitions and actions based on the game state.
    """

    def __init__(self):
        """
        Initialize the FSMChefAgent with an FSM for decision-making.
        """
        super().__init__()
        self.fsm = FiniteStateMachine()
        initialize_chef_fsm(self.fsm)  # Initialize FSM with default states and transitions

    def reset(self):
        """
        Reset the agent's FSM to the initial state.
        """
        self.fsm.set_state("IDLE")

    def action(self, state_info):
        """
        Define the agent's actions based on the current FSM state and game state.

        Parameters:
        - state_info: A dictionary containing the current state of the kitchen (e.g., location, holding, orders).

        Returns:
        - action: The action the agent will take (e.g., "pickup_onion", "move_to_pot").
        """
        # Extract necessary info from the game state
        agent_location = state_info["location"]
        agent_holding = state_info["holding"]
        orders = state_info["orders"]

        # Update the FSM with the current game state
        self.fsm.update(agent_holding, agent_location, orders)

        # Based on the FSM state, choose an action
        fsm_state = self.fsm.get_state()

        if fsm_state == "IDLE":
            return self.idle_action()
        elif fsm_state == "PREPARE_SOUP":
            return self.prepare_soup_action()
        elif fsm_state == "PICKING_ONION":
            return self.pick_onion_action()
        elif fsm_state == "COOKING_SOUP":
            return self.cook_soup_action()
        elif fsm_state == "DELIVER_SOUP":
            return self.deliver_soup_action()

    def idle_action(self):
        """
        Define what the agent does while in the IDLE state.
        """
        return "wait"

    def prepare_soup_action(self):
        """
        Define what the agent does while in the PREPARE_SOUP state.
        """
        return "move_to_onion_station"  # Example action: move toward onion station

    def pick_onion_action(self):
        """
        Define what the agent does while in the PICKING_ONION state.
        """
        return "pickup_onion"  # Example action: pick up onion

    def cook_soup_action(self):
        """
        Define what the agent does while in the COOKING_SOUP state.
        """
        return "move_to_pot"  # Example action: move toward pot to cook

    def deliver_soup_action(self):
        """
        Define what the agent does while in the DELIVER_SOUP state.
        """
        return "deliver_soup"  # Example action: deliver the soup to the delivery point
