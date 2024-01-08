import uuid


class Connection:
    """
    :class: Connection

    A class representing a connection between two bubbles.

    Attributes:
        id (UUID): The unique identifier for the connection.
        start (Bubble): The starting bubble of the connection.
        end (Bubble): The ending bubble of the connection.

    Methods:
        __init__(start_bubble, end_bubble): Initializes a new Connection object with the given start and end bubbles.

    """
    def __init__(self, start_bubble, end_bubble):

        self.id = uuid.uuid4()
        self.start = start_bubble
        self.end = end_bubble

        self.start.connect(end_bubble)
