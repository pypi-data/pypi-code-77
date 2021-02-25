"""iOS splash screen generator"""

import os
from PIL import Image
from assm.devices import APPLE_DEVICES


def make_splash_image(screen_orientation, screen_width, screen_height, logo_path):
    """ Generate splash image """

    # swap screen sizes
    if screen_orientation == 'landscape':
        screen_width, screen_height = screen_height, screen_width

    logo_size = round(screen_width / 5)
    logo_w_pos = round((screen_width / 2) - (logo_size / 2))
    logo_h_pos = round((screen_height / 2) - (logo_size / 2))

    splash_image = Image.new('RGB', (screen_width, screen_height), (255, 255, 255))
    logo_image = Image.open(logo_path)
    app_logo = logo_image.resize((logo_size, logo_size))
    splash_image.paste(app_logo, (logo_w_pos, logo_h_pos), app_logo)

    return splash_image


def main(output_folder='./images/'):
    """Sample main function"""

    # check folder exists
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    # portrait
    print('Generate portrait splash...')

    for device in APPLE_DEVICES:
        device_w = APPLE_DEVICES[device][0]
        device_h = APPLE_DEVICES[device][1]

        file_name = '{f}/splash-portrait-{h}x{w}.png'.format(
            f=output_folder, w=device_w, h=device_h
        )

        splash = make_splash_image('portrait', device_w, device_h, 'logo.png')
        splash.save(file_name)

        print('..splash for {w}x{h} saved...'.format(w=device_w, h=device_h))

    # landscape
    print('Generate landscape splash...')

    for device in APPLE_DEVICES:
        device_w = APPLE_DEVICES[device][0]
        device_h = APPLE_DEVICES[device][1]

        file_name = '{f}/splash-landscape-{h}x{w}.png'.format(
            f=output_folder, w=device_w, h=device_h
        )

        splash = make_splash_image('landscape', device_w, device_h, 'logo.png')
        splash.save(file_name)

        print('...splash for {h}x{w} saved...'.format(w=device_w, h=device_h))


if __name__ == '__main__':
    main()
