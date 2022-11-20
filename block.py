import random
import cocos
from bamboo import Bamboo

class Block(cocos.sprite.Sprite):
    def __init__(self, game):
        super(Block, self).__init__('g.png')
        self.game = game
        self.nezuko = game.nezuko
        self.floor = game.floor
        self.active = True
        self.image_anchor = 0, 0
        self.reset()
        self.schedule(self.update)

    def update(self, dt):
        if self.active and self.x < self.nezuko.x - self.floor.x:
            self.active = False
            self.game.add_score()
        if self.x + self.width + self.game.floor.x < -10:
            self.reset()

    def reset(self):
        x, y = self.game.last_block
        if x == 0:
            self.scale_x = 5
            self.scale_y = 1
            self.position = 0, 0
            self.active = False
        else:
            self.scale_x = 0.75 + random.random()
            self.scale_y = random.uniform(0.3,1)
            self.position = x + random.uniform(100,200), 0
            self.active = True
            # random add Bamboo
            if self.x > 1000 and random.random() > 0.5:
                self.floor.add(Bamboo(self))
        self.game.last_block = self.x + self.width, self.height
