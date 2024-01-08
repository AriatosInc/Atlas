import uuid


class Bubble:
    """
    Class Bubble

    A class representing a bubble in an environment.

    Attributes:
        id (uuid.UUID): The unique identifier for the bubble.
        environment (str): The environment in which the bubble exists.
        slug (str): The slug or name of the bubble.
        description (str): The description of the bubble.
        depth (int): The depth of the bubble in the environment.

        current_agents (AgentList): The list of agents currently in the bubble.
        connections (ConnectionsList): The list of connections to other bubbles.

    Methods:
        __init__(slug, description, depth, environment)
            Initializes a new instance of the Bubble class.

            Args:
                slug (str): The slug or name of the bubble.
                description (str): The description of the bubble.
                depth (int): The depth of the bubble in the environment.
                environment (str): The environment in which the bubble exists.

        __str__()
            Returns the string representation of the bubble.

            Returns:
                str: The string representation of the bubble.

        get_occupancy()
            Gets the occupancy of the bubble.

            Returns:
                int: The occupancy of the bubble.

        add_agent(agent)
            Adds an agent to the bubble.

            Args:
                agent (Agent): The agent to add to the bubble.

        remove_agent(agent)
            Removes an agent from the bubble.

            Args:
                agent (Agent): The agent to remove from the bubble.

        connect(other_bubble)
            Connects the bubble to another bubble.

            Args:
                other_bubble (Bubble): The other bubble to connect to.

        get_connected_bubbles(bubble_slug)
            Gets the connected bubbles with the specified slug.

            Args:
                bubble_slug (str): The slug of the bubble.

            Returns:
                list: The list of connected bubbles.

        get_waiting()
            Gets the waiting count for the bubble.

            Returns:
                int: The waiting count for the bubble.
    """
    def __init__(self, slug, description, depth, environment):
        self.id = uuid.uuid4()
        self.environment = environment
        self.slug = slug
        self.description = description
        self.depth = depth

        self.current_agents = AgentList()
        self.connections = ConnectionsList()

    def __str__(self):
        return f"Bubble: {self.slug} - {self.description}"

    def get_occupancy(self):
        return self.current_agents.get_occupancy()

    def add_agent(self, agent):
        self.current_agents.add(agent)

    def remove_agent(self, agent):
        self.current_agents.remove(agent)

    def connect(self, other_bubble):
        self.connections.add(other_bubble)

    def get_connected_bubbles(self, bubble_slug):
        return self.connections.get(bubble_slug)

    def get_waiting(self):
        return 0    # waiting list implemented in child objects


class AgentList:
    """
    The AgentList class represents a list of agents.

    Methods:
        - add(agent): Adds an agent to the list.
        - remove(agent): Removes an agent from the list.
        - get_occupancy(): Returns the number of agents in the list.

    Attributes:
        - _agents: A private list to store the agents.

    Example Usage:
        # Create an instance of AgentList
        agent_list = AgentList()

        # Add agents to the list
        agent_list.add(agent1)
        agent_list.add(agent2)

        # Remove an agent from the list
        agent_list.remove(agent1)

        # Get the number of agents in the list
        occupancy = agent_list.get_occupancy()

    Note:
        - All methods in this class print messages to the console for demonstration purposes. Modify the methods as needed.
        - The AgentList class does not provide direct access to the agents in the list, only methods to add, remove, and get occupancy.
    """
    def __init__(self):
        self._agents = []

    def __str__(self):
        agents_info = "\n".join(str(agent) for agent in self._agents)
        return f"--- AgentList ---\n{agents_info}"

    def add(self, agent):
        print(f"Adding agent {agent.id}")
        self._agents.append(agent)

    def remove(self, agent):
        if agent in self._agents:
            print(f"Removing agent {agent.id} from bubble")
            self._agents.remove(agent)
        else:
            # Handling the case where the agent is not found in the current bubble
            agent_current_bubble_slug = agent.current_bubble.slug if agent.current_bubble else "None"
            print(
                f"Error: Attempted to remove agent {agent.id} from bubble, but the agent was not found. "
                f"Agent's current bubble: {agent_current_bubble_slug}")

    def get_occupancy(self):
        return len(self._agents)


class ConnectionsList:
    """
    Initialize a new ConnectionsList object.

    :return: None
    """
    def __init__(self):
        self._connections = []

    def add(self, other_bubble):
        # Connects bubble objects to others
        self._connections.append(other_bubble)

    def get(self, bubble_slug):
        try:
            bubble = next(bubble for bubble in self._connections if bubble.slug == bubble_slug)
        except StopIteration:
            bubble = None
        return bubble