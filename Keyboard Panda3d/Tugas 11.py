# Inisialisasi atau memanggil fungsi
from math import pi, sin, cos 

from direct.showbase.ShowBase import ShowBase 
from direct.task import Task 
from direct.actor.Actor import Actor 
from panda3d.core import ClockObject

#sebagai kunci tombol kiri kanan dan memutar
keyMap = {
    "left": False,
    "right": False,
    "rotate": False
}

def updateKeyMap(key, state):
    keyMap[key] = state

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Menonakfitkan fungsi trackball kamera
        self.disableMouse()
        self.scene = self.loader.loadModel("models/environment")
        self.scene.reparentTo(self.render)
        self.scene.setScale(0.25, 0.25, 0.25)   # Mengatur transformasi atau perubahan skala dan posisi pada model
        self.scene.setPos(-8, 42, 0)

        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")   # Menambah pengaturan spin kamera

        # Meload dan mengubah aktor
        self.Panda = Actor("models/panda-model",
                           {"walk": "models/panda-walk4"})
        self.Panda.setScale(0.005, 0.005, 0.005)
        self.Panda.reparentTo(self.render)
        
        self.Panda.loop("walk") # meloop gerak panda
        
        # Mengatur gerak fungsi dari keyboard
        self.accept("arrow_left", updateKeyMap, ["left", True])
        self.accept("arrow_left-up", updateKeyMap, ["left", False])

        self.accept("arrow_right", updateKeyMap, ["right", True])
        self.accept("arrow_right-up", updateKeyMap, ["right", False])

        self.accept("space", updateKeyMap, ["rotate", True])
        self.accept("space-up", updateKeyMap, ["rotate", False])

        self.speed=6
        self.angle=0

        self.taskMgr.add(self.update, "update")

    # Mengatur penyesuaian gerak kamera
    def spinCameraTask(self, task):
        angleDegrees=task.time * 6.0
        angleRadians=angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20 * cos(angleRadians), 3)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont

    def update(self, task):

        globalClock = ClockObject.getGlobalClock()

        dt = globalClock.getDt()

        pos = self.Panda.getPos()

        if keyMap["left"]:
            pos.x -= self.speed * dt
        if keyMap["right"]:
            pos.x += self.speed * dt
        if keyMap["rotate"]:
            self.angle += 1
            self.Panda.setH(self.angle)

        self.Panda.setPos(pos)

        return task.cont

app = MyApp()

# Penambah dan pengaturan musik
mySound = app.loader.loadSfx("lagu/game.ogg") 
mySound.play()
mySound.setLoop(True)
mySound.setVolume(50)
app.run()