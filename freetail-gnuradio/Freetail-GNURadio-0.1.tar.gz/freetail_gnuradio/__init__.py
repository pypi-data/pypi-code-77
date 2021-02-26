import os.path as osp

with open(osp.join(osp.dirname(osp.dirname(__file__)), 'VERSION')) as version_file:
    __version__ = version_file.read().strip()


def install_gr_blocks():
    """Installs Freetail blocks into GNU Radio Companion's path

    Note: This will overwrite any existing configuration of local_blocks_path
    """
    import configparser
    import os.path as osp
    from gnuradio import gr

    config_filename = osp.join(gr.userconf_path(), "config.conf")

    config = configparser.ConfigParser()
    config.read(config_filename)

    if 'grc' not in config:
        config['grc'] = {}

    local_blocks_path = osp.join(osp.dirname(osp.dirname(osp.abspath(__file__))), 'grc')

    config['grc']['local_blocks_path'] = local_blocks_path
    with open(config_filename, 'w') as config_file:
        config.write(config_file)

