from zumi.zumi import Zumi
from screen import Screen
from zumi.protocol import Note
from time import sleep
from threading import Thread
from socket import gethostname


class Personality:
    def __init__(self, _zumi, _screen):
        self.check_break = False
        self.movement = Movement(_zumi)
        self.screen = _screen
        self.sound = Sound(_zumi)

    def _start_threading(self, *args):
        for thread in args:
            thread.start()
        for thread in args:
            thread.join()
            
    def reading(self, img):
        sound_thread = Thread(target=self.sound.calibrating)
        screen_thread = Thread(target=self.screen.draw_image, args=(img,))
        self._start_threading(screen_thread, sound_thread)
        
    def celebrate(self):
        screen_thread = Thread(target=self.screen.happy)
        sound_thread = Thread(target=self.sound.celebrate)
        move_thread = Thread(target=self.movement.celebrate)
        self._start_threading(screen_thread, sound_thread, move_thread)

    def look_around_open01(self):
        sound_thread = Thread(target=self.sound.look_around01)
        screen_thread = Thread(target=self.screen.look_around_open01)
        self._start_threading(sound_thread, screen_thread)

    def look_around_open02(self):
        sound_thread = Thread(target=self.sound.look_around02)
        screen_thread = Thread(target=self.screen.look_around_open02)
        self._start_threading(sound_thread, screen_thread)

    def look_around_open03(self):
        sound_thread = Thread(target=self.sound.look_around03)
        screen_thread = Thread(target=self.screen.look_around_open03)
        self._start_threading(sound_thread, screen_thread)

    def look_around_open04(self):
        sound_thread = Thread(target=self.sound.look_around04)
        screen_thread = Thread(target=self.screen.look_around_open04)
        self._start_threading(sound_thread, screen_thread)



class Movement:
    def __init__(self, _zumi):
        self.zumi = _zumi

    def celebrate(self):
        sleep(0.5)
        angle = self.zumi.read_z_angle()
        self.zumi.turn(angle+360, 3)


class Sound:
    def __init__(self, _zumi):
        self.zumi = _zumi

    def blink(self):
        self.zumi.play_note(49, 20)
        self.zumi.play_note(50, 20)
        self.zumi.play_note(51, 20)


    def look_around01(self):
        sleep(1.5)
        self.blink()
        
    def look_around02(self):
        sleep(1.1)
        self.blink()
        
    def look_around03(self):
        sleep(.7)

    def look_around04(self):
        sleep(0.4)
        self.blink()

    def celebrate(self):
        sleep(.25)
        self.zumi.play_note(48, 100)
        sleep(.005)
        self.zumi.play_note(52, 100)
        sleep(.005)
        self.zumi.play_note(55, 100)
        sleep(.005)
        self.zumi.play_note(55, 100)
        sleep(.20)
        self.zumi.play_note(52, 125)
        sleep(.005)
        self.zumi.play_note(55, 125)

    def calibrating(self):
        for i in range(1):
            tempo = 75
            self.zumi.play_note(Note.G5, tempo)
            sleep(0.1)
            self.zumi.play_note(Note.G5, tempo)
            sleep(0.1)
            self.zumi.play_note(Note.D6, tempo)
            sleep(0.1)
            self.zumi.play_note(Note.D6, tempo)
            sleep(0.2)
