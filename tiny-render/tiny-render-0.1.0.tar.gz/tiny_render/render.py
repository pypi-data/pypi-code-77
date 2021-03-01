# -*- coding: utf-8 -*-

import os

class Render(object):
    def __init__(self, template_dir):
        if not os.path.isdir(template_dir):
            raise ValueError(f"{template_dir} is not a valid directory")

        self._dir = template_dir
