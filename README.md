Code Architecture

FSM Logic (New Module)

src/
  overcooked_ai_py/
    fsm/
      __init__.py
      fsm.py           # Contains the FiniteStateMachine class
      fsm_utils.py     # Any additional utilities or helper functions

Breakdown of Key Functions (fsm.py):
__init__(): Initializes the FSM with an empty state and dictionaries for storing state transitions and actions (on entering or exiting states).
add_state(state_name, on_enter=None, on_exit=None): Adds a new state to the FSM, with optional functions for actions when entering or exiting the state.
add_transition(from_state, to_state, condition): Defines a transition between two states, where the transition occurs if the condition function returns True.
set_state(new_state): Updates the FSM to the new state and triggers any exit actions from the previous state and entry actions for the new state.
_enter_state(state): Internal helper to run the on-enter function for a state.
_exit_state(state): Internal helper to run the on-exit function for a state.
update(*args): Evaluates transitions based on the current state and the passed arguments (e.g., kitchen state, agent location). Transitions occur if the condition returns True.
get_state(): Returns the current state of the FSM.
Breakdown of Key Functions (fsm_utils.py):
is_at_location(agent_location, target_location):
This utility function checks whether an agent (human or AI) is at a specified location. It simplifies writing conditions for FSM transitions based on location, like "at_onion_station."
is_holding_item(agent_holding, target_item):
This function checks whether the agent is holding a specified item (e.g., "onion," "dish"). This is useful for conditions related to the agent’s inventory.
has_orders(orders_list):
This checks whether there are any outstanding orders, which is a common condition for transitioning from an idle state to an active state like "PREPARE_SOUP."
log_fsm_transition(from_state, to_state):
This utility logs FSM transitions to help with debugging. It's useful during development to ensure that FSM transitions are happening as expected.
initialize_chef_fsm(chef_fsm):
This function helps initialize a chef FSM with default states and transitions. It sets up common tasks such as preparing, picking ingredients, cooking, and delivering dishes in Overcooked AI. You can extend or modify this as needed for more complex behavior.

*We can expand fsm_utils.py to include more conditions or transition helpers specific to Overcooked environments.*


src/
  overcooked_ai_py/
    agents/
      fsm_agent.py    # Contains agents that implement FSM logic
Breakdown of Key Components (fsm_agent.py):
FSM Integration:
The agent contains an instance of FiniteStateMachine, which drives its state transitions and actions. The FSM is initialized with states like IDLE, PREPARE_SOUP, PICKING_ONION, etc., through initialize_chef_fsm().
action() Method:
This method is the heart of the agent. It receives the current game state (such as the agent’s location, what it's holding, and the list of orders) and updates the FSM based on this information.
The method then determines the appropriate action based on the FSM's current state. For example, if the agent is in the PICKING_ONION state, it returns the action pickup_onion.
State-Specific Action Methods:
Each FSM state has a corresponding action method, such as idle_action(), prepare_soup_action(), etc. These methods define what the agent should do while in each state.
You can further extend these methods to handle more complex behavior or introduce randomness in agent decisions.
Resetting the Agent:
The reset() method is included to reset the agent's FSM to the initial state (IDLE). This can be useful when restarting episodes or games.
src/
  overcooked_demo/
    fsm_experiment.py  # Contains the logic to run FSM-based Overcooked AI experiments

Breakdown of Key Components (fsm_experiment.py):
Initialization (__init__):
Sets up the experiment parameters such as the Overcooked layout and the number of steps.
Initializes the environment (setup_environment()) and agents (setup_agents()).
setup_environment():
Initializes the Overcooked environment using the selected layout.
Uses OvercookedGridworld.from_layout_name() to load the layout, and sets up a standard environment with chefs.
setup_agents():
Creates two FSM-based agents (FSMChefAgent) and pairs them using AgentPair.
run_experiment():
The core loop that runs the experiment for a specified number of steps (num_steps).
At each step, it retrieves the current environment state, collects actions from the FSM-based agents, steps the environment forward, and logs the actions and FSM state transitions.
Stops early if the experiment is "done" (all orders are completed).
log_step():
Logs the actions taken by the agents and records their FSM state transitions at each step.
summarize_results():
Prints a summary of the experiment results, such as the number of steps, the completion time, and the FSM transitions.
save_results():
Saves the results of the experiment to a JSON file for further analysis.



testing/
  test_fsm.py        # Tests for FSM logic
  test_fsm_agent.py  # Tests for FSM-based agents


Key Tests in test_fsm.py:
test_initial_state: Verifies that the FSM starts in the correct state (either None or the first manually set state).
test_transition_to_picking_onion: Tests that the FSM transitions from IDLE to PICKING_ONION when the correct conditions (location and holding) are met.
test_transition_to_cooking_soup: Ensures that the FSM transitions from PICKING_ONION to COOKING_SOUPwhen the agent is holding an onion.
test_no_transition_when_conditions_not_met: Ensures that no transition happens if the transition conditions are not met.
test_state_entry_exit_actions: Verifies that the FSM correctly calls entry/exit functions when entering or exiting states.
Key Tests in (test_fsm_agent.py):
test_initial_state_idle: Ensures that the FSM-based agent starts in the IDLE state when reset.
test_action_in_idle_state: Tests that the agent performs the correct action (wait) when in the IDLE state.
test_transition_to_prepare_soup: Tests that the agent transitions to PREPARE_SOUP when conditions are met and performs the appropriate action (move_to_onion_station).
test_transition_to_picking_onion: Ensures that the agent transitions to PICKING_ONION and performs the correct action (pickup_onion).
test_action_in_cooking_soup_state: Tests that the agent correctly performs the action for.
