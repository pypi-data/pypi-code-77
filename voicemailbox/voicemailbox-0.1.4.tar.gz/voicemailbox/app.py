from kivy import app as kv_app
from kivy import clock as kv_clock

from voicemailbox import screens


class VoicemailBoxApp(kv_app.App):

    def build(self):
        root_screen = screens.RootScreen()

        # Loop to update position of song every 5 ms
        kv_clock.Clock.schedule_interval(
            callback=lambda x: root_screen.update_position(
                root_screen.voicemail_screen_1),
            timeout=0.05,
        )
        kv_clock.Clock.schedule_interval(
            callback=lambda x: root_screen.update_position(
                root_screen.voicemail_screen_2),
            timeout=0.05,
        )

        # Loop to update new voicemails list every second
        kv_clock.Clock.schedule_interval(
            callback=root_screen.update_new_voicemails,
            timeout=1,
            )

        # Loop to update date and time every second
        kv_clock.Clock.schedule_interval(
            callback=root_screen.home_screen.update_datetime,
            timeout=1,
        )

        return root_screen
