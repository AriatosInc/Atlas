import random
from utilities.config import read_config


class Factory:
    """
    Factory class for creating agents based on configuration.

    Args:
        config (dict): Configuration dictionary.
        agent_class_type (class): Class type for the agent.

    Attributes:
        environment (object): Environment object.
        agent_class (class): Class type for the agent.
        weights (dict): Configuration weights.
        expected_weights (list): List of expected weight names.

    """

    def __init__(self, config, agent_class_type):
        """
        Constructor for the class.

        :param config: Configuration settings for the environment.
        :type config: dict
        # TODO: ADD EXAMPLE CONFIGURATION TO DOCUMENTATION

        :param agent_class_type: The class type for the agent.
        :type agent_class_type: type

        :returns: None
        """

        self.environment = None
        self.agent_class = agent_class_type

        # Set up the Factory
        self.weights = read_config(config)
        self.expected_weights = []
        self._generate_weights()

    def _generate_weights(self):
        """
        Generate weights based on the configuration.

        :return: None
        :raises KeyError: If a weight distribution key is not found in the weights configuration.
        """
        self.expected_weights = self._extract_weight_names()

        for weight in self.expected_weights:
            dist_key = weight + "_dist"
            if dist_key in self.weights:
                setattr(self, weight, self.weights[dist_key])
            else:
                raise KeyError(f"{dist_key} not found in the weights configuration.")

    def _extract_weight_names(self):
        """
        Extracts weight names from the keys in the weights dictionary.

        :return: A list of weight names without the '_dist' suffix.
        :rtype: list
        """
        weight_names = []
        for key in self.weights.keys():
            if key.endswith("_dist"):
                weight_names.append(key[:-5])  # Remove '_dist' suffix
        return weight_names

    def create_agent(self, start_bubble):
        """
        Create an agent with the specified starting bubble.

        :param start_bubble: The starting bubble for the agent.
        :return: The created agent.
        :raises ValueError: If the environment is not yet attached to the factory.
          Use factory.connect_environment(env) to connect.
        """

        if self.environment is None:
            raise ValueError("Environment not yet attached to the factory. "
                             "Use factory.connect_environment(env) to connect")

        agent_params = {
            "current_bubble": start_bubble,
            "environment": self.environment
        }

        # Add parameters from distribution
        for weight in self.expected_weights:
            # Get names and distributions from the configuration
            state_name = f"{weight}_states"
            dist_name = f"{weight}_dist"
            if state_name in self.weights and dist_name in self.weights:
                states = self.weights[state_name]
                dist = self.weights[dist_name]
                # Generate a state for each parameter from the distribution
                agent_params[weight] = random.choices(states, weights=dist, k=1)[0]

        return self.agent_class(**agent_params)

    def create_agents(self, num_agents, start_bubble):
        """
        :param num_agents: The number of agents to be created.
        :param start_bubble: The starting bubble for each agent.

        :return: A list of agent objects.
        """
        agents = []
        for _ in range(num_agents):
            agent = self.create_agent(start_bubble)
            agents.append(agent)
        return agents

    def connect_environment(self, environment):
        """
        :param environment: The environment to connect to
        :return: None

        """
        self.environment = environment
