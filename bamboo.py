import cocos

class Bamboo(cocos.sprite.Sprite):
    def __init__(self, block):
        super().__init__('bamboo.png')
        self.game = block.game
        self.nezuko = block.game.nezuko
        self.floor = block.floor
        self.position = block.x + block.width / 2, block.height + 100

        self.schedule(self.update)

    def update(self, dt):
        px = self.nezuko.x + self.nezuko.width / 2 - self.floor.x
        py = self.nezuko.y + self.nezuko.height / 2

        if abs(px - self.x) < 50 and abs(py - self.y) < 50:
            # nezuko get bamboo
            self.parent.remove(self)
            self.nezuko.rush()

    def reset(self):
        self.parent.remove(self)
