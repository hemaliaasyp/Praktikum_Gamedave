#membuat kelas Scene untuk langkah pertama sebagai kelas tampilan
class Scene():
#mendeklarasikan variabel self
  def __init__(self):
        pass

    def handle_events(self, events):
        raise NotImplementedError
#mendeklarasikan metode    
    def update(self):
        raise NotImplementedError
#mendeklarasikan def draw
    def draw(self, window):
        raise NotImplementedError

class SceneManager(object):
#mendeklarasikan variabel "self" "InitScene"
    def __init__(self, InitScene):
        self.go_to(InitScene)
#mendeklarasikan sebuah metode
    def go_to(self, scene):
        self.scene = scene
        self.scene.manager = self