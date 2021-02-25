from direct.directbase.DirectStart import base
from direct.task.TaskManagerGlobal import taskMgr
from direct.interval.IntervalGlobal import *
from NightWind3DLib2.TransformModel import model_position
from NightWind3DLib2.TextDisplay import *
from panda3d.core import *
import random
alien = []
sequences = []
score = 0
delay = 1


def load_model(ModelPath):
    model = loader.loadModel(ModelPath)
    model.reparentTo(render)
    model.setTransparency(True)
    hide = model.colorInterval(3, (1, 1, 1, 0), (1, 1, 1, 1))
    appear = model.colorInterval(3, (1, 1, 1, 1), (1, 1, 1, 0))
    sequences.append(Sequence(appear, Wait(1), hide))
    Sphere = CollisionSphere(0, 0, 110, 30)
    SphereNode = CollisionNode("alien")
    SphereNode.addSolid(Sphere)
    ModelCollision = model.attachNewNode(SphereNode)
    alien.append(model)


def main():
    window = WindowProperties()
    window.setTitle("Hit The Alien")
    window.setSize(1200, 800)

    # 将属性传递给主窗体
    base.win.requestProperties(window)

    # 加载并显示场景模型文件
    scene = loader.loadModel("images_alien/woodland")
    scene.reparentTo(render)

    # 设置镜头位置及角度
    base.cam.setPos(0, -1200, 1200)
    base.cam.setHpr(0, -45, 0)
    base.disableMouse()

    # 设置窗体背景色
    base.setBackgroundColor(0/255, 128/255, 255/255)

    # 加载外星人
    load_model("images_alien/alien_1")
    load_model("images_alien/alien_2")
    load_model("images_alien/alien_3")

    # 加载锤子
    hammer = loader.loadModel("images_alien/hammer")
    hammer.reparentTo(render)

    # 为锤子添加碰撞体
    sphere = CollisionSphere(-40, 0, 125, 25)
    sphereNode = CollisionNode("hammer")
    sphereNode.addSolid(sphere)
    HammerCollision = hammer.attachNewNode(sphereNode)

    # 处理碰撞
    base.cTrav = CollisionTraverser()
    QueueHandler = CollisionHandlerQueue()
    base.cTrav.addCollider(HammerCollision, QueueHandler)

    # 移动方法
    def move_task(task):
        global score, delay
        delay -= 0.01
        display(f"Score: {score}")
        for i in range(0, 3):
            if sequences[i].isStopped():
                alien[i].setPos(random.randint(-320, 320), random.randint(-240, 240), 0)
                sequences[i][1] = Wait(random.uniform(0.5, 3))
                sequences[i].start()

        # 处理碰撞
        if QueueHandler.getNumEntries() > 0:
            QueueHandler.sortEntries()
            if QueueHandler.getEntry(0).getIntoNode().getName() == "alien":
                score += 1
                delay = 1
                QueueHandler.getEntry(0).getIntoNodePath().getParent().setColor((1, 1, 1, 0))
                QueueHandler.getEntry(0).getIntoNodePath().getParent().setPos(
                    random.randint(-320, 320), random.randint(-240, 240), 0)

        model_position(hammer)
        return task.cont

    taskMgr.add(move_task)

    # 设置敲击效果
    def knock(leftButton):
        status = leftButton
        if status:
            hammer.setR(-60)
        else:
            hammer.setR(0)

    base.accept("mouse1", knock, [True])
    base.accept("mouse1-up", knock, [False])

    # 运行主程序
    base.run()


if __name__ == "__main__":
    main()
