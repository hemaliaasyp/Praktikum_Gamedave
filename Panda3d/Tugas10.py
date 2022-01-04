from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from math import pi, sin, cos
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3

#define a class 

class panda(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.scene = self.loader.loadModel("environment")
        self.scene.reparentTo(self.render)
        self.scene.setScale(0.20, 0.20, 0.20)
        self.scene.setPos(-8, 45, 0)

        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")
        self.pandaActor = Actor("panda-model", {"walk": "panda-walk4"})
        self.pandaActor.setScale(0.007,0.007,0.007)
        self.pandaActor.reparentTo(self.render)
        self.pandaActor.loop("walk")
      
        pandaPosInterval1 = self.pandaActor.posInterval(13,Point3(0, -10, 0),
                               startPos=Point3(0, 10, 0))
        pandaPosInterval2 = self.pandaActor.posInterval(13, Point3(0, 10, 0),
                               startPos=Point3(0, -10, 0))
        pandaHprInterval1 = self.pandaActor.hprInterval(3,Point3(180, 0, 0),
                               startHpr=Point3(0, 0, 0))
        pandaHprInterval2 = self.pandaActor.hprInterval(3,Point3(0, 0, 0),
                               startHpr=Point3(180, 0, 0))
        self.pandaPace = Sequence(pandaPosInterval1, pandaHprInterval1, 
                               pandaPosInterval2, pandaHprInterval2)
        self.pandaPace.loop()

        self.menuMusik = self.loader.loadMusic("lagu/game.ogg")
        self.menuMusik.setVolume(0.9)
        self.menuMusik.setLoop(True)
        self.menuMusik.play()
        
    def spinCameraTask(self, task):
        angleDegrees = task.time * 7.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20.0 * cos(angleRadians), 3)
        self.camera.setHpr(angleDegrees, 0, 0)

        return Task.cont
        base = ShowBase()

mypanda = panda()
mypanda.run()
