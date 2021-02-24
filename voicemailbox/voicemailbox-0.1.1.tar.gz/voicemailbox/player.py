import kivy.core.audio as kv_audio
import kivy.event as kv_event


class Player(kv_event.EventDispatcher):
    """
    Manager for playing voicemails
    """
    def __init__(self, volume=1.0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register_event_type('on_play')
        self.register_event_type('on_stop')
        self.source = None
        self.song = None
        self.duration = None
        self._position = None
        self.manual_paused = False
        self.volume = volume

    def load(self, voicemail):
        self.source = voicemail.source
        self.song = kv_audio.SoundLoader.load(str(self.source))
        self.song.volume = self.volume
        self.duration = self.song.length
        self.position = 0

        # When song is stopped, automatically save current position
        self.song.bind(on_play=lambda x: self.dispatch("on_play"))
        self.song.bind(on_stop=(
            lambda x: self.dispatch("on_stop", end=not self.manual_paused)))

    def save_position(self, *args):
        self.position = self.song.get_pos() if self.song else 0

    def play(self):
        self.manual_paused = False
        self.song.seek(self.position)
        self.song.play()

    def pause(self):
        self.manual_paused = True
        self.song.stop()

    def toggle_play_pause(self):
        if self.song.state == "play":
            self.pause()
        else:
            self.play()

    def unload(self):
        self.song.unload()
        self.song = None

    def on_stop(self, *args, **kwargs):
        self.save_position()

    def on_play(self, *args):
        pass

    @property
    def position(self):
        if self.song is None:
            return None
        elif self.song.state == "play":
            return self.song.get_pos()
        else:
            return self._position

    @position.setter
    def position(self, new_position):
        self._position = new_position

    @property
    def state(self):
        if self.song:
            return self.song.state
        else:
            return "stop"
