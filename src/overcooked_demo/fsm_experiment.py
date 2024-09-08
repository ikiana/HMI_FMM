import time
from overcooked_ai_py.mdp.overcooked_mdp import OvercookedGridworld
from overcooked_ai_py.agents.agent import AgentPair
from overcooked_ai_py.fsm.fsm_agent import FSMChefAgent

class FSMExperiment:
    """
    A class for running experiments with FSM-based agents in the Overcooked AI environment.
    """

    def __init__(self, layout_name="cramped_room", num_steps=1000):
        """
        Initialize the experiment with a specific layout and number of steps.

        Parameters:
        - layout_name: The name of the Overcooked layout to use (default: "cramped_room").
        - num_steps: The number of steps to run in the simulation (default: 1000).
        """
        self.layout_name = layout_name
        self.num_steps = num_steps

        # Set up the Overcooked environment and agents
        self.env, self.mdp = self.setup_environment()
        self.agent_pair = self.setup_agents()

        # Results storage for later analysis
        self.results = {
            "actions": [],
            "transitions": [],
            "completion_time": None,
            "orders_completed": 0
        }

    def setup_environment(self):
        """
        Set up the Overcooked environment based on the specified layout.

        Returns:
        - env: The initialized Overcooked environment.
        - mdp: The OvercookedGridworld MDP.
        """
        mdp = OvercookedGridworld.from_layout_name(self.layout_name)
        env = mdp.get_standard_chef_agents()
        print(f"Environment initialized with layout: {self.layout_name}")
        return env, mdp

    def setup_agents(self):
        """
        Set up FSM-based agents for the experiment.

        Returns:
        - agent_pair: A pair of FSMChefAgents to operate in the environment.
        """
        fsm_agent_1 = FSMChefAgent()  # First FSM-based agent
        fsm_agent_2 = FSMChefAgent()  # Second FSM-based agent

        # Create an agent pair
        agent_pair = AgentPair(fsm_agent_1, fsm_agent_2)
        print("FSM agents initialized and paired.")
        return agent_pair

    def run_experiment(self):
        """
        Run the FSM experiment for a given number of steps.
        """
        start_time = time.time()

        for step in range(self.num_steps):
            # Get the current state of the environment
            state = self.mdp.get_state()

            # Get actions from both agents based on the FSM
            actions = self.agent_pair.joint_action(state)

            # Step the environment forward with the chosen actions
            _, reward, done, info = self.env.step(actions)

            # Log actions and transitions at each step
            self.log_step(step, state, actions, info)

            # Check if the episode is done (all orders completed or max steps reached)
            if done:
                break

        end_time = time.time()
        self.results["completion_time"] = end_time - start_time
        print(f"Experiment completed in {self.results['completion_time']:.2f} seconds.")

    def log_step(self, step, state, actions, info):
        """
        Log the details of each step in the experiment, including actions and FSM transitions.

        Parameters:
        - step: The current step number in the experiment.
        - state: The current state of the environment.
        - actions: The actions taken by both agents.
        - info: Additional information returned from the environment (e.g., rewards).
        """
        # Log the actions taken by the agents
        self.results["actions"].append({
            "step": step,
            "state": state,
            "actions": actions,
            "info": info
        })

        # Log FSM transitions
        transition_data = {
            "step": step,
            "agent_1_state": self.agent_pair.agent1.fsm.get_state(),
            "agent_2_state": self.agent_pair.agent2.fsm.get_state()
        }
        self.results["transitions"].append(transition_data)

    def summarize_results(self):
        """
        Print and summarize the results of the experiment.
        """
        print("Experiment Summary:")
        print(f"Total steps: {self.num_steps}")
        print(f"Total completion time: {self.results['completion_time']:.2f} seconds")
        print(f"FSM Transitions: {len(self.results['transitions'])} transitions recorded")
        # Additional metrics can be printed here (e.g., orders completed, actions taken)

    def save_results(self, filename="experiment_results.json"):
        """
        Save the results of the experiment to a file (JSON format).

        Parameters:
        - filename: The name of the file to save the results to (default: "experiment_results.json").
        """
        import json
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=4)
        print(f"Results saved to {filename}")

if __name__ == "__main__":
    # Initialize and run the FSM experiment
    experiment = FSMExperiment(layout_name="cramped_room", num_steps=1000)
    experiment.run_experiment()
    experiment.summarize_results()
    experiment.save_results("fsm_experiment_results.json")
