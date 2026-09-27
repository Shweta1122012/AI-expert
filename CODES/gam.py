import math
import random
import sys

from direct.gui.OnscreenText import OnscreenText
from direct.showbase.ShowBase import ShowBase
from panda3d.core import (
    AmbientLight,
    BitMask32,
    CardMaker,
    CollisionHandlerPusher,
    CollisionNode,
    CollisionSphere,
    CollisionTraverser,
    CollisionBox,
    Spotlight,
    TextNode,
    Vec3,
)


WORLD_SIZE = 80.0
ROOM_SIZE = 18.0
WALL_HEIGHT = 4.0
WALL_THICKNESS = 0.6
ROOM_GRID = (5, 4)
PLAYER_SPEED = 7.0
SPRINT_MULT = 1.6
MOUSE_SENS = 0.2
TOOL_NAMES = ["EMF", "Spirit Box", "Temperature"]
TOOL_KEYS = ["1", "2", "3"]


def clamp(value, lo, hi):
    return max(lo, min(hi, value))


class HorrorGame(ShowBase):
    def __init__(self):
        super().__init__()
        self.disableMouse()
        self.setFrameRateMeter(False)

        self.accept("escape", sys.exit)
        for key in TOOL_KEYS:
            self.accept(key, self.set_tool, [key])

        self.key_map = {"w": False, "s": False, "a": False, "d": False, "shift": False}
        for key in self.key_map:
            self.accept(key, self.set_key, [key, True])
            self.accept(f"{key}-up", self.set_key, [key, False])

        self.player_pos = Vec3(0, 0, 1.6)
        self.player_np = self.render.attachNewNode("player")
        self.player_np.setPos(self.player_pos)
        self.heading = 0.0
        self.pitch = 0.0
        self.stamina = 1.0
        self.sanity = 1.0
        self.tool_index = 0

        self.ghost_pos = Vec3(
            random.uniform(-WORLD_SIZE / 2, WORLD_SIZE / 2),
            random.uniform(-WORLD_SIZE / 2, WORLD_SIZE / 2),
            0,
        )

        self.rooms = self.build_rooms()
        self.build_world()
        self.build_lights()
        self.build_ui()
        self.build_collisions()
        self.center_mouse()

        self.taskMgr.add(self.update, "update")

    def build_rooms(self):
        rows, cols = ROOM_GRID
        rooms = []
        start_x = -((cols - 1) * ROOM_SIZE) / 2
        start_y = -((rows - 1) * ROOM_SIZE) / 2
        for r in range(rows):
            for c in range(cols):
                cx = start_x + c * ROOM_SIZE
                cy = start_y + r * ROOM_SIZE
                rooms.append({"center": Vec3(cx, cy, 0), "doors": {}})

        # Simple fixed door layout between adjacent rooms
        for idx, room in enumerate(rooms):
            r = idx // cols
            c = idx % cols
            if c < cols - 1:
                room["doors"]["east"] = True
            if c > 0:
                room["doors"]["west"] = True
            if r < rows - 1:
                room["doors"]["north"] = True
            if r > 0:
                room["doors"]["south"] = True
        return rooms

    def build_world(self):
        self.scene = self.loader.loadModel("models/environment")
        if self.scene:
            self.scene.reparentTo(self.render)
            self.scene.setScale(0.08)
            self.scene.setPos(0, 8, -2)

        # Simple floor card (no external model dependency)
        cm = CardMaker("floor")
        half = WORLD_SIZE / 2
        cm.setFrame(-half, half, -half, half)
        self.floor = self.render.attachNewNode(cm.generate())
        self.floor.setPos(0, 0, -2)
        self.floor.setHpr(0, -90, 0)
        self.floor.setColor(0.08, 0.08, 0.1, 1)

        self.build_room_geometry()

    def build_room_geometry(self):
        half = ROOM_SIZE / 2
        for room in self.rooms:
            cx, cy = room["center"].x, room["center"].y
            doors = room["doors"]

            # North wall
            self.add_wall(
                cx, cy + half, length=ROOM_SIZE, horizontal=True, gap=doors.get("north")
            )
            # South wall
            self.add_wall(
                cx, cy - half, length=ROOM_SIZE, horizontal=True, gap=doors.get("south")
            )
            # East wall
            self.add_wall(
                cx + half, cy, length=ROOM_SIZE, horizontal=False, gap=doors.get("east")
            )
            # West wall
            self.add_wall(
                cx - half, cy, length=ROOM_SIZE, horizontal=False, gap=doors.get("west")
            )

    def add_wall(self, x, y, length, horizontal=True, gap=False):
        # Build wall from two segments if there is a door gap
        door_width = 4.0
        half = length / 2
        segments = [(-half, -door_width / 2), (door_width / 2, half)] if gap else [(-half, half)]

        for a, b in segments:
            cm = CardMaker("wall")
            cm.setFrame(a, b, 0, WALL_HEIGHT)
            wall = self.render.attachNewNode(cm.generate())
            if horizontal:
                wall.setPos(x, y, -2)
                wall.setHpr(0, 0, 0)
            else:
                wall.setPos(x, y, -2)
                wall.setHpr(90, 0, 0)
            wall.setColor(0.12, 0.12, 0.14, 1)
            self.add_wall_collider(wall)

    def add_wall_collider(self, wall_np):
        # Add a collision box matching the wall card bounds
        min_bound, max_bound = wall_np.getTightBounds()
        center = (min_bound + max_bound) * 0.5
        extents = (max_bound - min_bound) * 0.5
        cnode = CollisionNode("wall")
        cnode.addSolid(CollisionBox(center, extents.x, extents.y, extents.z))
        cnode.setFromCollideMask(BitMask32.allOff())
        cnode.setIntoCollideMask(BitMask32.bit(1))
        cnp = wall_np.attachNewNode(cnode)
        cnp.setCollideMask(BitMask32.bit(1))

    def build_collisions(self):
        self.c_trav = CollisionTraverser("player")
        self.c_handler = CollisionHandlerPusher()
        self.c_handler.setHorizontal(True)

        cs = CollisionSphere(0, 0, 0.6, 0.5)
        cnode = CollisionNode("player")
        cnode.addSolid(cs)
        cnode.setFromCollideMask(BitMask32.bit(1))
        cnode.setIntoCollideMask(BitMask32.allOff())
        cnp = self.player_np.attachNewNode(cnode)

        self.c_trav.addCollider(cnp, self.c_handler)
        self.c_handler.addCollider(cnp, self.player_np)

    def build_lights(self):
        ambient = AmbientLight("ambient")
        ambient.setColor((0.15, 0.15, 0.18, 1))
        ambient_np = self.render.attachNewNode(ambient)
        self.render.setLight(ambient_np)

        self.flashlight = Spotlight("flashlight")
        self.flashlight.setColor((1.0, 0.96, 0.8, 1))
        lens = self.flashlight.getLens()
        lens.setFov(45)
        lens.setNearFar(0.1, 35)
        self.flashlight_np = self.camera.attachNewNode(self.flashlight)
        self.flashlight_np.setPos(0, 0.2, 0)
        self.render.setLight(self.flashlight_np)

    def build_ui(self):
        self.ui_tool = OnscreenText(
            text="Tool: EMF",
            pos=(-1.25, 0.9),
            scale=0.06,
            fg=(0.85, 0.9, 0.85, 1),
            align=TextNode.ALeft,
        )
        self.ui_readout = OnscreenText(
            text="Reading: --",
            pos=(-1.25, 0.82),
            scale=0.06,
            fg=(0.9, 0.9, 0.7, 1),
            align=TextNode.ALeft,
        )
        self.ui_sanity = OnscreenText(
            text="Sanity: 100%",
            pos=(-1.25, 0.74),
            scale=0.06,
            fg=(0.7, 0.9, 1, 1),
            align=TextNode.ALeft,
        )
        self.ui_hint = OnscreenText(
            text="WASD Move  |  Shift Sprint  |  1-3 Tools",
            pos=(-1.25, -0.92),
            scale=0.05,
            fg=(0.6, 0.6, 0.6, 1),
            align=TextNode.ALeft,
        )

    def set_tool(self, key):
        self.tool_index = TOOL_KEYS.index(key)
        self.ui_tool.setText(f"Tool: {TOOL_NAMES[self.tool_index]}")

    def set_key(self, key, value):
        self.key_map[key] = value

    def center_mouse(self):
        props = self.win.getProperties()
        self.win.movePointer(0, props.getXSize() // 2, props.getYSize() // 2)

    def update(self, task):
        dt = globalClock.getDt()
        self.update_mouse()
        self.update_movement(dt)
        self.update_readouts(dt)
        return task.cont

    def update_mouse(self):
        if not self.mouseWatcherNode.hasMouse():
            return
        md = self.win.getPointer(0)
        props = self.win.getProperties()
        cx = props.getXSize() / 2
        cy = props.getYSize() / 2
        dx = md.getX() - cx
        dy = md.getY() - cy
        self.heading -= dx * MOUSE_SENS
        self.pitch = clamp(self.pitch - dy * MOUSE_SENS, -70, 70)
        self.camera.setHpr(self.heading, self.pitch, 0)
        self.win.movePointer(0, int(cx), int(cy))

    def update_movement(self, dt):
        direction = Vec3(0, 0, 0)
        if self.key_map["w"]:
            direction.y += 1
        if self.key_map["s"]:
            direction.y -= 1
        if self.key_map["a"]:
            direction.x -= 1
        if self.key_map["d"]:
            direction.x += 1

        if direction.length() > 0:
            direction.normalize()

        speed = PLAYER_SPEED
        if self.key_map["shift"] and self.stamina > 0.05:
            speed *= SPRINT_MULT
            self.stamina -= dt * 0.35
        else:
            self.stamina += dt * 0.2
        self.stamina = clamp(self.stamina, 0.0, 1.0)

        heading_rad = math.radians(self.heading)
        forward = Vec3(math.sin(heading_rad), math.cos(heading_rad), 0)
        right = Vec3(forward.y, -forward.x, 0)
        move = (forward * direction.y + right * direction.x) * speed * dt
        self.player_pos += move
        self.player_pos.x = clamp(self.player_pos.x, -WORLD_SIZE / 2, WORLD_SIZE / 2)
        self.player_pos.y = clamp(self.player_pos.y, -WORLD_SIZE / 2, WORLD_SIZE / 2)
        self.player_np.setPos(self.player_pos)
        self.c_trav.traverse(self.render)
        self.player_pos = self.player_np.getPos()
        self.camera.setPos(self.player_pos)

    def update_readouts(self, dt):
        dist = (self.player_pos - self.ghost_pos).length()
        proximity = clamp(1.0 - (dist / 20.0), 0.0, 1.0)

        if self.tool_index == 0:
            emf = 1 + int(proximity * 4 + random.uniform(0, 0.7))
            reading = f"{emf} EMF"
        elif self.tool_index == 1:
            if proximity > 0.6 and random.random() < 0.08:
                reading = random.choice(["...behind you", "leave", "here"])
            else:
                reading = "static..."
        else:
            temp = 18 - int(proximity * 12 + random.uniform(0, 2))
            reading = f"{temp} C"

        self.ui_readout.setText(f"Reading: {reading}")

        self.sanity -= dt * (0.01 + proximity * 0.04)
        self.sanity = clamp(self.sanity, 0.0, 1.0)
        self.ui_sanity.setText(f"Sanity: {int(self.sanity * 100)}%")

        if random.random() < 0.002:
            self.ghost_pos = Vec3(
                random.uniform(-WORLD_SIZE / 2, WORLD_SIZE / 2),
                random.uniform(-WORLD_SIZE / 2, WORLD_SIZE / 2),
                0,
            )


def main():
    game = HorrorGame()
    game.run()


if __name__ == "__main__":
    main()
