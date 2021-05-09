class Scene(object):
    def __init__(self, state="menu"):
        self.running = True
        sce = {"hi":5}
        self.scenes = {
            "game" : Game(),
            "menu" : MainMenu(),
            "tuning" : Tuning()
        }
        self.current_scene = self.scenes[state]
    
    def change_scene(self, state):
        self.current_scene = self.scenes[state]

    def run(self):
        while self.running:
            self.current_scene.update()

class Game(Scene):

    def __init__(self):
        pass
    def update(self):
        print("game")


class MainMenu(Scene):

    def __init__(self):
        pass

    def update(self):
        print("menu")
        self.abc("game")

    def abc(self, value):
        Scene.sce

class Tuning(Scene):

    def __init__(self):
        pass
    def update(self):
        print("tune")