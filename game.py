import cocos
from cocos.sprite import Sprite
from cocos.director import director
from pyaudio import PyAudio, paInt16
import struct
from nezuko import Nezuko
from block import Block
from gameover import Gameover

class VoiceGame(cocos.layer.ColorLayer):
    is_event_handler = True

    def __init__(self):
        super().__init__(255, 255, 150, 255, 800, 600)
        # self.gameover = None
        self.score = 0
        self.txt_score = cocos.text.Label(u"Cross: 0 block",
                                          font_name="SimSun",
                                          font_size=14,
                                          color=(0, 0, 0, 255))
        self.txt_score.position = 600, 570
        self.add(self.txt_score)

        self.NUM_SAMPLES = 2048 
        self.LEVEL = 1500

        self.voicebar = Sprite('p.png')
        self.voicebar.position = 20, 570
        self.voicebar.scale_y = 0.1
        self.voicebar.image_anchor = 0, 0
        self.add(self.voicebar)

        self.nezuko = Nezuko(self)
        self.add(self.nezuko)

        self.floor = cocos.cocosnode.CocosNode()
        self.add(self.floor)
        self.last_block = 0, 100
        for i in range(5):
            b = Block(self)
            self.floor.add(b)
            pos = b.x + b.width, b.height

        pa = PyAudio()
        SAMPLING_RATE = int(pa.get_device_info_by_index(0)['defaultSampleRate'])
        self.stream = pa.open(format=paInt16, channels=1, rate=SAMPLING_RATE, input=True, frames_per_buffer=self.NUM_SAMPLES)
        self.stream.stop_stream()

        # self.schedule(self.update)
        self.schedule(self.update)

    def collide(self):
        px = self.nezuko.x - self.floor.x
        for b in self.floor.get_children():
            if b.x <= px + self.nezuko.width * 0.8 and px + self.nezuko.width * 0.2 <= b.x + b.width:
                if self.nezuko.y < b.height:
                    self.nezuko.land(b.height)
                    break

    def update(self, dt):
        if self.stream.is_stopped():
            self.stream.start_stream()
        string_audio_data = self.stream.read(self.NUM_SAMPLES)
        k = max(struct.unpack('2048h', string_audio_data))

        self.voicebar.scale_x = k / 10000.0
        if k > 3000:
            # if not self.nezuko.dead:
                self.floor.x -= min((k / 20.0), 150) * dt
        if k > 8000:
            self.nezuko.jump((k - 8000) / 25.0)
        self.floor.x -= self.nezuko.velocity * dt
        self.collide()

    def endGame(self):
        self.stream.stop_stream()
        self.pause_scheduler()
        director.replace(cocos.scene.Scene(Gameover(self)))

    def add_score(self):
        self.score += 1
        self.txt_score.element.text = u'Cross: %d  block' % self.score


if __name__ == '__main__':
    director.init(width=800,height=600, caption="Nezuko Run")
    gamelayer = VoiceGame()

    scence = cocos.scene.Scene()
    scence.add(gamelayer)
    director.run(scence)
