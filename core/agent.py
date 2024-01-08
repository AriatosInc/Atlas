import uuid


class Agent:
    """
    Agent class

    This class represents an agent in a simulation environment. Agents can move between bubbles and decide on their next event.

    Attributes:
        environment (Environment): The simulation environment that the agent exists in.
        id (uuid.UUID): The unique identifier for the agent.
        current_bubble (Bubble): The current bubble that the agent is in.
        event_slug_dict (dict): A dictionary mapping bubble slugs to functions that decide the next event for the agent.

    Methods:
        __init__(self, current_bubble, environment): Initializes a new Agent instance.
        __str__(self): Returns a string representation of the agent.
        move_agent(self, bubble): Moves the agent to a new bubble.
        decide_and_schedule_next_event(self, event_time=None): Decides on the next event for the agent and schedules it.
        decide_next_event(self): Decides on the next event for the agent based on the current bubble.

    """

    def __init__(self, current_bubble, environment):
        self.environment = environment
        self.id = uuid.uuid4()
        self.current_bubble = current_bubble
        self.event_slug_dict = {}

    def __str__(self):
        return f'{self.id} @ {self.current_bubble}'

    def move_agent(self, bubble):
        self.current_bubble = bubble
        bubble.add_agent(agent=self)

    def decide_and_schedule_next_event(self, event_time=None):
        """

        Decide and Schedule Next Event

        :param event_time: The time at which the event should occur. If not provided, the current time of the environment will be used.
        :return: None

        This method determines the next event for the agent and schedules it in the environment. If the event type is "stay", the agent remains in the current bubble. If the event type is a
        * movement, the agent is scheduled to move to the next bubble.

        Example usage:
            agent.decide_and_schedule_next_event(event_time=10)

        """

        if event_time is None: event_time = self.environment.time
        next_event_slug, event_type = self.decide_next_event()

        if event_type == "stay":
            self.handle_stay_event(next_event_slug)
        elif event_type is not None:
            self.schedule_movement_event(next_event_slug, event_time)
        else:
            raise ValueError

    def handle_stay_event(self, next_event_slug):
        """
          Handles the case where the agent stays in the current bubble.
        """
        print(f"Agent {self.id} will stay in {self.current_bubble.slug}")

    def schedule_movement_event(self, next_event_slug, event_time):
        """
         Schedules a movement event to the next bubble identified by the next_event_slug.
        """
        next_bubble = self.current_bubble.get_connected_bubbles(next_event_slug)
        if not next_bubble:
            print(f"Error: No connected bubble found for slug: {next_event_slug}")
            raise ValueError(f"No connected bubble found for slug: {next_event_slug}")
        print(f"Scheduling movement event for Agent {self.id} to {next_event_slug} at time {event_time}")

        from core import MovementEvent
        movement_event = MovementEvent(event_time, self, self.current_bubble, next_bubble)
        self.environment.schedule_event(movement_event)

    def decide_next_event(self):
        """
        Method `decide_next_event` is used to check the current bubble and determine the next step.

        :return: The decision regarding the next event.
        """
        # Check the current bubble and decide the next step

        decision = self.event_slug_dict[self.current_bubble.slug]()
        print(f"Person {self.id} decided on next event: {decision}")
        return decision
