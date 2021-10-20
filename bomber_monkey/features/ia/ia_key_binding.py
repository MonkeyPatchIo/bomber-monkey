class IAKeyBinding:
    def __init__(self, left_description: str, right_description: str, left_key: int, right_key: int):
        self.left_description = left_description
        self.right_description = right_description
        self.left_key = left_key
        self.right_key = right_key