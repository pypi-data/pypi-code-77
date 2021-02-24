import datetime

import kivy.uix.screenmanager as kv_screenmanager
import kivy.properties as kv_properties
import kivy.uix.button as kv_button
import kivy.uix.slider as kv_slider
import kivy.clock as kv_clock
import kivy.core.audio as kv_audio

from voicemailbox import logger
from voicemailbox import NEW_MAIL_SONG_PATH
from voicemailbox import voicemail
from voicemailbox import player
from voicemailbox import animation as vmb_animation
from voicemailbox import backlight


class RootScreen(kv_screenmanager.ScreenManager):

    SLEEP_DELAY = 30

    new_voicemails = kv_properties.ListProperty([-1])

    voicemails_volume = (
        kv_properties.BoundedNumericProperty(0.5, min=0.0, max=1.0))
    new_mail_song_volume = (
        kv_properties.BoundedNumericProperty(1.0, min=0.0, max=1.0))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.vm_manager = voicemail.VoicemailManager()
        self.vm_player = player.Player(volume=self.voicemails_volume)
        self.voicemails_to_play = list()

        # Set brightness to 1 at startup
        self.backlight = backlight.Backlight()
        self.backlight.power = True
        self.backlight.brightness = 100

        self.after_slider_move = ""

        self.ring_song = None
        self.nb_new_voicemails = 0

        # Create sleep and ring events
        self.sleep_event = None
        self.ring_event = None

        # Bind events to callbacks
        self.home_screen \
            .voicemails_button.bind(on_release=self.play_next_voicemail)

        # Loop to bind callbacks to the 2 voice_mail_screen events
        for vms in (self.voicemail_screen_1, self.voicemail_screen_2,):
            vms_slider = vms.voicemail_slider
            vms.play_button.bind(on_release=self.toggle_play_pause)
            vms_slider.bind(is_moving=self.slider_move)

        self.update_new_voicemails()

    def slider_move(self, slider, is_moving):
        """
        If slider is touching down, song is stopped (if necessary)
        after_slider_move attribute is modified
        to adapt performed action when the slider move ends
        (play only if song was playing before the slider move)
        """
        if is_moving:
            if self.vm_player.state == "play":
                self.pause()
                self.after_slider_move = "play"
            else:
                self.after_slider_move = "stop"

        else:
            self.vm_player.position = slider.value
            if self.after_slider_move == "play":
                self.play()

    def update_new_voicemails(self, *args):
        """
        Update list of unread voicemails
        """
        self.new_voicemails = self.vm_manager.new_voicemails

    def update_position(self, vms, *args):
        """
        Update position property according to song position
        only if song is currently playing
        """
        if (self.vm_player.song is not None
                and vms.voicemail_slider.is_moving is False):
            vms.position = self.vm_player.position

    def update_play_button(self, *args, **kwargs):
        self.crt_screen.state = "\uf04c" if (
                self.vm_player.state == "play") else "\uf04b"

    def on_new_voicemails(self, instance, new_voicemails):
        """
        New voicemails list event callback
        Update home screen head label, button and background
        """

        # Check if new voicemails arrived and update new voicemails number
        new_voicemail_arrived = len(new_voicemails) > self.nb_new_voicemails
        self.nb_new_voicemails = len(new_voicemails)

        # These functions return tuples (animation_object, widget)
        # allowing to start animations at the same time
        # animation is enabled if current screen is home screen

        animation = (True if self.current_screen == self.home_screen
                     else False)

        # first item of each tuple is animation_object
        # set to None if animation is disabled
        hl_tuple = self.home_screen \
            .update_head_label(len(new_voicemails), animation=animation)
        btn_tuple = self.home_screen \
            .update_voicemails_button(len(new_voicemails), animation=animation)
        back_tuple = self.home_screen \
            .update_background(len(new_voicemails), animation=animation)

        # Loop for starting animations (if enable)
        for t in (hl_tuple, btn_tuple, back_tuple):
            if t[0] is not None:
                t[0].start(t[1])

        # Wake the backlight up when new voicemails are arriving
        # And ring to alert of these new voicemails
        if new_voicemail_arrived:

            if self.current_screen == self.home_screen:
                self.wake_up()
                self.activate_sleeping()

            self.ring()

    def play_next_voicemail(self, *args):

        if args and isinstance(args[0], kv_button.Button):
            self.voicemails_to_play = self.new_voicemails[:]

        voicemail = self.voicemails_to_play[0]

        # Init VmPlayer and load voicemail
        self.vm_player.load(voicemail)
        self.vm_player.bind(on_play=self.update_play_button)
        self.vm_player.bind(on_stop=self.manage_mail_stop)

        # Update voicemail screen information
        self.next_voicemail_screen.voicemail = voicemail
        self.next_voicemail_screen.duration = self.vm_player.duration

        # Display voicemail_screen and play voicemail
        self.crt_screen = self.next_voicemail_screen
        self.vm_player.play()
        logger.info(f"Volume VmPlayer : {self.vm_player.song.volume}")

    def toggle_play_pause(self, *args):
        self.vm_player.toggle_play_pause()

    def pause(self, *args):
        self.vm_player.pause()

    def play(self, *args):
        self.vm_player.play()

    def manage_mail_stop(self, *args, **kwargs):
        # Update play button and go to next screen if mail is ended
        self.update_play_button()
        if kwargs.get("end", False):
            self.to_next_screen()

    def to_next_screen(self):

        # check if current screen is a voicemail_screen (1 or 2)
        # if it is, unload voicemail, update voicemails_to_play list,
        # marks current mail as read and update new_voicemails list
        # (for home screen to be up to date)
        if self.crt_screen in (self.voicemail_screen_1,
                               self.voicemail_screen_2):

            self.vm_player.unload()
            self.voicemails_to_play.remove(self.crt_screen.voicemail)
            self.crt_screen.voicemail.read = True
            self.new_voicemails = self.vm_manager.new_voicemails

            if self.voicemails_to_play:
                self.play_next_voicemail()
            else:
                self.crt_screen = self.home_screen

    def sleep(self, *args):
        if self.current_screen == self.home_screen:
            with self.backlight.fade(duration=1):
                self.backlight.brightness = 0
            self.backlight.power = False

    def wake_up(self):
        self.backlight.power = True
        with self.backlight.fade(duration=1):
            self.backlight.brightness = 100

    def deactivate_sleeping(self):
        if getattr(self, "sleep_event", None) is not None:
            self.sleep_event.cancel()
            logger.info("deactivate sleeping !")
        else:
            logger.info("cannot deactivate, sleep_event is None")

    def activate_sleeping(self):
        self.deactivate_sleeping()
        self.sleep_event = kv_clock.Clock.schedule_once(self.sleep,
                                                        self.SLEEP_DELAY)
        logger.info("activate sleeping !")

    def ring(self, *args):
        logger.info("RING !")
        if getattr(self, "ring_event", None) is not None:
            logger.info("ring_event is not None")
            self.ring_event.cancel()

        # Load new mail song
        self.ring_song = kv_audio.SoundLoader.load(str(NEW_MAIL_SONG_PATH))
        self.ring_song.volume = self.new_mail_song_volume
        self.ring_song.bind(on_stop=lambda x: self.ring_song.unload())

        # Ring only on home screen and if there are still new voicemails
        if self.current_screen == self.home_screen and self.new_voicemails:
            self.ring_song.seek(0)
            self.ring_song.play()

        # If there are still new voicemails, schedule a new ring
        # a minute later
        if self.new_voicemails:
            self.ring_event = kv_clock.Clock.schedule_once(self.ring, 60)

    def on_touch_up(self, touch):
        do_not_propagate = False
        if not self.backlight.power:
            self.wake_up()
            do_not_propagate = True

        if self.current_screen == self.home_screen:
            self.activate_sleeping()

        return do_not_propagate

    @property
    def crt_screen(self):
        return getattr(self, self.current, None)

    @crt_screen.setter
    def crt_screen(self, screen):
        if screen == self.home_screen:
            self.current = "home_screen"
        elif screen == self.voicemail_screen_1:
            self.current = "voicemail_screen_1"
        elif screen == self.voicemail_screen_2:
            self.current = "voicemail_screen_2"
        else:
            raise ValueError("unknown screen")

    @property
    def next_voicemail_screen(self):
        if self.crt_screen == self.home_screen:
            return self.voicemail_screen_1
        elif self.crt_screen == self.voicemail_screen_1:
            return self.voicemail_screen_2
        elif self.crt_screen == self.voicemail_screen_2:
            return self.voicemail_screen_1
        else:
            return None

class HomeScreen(kv_screenmanager.Screen):
    background_rgba = kv_properties.ListProperty([0 / 255,
                                                  0 / 255,
                                                  0 / 255, 1]
                                                 )
    head_label = kv_properties.ObjectProperty(None)
    home_screen_background = kv_properties.ObjectProperty(None)

    current_date = kv_properties.StringProperty("")
    current_time = kv_properties.StringProperty("")

    def on_enter(self):
        root_screen = self.parent
        root_screen.activate_sleeping()

    def update_background(self, nb_new_voicemails, animation=True):
        """
        Background transition
        (no voicemail : blue/green ; new voicemails : red)
        :param nb_new_voicemails: int
        :param animation: bool
        :return: (VMAnimation object, widget)
        """
        background_color = None

        if nb_new_voicemails:
            background_color = (217 / 255, 33 / 255, 33 / 255, 1)
        else:
            background_color = (1 / 255, 120 / 255, 111 / 255, 1)

        if background_color != self.background_rgba:
            if animation:
                return (vmb_animation.Animation.background_fade(
                    self, background_color),
                        self,
                        )
            else:
                self.background_rgba = background_color
                return None, self

    def update_head_label(self, nb_new_voicemails, animation=True):
        """
        Head label transition (Pas de nouveau message ; X nouveaux messages)
        :param nb_new_voicemails: int
        :param animation: bool
        :return: (VMAnimation object, widget)
        """
        if nb_new_voicemails > 1:
            head_label = f"{nb_new_voicemails} nouveaux messages"
        elif nb_new_voicemails == 1:
            head_label = f"{nb_new_voicemails} nouveau message"
        else:
            head_label = f"Pas de nouveau message"

        if animation:
            return (vmb_animation.Animation.fade_out_in(self.head_label,
                                                        "text",
                                                        head_label),
                    self.head_label
                    )
        else:
            self.head_label.text = head_label
            return None, self.head_label

    def update_voicemails_button(self, nb_new_voicemails, animation=True):
        """
        Home screen button transition
        (no voicemail : no button ; new voicemails : button)
        :param nb_new_voicemails: int
        :param animation: bool
        :return: (VMAnimation object, widget)
        """
        if nb_new_voicemails:
            if animation:
                return (vmb_animation.Animation.fade_in(
                    self.voicemails_button),
                        self.voicemails_button)
            else:
                self.voicemails_button.disabled = False
                self.voicemails_button.opacity = 1
                return None, self.voicemails_button
        else:
            if animation:
                return (vmb_animation.Animation.fade_out(
                    self.voicemails_button),
                        self.voicemails_button)
            else:
                self.voicemails_button.disabled = True
                self.voicemails_button.opacity = 0
                return None, self.voicemails_button

    def update_datetime(self, *args):

        dt = datetime.datetime.now()

        self.current_date = dt.strftime("%A %d %B %Y")
        self.current_time = dt.strftime("%Hh%M")


class VoicemailScreenCore(kv_screenmanager.Screen):
    voicemail = kv_properties.ObjectProperty(None, allownone=True)

    position = kv_properties.NumericProperty(0)
    duration = kv_properties.NumericProperty(0)
    state = kv_properties.StringProperty("\uf04c")
    date = kv_properties.StringProperty("")
    time = kv_properties.StringProperty("")
    numero = kv_properties.StringProperty("")
    label = kv_properties.StringProperty("")

    def __init__(self, **kwargs):
        super(VoicemailScreenCore, self).__init__(**kwargs)

    def on_enter(self):
        logger.info(f"Enter Voicemail screen, parent : {self.parent}")
        root_screen = self.parent
        root_screen.deactivate_sleeping()

    def on_voicemail(self, instance, voicemail):
        self.date = voicemail.pretty_date
        self.time = voicemail.pretty_time
        self.numero = voicemail.pretty_numero

        self.label = f"Message reçu\n" \
                     f"[b]{self.date}[/b] à [b]{self.time}[/b]\n" \
                     f"{'du ' if not self.numero[0] == 'n' else ''}" \
                     f"[b]{self.numero}[/b]"


class VoicemailScreen1(VoicemailScreenCore):
    pass


class VoicemailScreen2(VoicemailScreenCore):
    pass


class VoicemailSlider(kv_slider.Slider):
    """
    Slider shown in voicemail screen
    """

    is_moving = kv_properties.BooleanProperty(False)

    def on_touch_down(self, touch):
        """
        When slider is touched down,
        is_moving set to True
        """

        if self.collide_point(*touch.pos):
            self.is_moving = True
            touch.grab(self)

        super().on_touch_down(touch)

    def on_touch_up(self, touch):
        """
        When slider is touched up,
        is_moving set to False
        """

        if touch.grab_current is self and self.is_moving:
            self.is_moving = False
            touch.ungrab(self)
            return True

        else:
            super().on_touch_up(touch)
