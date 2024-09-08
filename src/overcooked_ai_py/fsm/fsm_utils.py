# Utility function to check if an agent is at a specific location
def is_at_location(agent_location, target_location):
    """
    Check if an agent is at a specified target location.

    Parameters:
    - agent_location: The current location of the agent (string).
    - target_location: The location to check against (string).

    Returns:
    - bool: True if the agent is at the target location, False otherwise.
    """
    return agent_location == target_location


# Utility function to check if an agent is holding a specific item
def is_holding_item(agent_holding, target_item):
    """
    Check if an agent is holding a specified item.

    Parameters:
    - agent_holding: The current item the agent is holding (string).
    - target_item: The item to check against (string).

    Returns:
    - bool: True if the agent is holding the target item, False otherwise.
    """
    return agent_holding == target_item


# Utility function to check if orders exist
def has_orders(orders_list):
    """
    Check if there are any orders in the list.

    Parameters:
    - orders_list: A list of orders.

    Returns:
    - bool: True if there are any orders, False otherwise.
    """
    return len(orders_list) > 0


# Utility function to log FSM transitions for debugging
def log_fsm_transition(from_state, to_state):
    """
    Log FSM transitions from one state to another.

    Parameters:
    - from_state: The state the FSM is transitioning from (string).
    - to_state: The state the FSM is transitioning to (string).

    Returns:
    - None
    """
    print(f"FSM transition from {from_state} to {to_state}")


# Utility function to initialize FSM with default states and transitions
def initialize_chef_fsm(chef_fsm):
    """
    Initialize a chef FSM with predefined states and transitions.

    Parameters:
    - chef_fsm: An instance of FiniteStateMachine.

    Returns:
    - None
    """
    # Define states
    chef_fsm.add_state("IDLE")
    chef_fsm.add_state("PREPARE_SOUP")
    chef_fsm.add_state("PICKING_ONION")
    chef_fsm.add_state("COOKING_SOUP")
    chef_fsm.add_state("DELIVER_SOUP")

    # Define transitions
    chef_fsm.add_transition("IDLE", "PREPARE_SOUP", has_orders)  # Transition based on orders
    chef_fsm.add_transition("PREPARE_SOUP", "PICKING_ONION",
                            lambda holding, location: is_holding_item(holding, "empty") and is_at_location(location,
                                                                                                           "at_onion_station"))
    chef_fsm.add_transition("PICKING_ONION", "COOKING_SOUP", lambda holding: is_holding_item(holding, "onion"))
    chef_fsm.add_transition("COOKING_SOUP", "DELIVER_SOUP", lambda holding: is_holding_item(holding, "soup"))
    chef_fsm.add_transition("DELIVER_SOUP", "IDLE", lambda holding: is_holding_item(holding, "empty"))

    print("Chef FSM initialized with default states and transitions.")
