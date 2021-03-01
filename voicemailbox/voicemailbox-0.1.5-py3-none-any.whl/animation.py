from kivy import animation as kv_animation


class Animation:
    """
    Class gathering all transition methods
    """
    @staticmethod
    def background_fade(widget, background_color):
        """
        Background fading
        """
        fade = kv_animation.Animation(background_rgba=background_color,
                                      duration=1,
                                      t="in_back")
        return fade

    @staticmethod
    def fade_out_in(widget, attr_name, attr_value, **kwargs):
        """
        Widget fading out, widget attribute change and widget fading in
        """
        def update_during_transition(_widget, _attr_name, _attr_value):
            setattr(_widget, _attr_name, _attr_value)
            fade_in = kv_animation.Animation(opacity=1,
                                             duration=0.5,
                                             t="in_back")
            fade_in.start(widget)

        fade_out = kv_animation.Animation(opacity=0, duration=0.5, t="in_back")
        fade_out.bind(
            on_complete=lambda *args: update_during_transition(widget,
                                                               attr_name,
                                                               attr_value))
        return fade_out

    @staticmethod
    def fade_in(widget):
        """
        Widget fading in
        """
        def enable(_widget):
            _widget.disabled = False

        fade_in = kv_animation.Animation(opacity=1, duration=1, t="in_back")
        fade_in.bind(on_start=lambda *args: enable(widget))
        return fade_in

    @staticmethod
    def fade_out(widget):
        """
        Widget fading out
        """
        def disable(_widget):
            _widget.disabled = True

        fade_out = kv_animation.Animation(opacity=0, duration=1, t="in_back")
        fade_out.bind(on_complete=lambda *args: disable(widget))
        return fade_out
