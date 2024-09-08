import unittest
from overcooked_ai_py.fsm.fsm import FiniteStateMachine
from overcooked_ai_py.fsm.fsm_utils import is_at_location, is_holding_item


class TestFSM(unittest.TestCase):

    def setUp(self):
        """
        Set up the FSM with some basic states and transitions for testing.
        """
        self.fsm = FiniteStateMachine()
        self.fsm.add_state("IDLE")
        self.fsm.add_state("PICKING_ONION")
        self.fsm.add_state("COOKING_SOUP")

        # Example transition: from IDLE to PICKING_ONION when at onion station
        self.fsm.add_transition("IDLE", "PICKING_ONION",
                                lambda holding, location: is_holding_item(holding, "empty") and is_at_location(location,
                                                                                                               "at_onion_station"))

        # Example transition: from PICKING_ONION to COOKING_SOUP when holding onion
        self.fsm.add_transition("PICKING_ONION", "COOKING_SOUP", lambda holding: is_holding_item(holding, "onion"))

    def test_initial_state(self):
        """
        Test that the FSM starts in the correct initial state (None or IDLE).
        """
        self.assertIsNone(self.fsm.get_state(), "FSM should start with no state set.")

        # Set state and check if it initializes correctly
        self.fsm.set_state("IDLE")
        self.assertEqual(self.fsm.get_state(), "IDLE", "FSM did not correctly set the initial state.")

    def test_transition_to_picking_onion(self):
        """
        Test that the FSM transitions from IDLE to PICKING_ONION when conditions are met.
        """
        self.fsm.set_state("IDLE")
        self.fsm.update("empty", "at_onion_station", ["soup"])  # Holding nothing, at onion station
        self.assertEqual(self.fsm.get_state(), "PICKING_ONION", "FSM did not transition to PICKING_ONION.")

    def test_transition_to_cooking_soup(self):
        """
        Test that the FSM transitions from PICKING_ONION to COOKING_SOUP when conditions are met.
        """
        self.fsm.set_state("PICKING_ONION")
        self.fsm.update("onion", "at_pot_station", ["soup"])  # Holding onion
        self.assertEqual(self.fsm.get_state(), "COOKING_SOUP", "FSM did not transition to COOKING_SOUP.")

    def test_no_transition_when_conditions_not_met(self):
        """
        Test that the FSM does not transition if the conditions are not met.
        """
        self.fsm.set_state("IDLE")
        self.fsm.update("empty", "not_onion_station", ["soup"])  # Not at onion station
        self.assertEqual(self.fsm.get_state(), "IDLE", "FSM transitioned when it should not have.")

    def test_state_entry_exit_actions(self):
        """
        Test that state entry and exit actions are called when states are entered or exited.
        """

        def on_enter_picking_onion():
            print("Entering PICKING_ONION")

        def on_exit_idle():
            print("Exiting IDLE")

        # Add entry/exit actions
        self.fsm.add_state("PICKING_ONION", on_enter=on_enter_picking_onion)
        self.fsm.add_state("IDLE", on_exit=on_exit_idle)

        # Set state to IDLE and then transition to PICKING_ONION
        self.fsm.set_state("IDLE")
        self.fsm.update("empty", "at_onion_station", ["soup"])

        # Check state
        self.assertEqual(self.fsm.get_state(), "PICKING_ONION")


if __name__ == "__main__":
    unittest.main()
