"""
Main script for In Container

© Zigfrid Zvezdin — 2021
"""

from os.path import exists, isfile

def in_container():
    """
    Returns if you currently are in a Docker container
    """
    c_group_docker = False
    if isfile('/proc/self/cgroup'):
        with open('/proc/self/cgroup') as c_group:
            c_group_docker = "docker" in c_group.read()
    return exists('/.dockerenv') or c_group_docker
    