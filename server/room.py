class Room:
    def __init__(self, name: str):
        self.name = name

    def connect(self, client: str) -> bool:
        """
        connecting in room
        :param client: client name
        :return: bool
        """
        pass

    def disconnect(self, client: str) -> bool:
        """
        disconnecting off room
        :param client: client name
        :return: bool
        """
        pass
