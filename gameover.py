import cocos
from cocos.sprite import Sprite
from cocos.director import director
class Gameover(cocos.layer.Layer):
    def __init__(self,game):
        super().__init__()
        self.game = game
        self.spr= Sprite("nc.jpg")
        self.text = cocos.text.Label(u"Died...QQ    Cross: %d block"% self.game.score,
                                font_name="Times New Roman",
                                font_size=32,
                                anchor_x="center",
                                anchor_y="center")
        self.text.position= 400,50
        self.spr.position = 400 ,310
        self.add(self.spr)
        self.add(self.text)