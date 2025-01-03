class TestScene:
    scene: str

    is_run: bool = False

    def __init__(self, scene: str, is_run: bool):
        self.scene = scene
        self.is_run = is_run

    def get_scenes(self) -> str:
        return self.scene
