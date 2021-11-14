from panda3d.core import Vec3, Vec4
from direct.actor.Actor import Actor
from panda3d.core import CollisionSphere, CollisionNode

FRICTION = 150.0

class GameObject():
    def __init__(self, pos, modelName, modelAnims, maxHealth, maxSpeed, colliderName):
        self.actor = Actor(modelName, modelAnims)
        self.actor.reparentTo(render)
        self.actor.setPos(pos)

        self.maxHealth = maxHealth
        self.Health = maxHealth

        self.maxSpeed = maxSpeed

        self.velocity = Vec3(0, 0, 0)
        self.acceleration = 300.0

        self.walking = False

        colliderNode = CollisionNode(colliderName)
        colliderNode.addSolid(CollisionSphere(0, 0, 0, 0.3))
        self.collider = self.actor.attachNewNode(colliderNode)
        self.collider.setPythonTag("owner", self)

    def update(self, dt):
        # if we go faster than the max speed, set the velocity vector's length to that maximum.
        speed = self.velocity.length()
        if speed > self.maxSpeed:
            self.velocity.normalize()
            self.velocity *= self.maxSpeed
            speed = self.maxSpeed
        # If we're walking, don't worry about friction.
        # Otherwise, use friction to slow us down.
        if not self.walking:
            frictionVal = FRICTION*dt
            if frictionVal > speed:
                self.velocity.set(0, 0, 0)
            else:
                frictionVec = -self.velocity
                frictionVec.normalize()
                frictionVec *= frictionVal

                self.velocity += frictionVec

        self.actor.setPos(self.actor.getPos() + self.velocity*dt)

    def alterHealth(self, dHealth):
        self.health += dHealth

        if self.health > self.maxHealth:
            self.health = self.maxHealth

    def cleanup(self):
        # Remove various nodes, and clear the Python-tag
        if self.collider is not None and not self.collider.isEmpty():
            self.collider.clearnPythonTag("owner")
            base.cTrav.removeCollider(self.collider)
            base.pusher.removeCollider(self.collider)
        if self.actor is not None:
            self.actor.cleanup()
            self.actor.removeNode()
            self.actor = None

        self.collider = None

# end game obj class

class Player(GameObject):
    def __init__(self):
        GameObject.__init__(self,
                            Vec3(0, 0, 0),
                            "samplemodels2/act_p3d_chan",
                            {
                                "walk" : "samplemodels2/a_p3d_chan_run",
                                "stand" : "samplemodels2/a_p3d_chan_idle"
                            },
                            5,
                            10,
                            "player")
        self.actor.getChild(0).setH(180)
        base.pusher.addCollider(self.collider, self.actor)
        base.cTrav.addCollider(self.collider, base.pusher)

        self.actor.loop("stand")

    def update(self, keys, dt):
        GameObject.update(self, dt)

        self.walking = False

        if keys["up"]:
            self.walking = True
            self.velocity.addY(self.acceleration * dt)
        if keys["down"]:
            self.walking = True
            self.velocity.addY(-self.acceleration * dt)
        if keys["left"]:
            self.walking = True
            self.velocity.addX(-self.acceleration * dt)
        if keys["right"]:
            self.walking = True
            self.velocity.addX(self.acceleration * dt)

        if self.walking:
            standControl = self.actor.getAnimControl("stand")
            if standControl.isPlaying():
                standControl.stop()

            walkControl = self.actor.getAnimControl("walk")
            if not walk.Control.isPlaying():
                self.actor.loop("walk")
        else:
            standControl = self.actor.getAnimControl("stand")
            if not standControl.isPlaying():
                self.actor.stop("walk")
                self.actor.loop("stand")

# end player class

