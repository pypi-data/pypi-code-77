#!/usr/bin/env python
# coding: utf-8

# PEP0440 compatible formatted version, see:
# https://www.python.org/dev/peps/pep-0440/
#
# Generic release markers:
# X.Y
# X.Y.Z # For bugfix releases  
# 
# Admissible pre-release markers:
# X.YaN # Alpha release
# X.YbN # Beta release         
# X.YrcN # Release Candidate   
# X.Y # Final release
#
# Dev branch marker is: 'X.Y.dev' or 'X.Y.devN' where N is an integer.
# 'X.Y.dev0' is the canonical version of 'X.Y.dev'
__version__ = '1.0.1.dev0'

def get_version():
    """Returns the version ID of the library."""
    return __version__


import sys, subprocess

def is_colab():
    return "google.colab" in sys.modules

# C.f. https://github.com/openai/gym#installing-everything

# apt install xvfb x11-utils swig
debian_requirements = [
    "xvfb",
    "x11-utils",
    "swig"               # Required for Box2D
]

# pip install gym[box2d] numpy pandas seaborn pyvirtualdisplay imageio nnfigs
pip_requirements = [
    "gym[box2d]",
    #"numpy",            # Already installed on Google Colab
    #"pandas",           # Already installed on Google Colab
    #"seaborn",          # Already installed on Google Colab
    "pyvirtualdisplay",
    "cma",
    #"imageio",          # Already installed on Google Colab
    "nnfigs"
]

if is_colab():

    def run_subprocess_command(cmd):
        # run the command
        process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        # print the output
        for line in process.stdout:
            print(line.decode().strip())

    for i in pip_requirements:
        run_subprocess_command("pip install " + i)

    for i in debian_requirements:
        run_subprocess_command("apt install " + i)


# Setup virtual display for Google colab

if "google.colab" in sys.modules:
    import pyvirtualdisplay

    _display = pyvirtualdisplay.Display(visible=False,  # use False with Xvfb
                                        size=(1400, 900))
    _ = _display.start()


import numpy as np
import time

import imageio     # To render episodes in GIF images (otherwise there would be no render on Google Colab)
                   # C.f. https://stable-baselines.readthedocs.io/en/master/guide/examples.html#bonus-make-a-gif-of-a-trained-agent

# To display GIF images in the notebook

import IPython
from IPython.display import Image

class RenderWrapper:
    def __init__(self, env, force_gif=False):
        self.env = env
        self.force_gif = force_gif
        self.reset()

    def reset(self):
        self.images = []

    def render(self):
        if not is_colab():
            self.env.render()
            time.sleep(1./60.)

        if is_colab() or self.force_gif:
            img = self.env.render(mode='rgb_array')
            self.images.append(img)

    def make_gif(self, filename="render"):
        if is_colab() or self.force_gif:
            imageio.mimsave(filename + '.gif', [np.array(img) for i, img in enumerate(self.images) if i%2 == 0], fps=29)
            return Image(open(filename + '.gif','rb').read())

    @classmethod
    def register(cls, env, force_gif=False):
        env.render_wrapper = cls(env, force_gif=True)
