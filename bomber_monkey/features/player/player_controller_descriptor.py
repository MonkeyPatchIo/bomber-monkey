from bomber_monkey.features.player.input_mapping import InputMapping


class PlayerControllerDescriptor:
    def __init__(self, name: str, input_mapping: InputMapping):
        self.name = name
        self.input_mapping = input_mapping