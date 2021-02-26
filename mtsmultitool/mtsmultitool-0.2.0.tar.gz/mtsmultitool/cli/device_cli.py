
import os
import pprint
import argparse
import cbor
import textwrap
import re
import tempfile

from .. import device
from .. import device_serial
from .. import device_types


def key_gen(args):
    sk, vk = device.gen_key_pair()
    priv, pub = device.export_key_pair(sk, args.name, args.dir)
    print(f'Private key written to "{priv}"')
    print(f'Public key written to "{pub}"')


def key_pub(args):
    sk = device.import_key_pem(args.priv_key_file)
    vk = device.pub_key_from_private(sk)

    output_format = 'wb'
    if args.format == 'hex':
        formatted = vk.hex()
        output_format = 'w'
    elif args.format == 'c':
        formatted = '{ ' + ', '.join([f'0x{b:02x}' for b in vk]) + ' }'
        output_format = 'w'
    else:
        formatted = vk

    if args.output is not None:
        with open(args.output, output_format) as fd:
            fd.write(formatted)
        print(f'Public key written to "{args.output}"')
    else:
        print(formatted)


def patch(args):
    dp = None

    if args.manifest or args.bootloader:
        if args.series is None:
            print('Must specify device series.')
            return
        dt = device_types.DeviceSeries[args.series]
        dp = device_types.DeviceProperties(dt)

    with open(args.original, 'rb') as fd:
        original_image = fd.read()

    with open(args.upgrade, 'rb') as fd:
        upgrade_image = fd.read()

    app_offset = 0
    if args.bootloader:
        app_offset = dp.app_offset

    fw_upgrade = device.create_patch(original_image, upgrade_image, app_offset)

    mf = None
    if args.manifest:

        mf = device.generate_manifest(fw_upgrade, args.version, dp, args.description, args.required_version,
                                      args.vendor, args.model, args.vendor_dns)

        if args.sign is not None:
            sk = device.import_key_pem(args.sign)
            mf = device.sign_manifest(sk, mf)

    output_file = args.output
    if output_file is None:
        output_file = os.path.splitext(args.upgrade)[0]
        output_file += '.patch'
    device.combine(output_file, mf, fw_upgrade.image, args.crc, 0)
    print(f'Firmware patch written to "{output_file}"')


def compress(args):
    dp = None

    if args.manifest or args.bootloader:
        if args.series is None:
            print('Must specify device series.')
            return
        dt = device_types.DeviceSeries[args.series]
        dp = device_types.DeviceProperties(dt)

    with open(args.image, 'rb') as fd:
        image = fd.read()

    app_offset = 0
    if args.bootloader:
        app_offset = dp.app_offset

    fw_upgrade = device.compress(image, app_offset)

    mf = None
    if args.manifest:
        mf = device.generate_manifest(fw_upgrade, args.version, dp, args.description, None,
                                      args.vendor, args.model, args.vendor_dns)

        if args.sign is not None:
            sk = device.import_key_pem(args.sign)
            mf = device.sign_manifest(sk, mf)

    output_file = args.output
    if output_file is None:
        output_file = os.path.splitext(args.image)[0]
        output_file += '.lz4'
    device.combine(output_file, mf, fw_upgrade.image, args.crc, 0)
    print(f'Compressed firmware image written to "{output_file}"')


def plain(args):
    dp = None

    if args.manifest or args.bootloader:
        if args.series is None:
            print('Must specify device series.')
            return
        dt = device_types.DeviceSeries[args.series]
        dp = device_types.DeviceProperties(dt)

    with open(args.image, 'rb') as fd:
        image = fd.read()

    app_offset = 0
    if args.bootloader:
        app_offset = dp.app_offset

    fw_upgrade = device.plain(image, app_offset)

    mf = None
    if args.manifest:
        mf = device.generate_manifest(fw_upgrade, args.version, dp, args.description, None,
                                      args.vendor, args.model, args.vendor_dns)

        if args.sign is not None:
            sk = device.import_key_pem(args.sign)
            mf = device.sign_manifest(sk, mf)

    output_file = args.output
    if output_file is None:
        output_file = os.path.splitext(args.image)[0]
        output_file += '.upgrade'
    device.combine(output_file, mf, fw_upgrade.image, args.crc, 0)
    print(f'Upgrade written to "{output_file}"')


def manifest(args):
    dt = device_types.DeviceSeries[args.series]
    dp = device_types.DeviceProperties(dt)

    # TODO: Check for file, print error if it does not exist
    with open(args.image, 'rb') as fd:
        image = fd.read()

    app_offset = 0
    if args.bootloader:
        app_offset = dp.app_offset

    size, digest = device.digest(image, app_offset)
    required_version = None
    if args.patch is not None:
        image_type = device.FirmwareUpgrade.Type.PATCH
        required_version = args.patch
    elif args.compressed:
        image_type = device.FirmwareUpgrade.Type.COMPRESSED
    else:
        image_type = device.FirmwareUpgrade.Type.PLAIN
    fw_upgrade = device.FirmwareUpgrade(image[app_offset:], size, digest, image_type)

    mf = device.generate_manifest(fw_upgrade, args.version, dp, args.description, required_version,
                                  args.vendor, args.model, args.vendor_dns)
    if args.sign is not None:
        sk = device.import_key_pem(args.sign)
        mf = device.sign_manifest(sk, mf)

    if args.apply:
        device.combine(args.image, mf, fw_upgrade.image, False, 0)
        print(f'Manifest applied to "{args.image}"')
    else:
        if args.format == 'text':
            pp = pprint.PrettyPrinter()
            output_mf = pp.pformat(mf)
            output_fmt = 'w'
        else:
            output_mf = device.encode_manifest(mf)
            if args.format == 'hex':
                output_mf = output_mf.hex()
                output_fmt = 'w'
            else:
                output_fmt = 'wb'

        if args.output is not None:
            with open(args.output, output_fmt) as fd:
                fd.write(output_mf)
            print(f'Manifest written to "{args.output}"')
        else:
            print(output_mf)


def verify(args):
    with open(args.image, 'rb') as fd:
        image = fd.read()
    try:
        with open(args.pub_key_file, 'rb') as fd:
            pub_key = fd.read()
        sig_res, dig_res = device.verify_manifest(image, pub_key)
        print('Signature: {0}'.format('SUCCESS' if sig_res else 'FAILED'))
        print('Hash digest: {0}'.format('SUCCESS' if sig_res else 'FAILED'))
    except Exception as ex:
        print(ex)


def combine(args):
    with open(args.image, 'rb') as fd:
        image = fd.read()
    with open(args.manifest, 'rb') as fd:
        mf_enc = fd.read()

    output = args.output
    if output is None:
        output = args.image
    mf = cbor.loads(mf_enc)
    device.combine(output, mf, image, args.crc, args.bootloader)
    print(f'Merged file written to "{output}"')


def crc(args):
    with open(args.image, 'rb') as fd:
        image = fd.read()

    appended = False
    output = args.output
    if output is None:
        output = args.image
        appended = True

    with open(output, 'wb') as fd:
        fd.write(image)
        image_crc = device.calculate_crc(image)
        fd.write(image_crc)
        if appended:
            print(f'CRC ({image_crc.hex()}) appended to "{output}"')
        else:
            print(f'Image with CRC ({image_crc.hex()}) written to "{output}"')


def upgrade(args):
    dt = device_types.DeviceSeries[args.series]
    dp = device_types.DeviceProperties(dt)

    app_offset = 0
    if args.bootloader:
        app_offset = dp.app_offset

    with open(args.image, 'rb') as fd:
        image = fd.read()

    mf = None
    if args.no_processing:
        fw_upgrade = device.plain(image, app_offset)
    else:
        fw_upgrade = device.compress(image, app_offset)
        mf = device.generate_manifest(fw_upgrade, [0,0,0,0], dp, None, None, None, None, None)
        print(f"Compressed upgrade file {(len(image) - len(fw_upgrade.image)) / len(image):0.1%}")
    del image
    with tempfile.TemporaryDirectory() as temp_dir:
        output_file = os.path.join(temp_dir, os.path.basename(os.path.splitext(args.image)[0]))
        device.combine(output_file, mf, fw_upgrade.image, not args.no_processing, 0)

        def progress(transferred, total, msg):
            if msg is not None:
                print('\r  {msg}', flush=True, end='')
            else:
                if transferred > total:     # Padding bytes can be included in the transferred amount
                    transferred = total
                p = transferred / total
                print('\r  ' + f'{p:.1%}'.rjust(6, ' ') + f' -- {int(transferred / 1024)} of {int(total / 1024)} KB', flush=True, end='')
                if transferred == total:
                    print()

        def device_event_handler(serif, evt):
            if evt == device_serial.DeviceEvent.MANUAL_RESET_REQUEST:
                print("Reset device now")
            elif evt == device_serial.DeviceEvent.AUTOMATIC_RESET:
                print("Device reset")
            elif evt == device_serial.DeviceEvent.BOOTLOADER_ACTIVE:
                print("Successfully entered bootloader")
            elif evt == device_serial.DeviceEvent.FILE_TRANSFER_SETUP:
                print(f'  Setting up file transfer (<{dp.transfer_setup_time:.0f} seconds)...')
            elif evt == device_serial.DeviceEvent.FILE_TRANSFER_SUCCESS:
                print('  Transfer completed successfully')
            elif evt == device_serial.DeviceEvent.FILE_TRANSFER_FAIL:
                print('  Transfer failed')
            elif evt == device_serial.DeviceEvent.APPLYING_UPDATE:
                print(f'Applying upgrade (<{dp.upgrade_time} seconds)...')

        try:
            if args.command_interface:
                serif = device_serial.CommandInterface(dp, args.port, args.baudrate, event_cb=device_event_handler)
            else:
                serif = device_serial.DebugInterface(dp, args.port, args.baudrate, event_cb=device_event_handler)
            serif.open()
        except:
            print("Failed to open serial port")
            return

        try:
            with device_serial.DeviceBootloader(serif) as bl:
                print("Transferring upgrade file...")
                try:
                    upgraded = False
                    if bl.send_upgrade(output_file, apply=False, progress=progress):
                        if 'flash' in dp.bootloader_commands:
                            print('Applying upgrade...')
                            # The upgrade was applied immediately if the bootloader does not support flash
                            upgraded = bl.flash()
                        else:
                            upgraded = True

                    if upgraded:
                        print(f'{dp.name} upgraded')
                    else:
                        print('Upgrade failed')
                except TimeoutError:
                    print('  Transfer timed out')
                    return
        except TimeoutError:
            print('Timeout when entering bootloader')
            return


def hex_int_arg(arg: str):
    """Validate argument as an integer or convert from hex."""
    try:
        if arg.startswith('0x'):
            return int(arg, 16)
        else:
            return int(arg)
    except ValueError:
        raise argparse.ArgumentTypeError('Must be a decimal or hex starting with "0x"')


def version_arg(arg: str) -> list:
    """Validate argument in a version format x.y.z and convert to list of ints."""
    try:

        m = re.findall(r'(\d+)\.*|-rc(\d+)|-beta(\d+)|-alpha(\d+)', arg)

        v = [0,0,0,0]

        for i in range(len(m)):
            for j in range(4):
                if m[i][j] != '':
                    if j > 0:
                        if i != 2:
                            raise ValueError('')
                        v[i] = j * -1
                        v[i+1] = int(m[i][j])
                    else:
                        v[i] = int(m[i][j])

        for i in v:
            if i > 0xff:
                raise ValueError('Version components cannot exceed 255')
        return v
    except ValueError:
        raise argparse.ArgumentTypeError('Version must in M.m.p.b, M.m-rcN, M.m-alphaN, or M.m-betaN format')


def series_arg(arg: str) -> device_types.DeviceSeries:
    """Validate argument is a valid device series name."""
    try:
        dt = device_types.DeviceSeries[arg]
    except KeyError:
        valid_series = ', '.join([s.name for s in device_types.DeviceSeries])
        raise argparse.ArgumentTypeError(f'Unsupported device series, must be one of {valid_series}')
    return dt


def description(arg: str):
    desc = textwrap.dedent(f'''\
        Commands supporting device firmware upgrade packaging with
        BSDIFF and LZ4 compression with options to apply a SUIT
        manifest and COSE signing using ES256.

        BSDIFF and LZ4 algorithms are modified to use a 512 byte block
        size making patches and compressed images compatible with
        MultiTech\'s bootloader (version 1.0+).

        Provide --help or -h option to see all sub-commands.
    ''')
    print(desc)


def add_parser(subparsers):
    valid_series = ', '.join([s.name for s in device_types.DeviceSeries])

    device_parser = subparsers.add_parser('device', help='Device commands')
    device_parser.set_defaults(func=description)
    device_subparsers = device_parser.add_subparsers(metavar='CMD')

    key_gen_parser = device_subparsers.add_parser('keygen', help='Create a key pair for signing a manifest.')
    key_gen_parser.add_argument('name', type=str, help='Name of key')
    key_gen_parser.add_argument('-d', '--dir', type=str, help='Directory path to save key files')
    key_gen_parser.set_defaults(func=key_gen)

    key_pub_parser = device_subparsers.add_parser('keypub', help='Export public key from a private key.')
    key_pub_parser.add_argument('priv_key_file', type=str, help='Path to private key file')
    key_pub_parser.add_argument('-f', '--format', choices=['hex', 'c'], help='Key output format')
    key_pub_parser.add_argument('-o', '--output', type=str,
                                help='Output file path')
    key_pub_parser.set_defaults(func=key_pub)

    patch_parser = device_subparsers.add_parser('patch', aliases=['pa'],
                                         help='Create a firmware patch from old and new images.')
    patch_parser.add_argument('original', type=str, help='Path to original firmware image')
    patch_parser.add_argument('upgrade', type=str, help='Path to upgrade firmware image')
    patch_parser.add_argument('-m', '--manifest', action='store_true',
                              help='Add a manifest to patch image, requires version and class description arguments')
    patch_parser.add_argument('-d', '--description', help='Description of upgrade')
    patch_parser.add_argument('-i', '--series', type=str,
                              help=f'Target hardware series ({valid_series}).')
    patch_parser.add_argument('-I', '--model', type=str,
                              help='A more precise hardware description than the series.')
    patch_parser.add_argument('-v', '--version', type=version_arg,
                              help='Firmware version in upgrade')
    patch_parser.add_argument('-V', '--required-version', type=version_arg,
                              help='Version of original firmware in x.y.z format')
    patch_parser.add_argument('-n', '--vendor', type=str,
                              help='Vendor name, defaults to "Multi-Tech System Inc."')
    patch_parser.add_argument('-N', '--vendor-dns', type=str,
                              help='Vendor DNS, Defaults to "multitech.com"')
    patch_parser.add_argument('-s', '--sign', metavar='KEYFILE', type=str, default=None,
                              help='Sign manifest with the specified private key')
    patch_parser.add_argument('-b', '--bootloader', action='store_true',
                              help='Images contain a bootloader')
    patch_parser.add_argument('-c', '--crc', action='store_true',
                              help='Append CRC32 to end of output file')
    patch_parser.add_argument('-o', '--output', type=str,
                              help='Output file path')
    patch_parser.set_defaults(func=patch)

    compress_parser = device_subparsers.add_parser('compress', aliases=['co'], help='Compress a firmware image.')
    compress_parser.add_argument('image', type=str, help='Path to firmware image')
    compress_parser.add_argument('-m', '--manifest', help='Add a manifest to compressed image', action='store_true')
    compress_parser.add_argument('-d', '--description', help='Description of upgrade')
    compress_parser.add_argument('-i', '--series', type=str,
                                 help=f'Target hardware series ({valid_series}).')
    compress_parser.add_argument('-I', '--model', type=str,
                                 help='A more precise hardware description than the series.')
    compress_parser.add_argument('-v', '--version', type=version_arg,
                                 help='Firmware version in upgrade')
    compress_parser.add_argument('-n', '--vendor', type=str,
                                 help='Vendor name, defaults to "Multi-Tech System Inc."')
    compress_parser.add_argument('-N', '--vendor-dns', type=str,
                                 help='Vendor DNS, Defaults to "multitech.com"')
    compress_parser.add_argument('-s', '--sign', metavar='KEYFILE', type=str, default=None,
                                 help='Sign manifest with the specified private key')
    compress_parser.add_argument('-b', '--bootloader', action='store_true',
                                 help='Images contain a bootloader')
    compress_parser.add_argument('-c', '--crc', action='store_true',
                                 help='Append CRC32 to end of output file')
    compress_parser.add_argument('-o', '--output', type=str,
                                 help='Output file path')
    compress_parser.set_defaults(func=compress)

    plain_parser = device_subparsers.add_parser('plain', aliases=['pl'],
                                         help='Create a plain firmware upgrade.')
    plain_parser.add_argument('image', type=str, help='Path to firmware image')
    plain_parser.add_argument('-m', '--manifest', action='store_true', help='Add a manifest to patch image.')
    plain_parser.add_argument('-d', '--description', help='Description of upgrade')
    plain_parser.add_argument('-i', '--series', type=str,
                              help=f'Target hardware series ({valid_series}).')
    plain_parser.add_argument('-I', '--model', type=str,
                              help='A more precise hardware description than the series.')
    plain_parser.add_argument('-v', '--version', type=version_arg,
                              help='Firmware version in upgrade')
    plain_parser.add_argument('-n', '--vendor', type=str,
                              help='Vendor name, defaults to "Multi-Tech System Inc."')
    plain_parser.add_argument('-N', '--vendor-dns', type=str,
                              help='Vendor DNS, Defaults to "multitech.com"')
    plain_parser.add_argument('-s', '--sign', metavar='KEYFILE', type=str, default=None,
                              help='Sign manifest with the specified private key')
    plain_parser.add_argument('-b', '--bootloader', action='store_true',
                              help='Images contain a bootloader')
    plain_parser.add_argument('-c', '--crc', action='store_true',
                              help='Append CRC32 to end of output file')
    plain_parser.add_argument('-o', '--output', type=str,
                              help='Output file path')
    plain_parser.set_defaults(func=plain)

    manifest_parser = device_subparsers.add_parser('manifest', aliases=['mf'], help='Create a manifest for a firmware image.')
    manifest_parser.add_argument('series', type=str, help=f'Target hardware series ({valid_series}).')
    manifest_parser.add_argument('image', type=str, help='Path to firmware image')
    manifest_parser.add_argument('-a', '--apply', action='store_true', help='Add manifest to directly to image file')
    manifest_parser.add_argument('-f', '--format', choices=['text', 'hex'], help='Output format')
    manifest_parser.add_argument('-d', '--description', help='Description of upgrade')
    manifest_parser.add_argument('-I', '--model', type=str,
                                 help='A more precise hardware description than the series.')
    manifest_parser.add_argument('-v', '--version', type=version_arg,
                                 help='Firmware version in upgrade')
    manifest_parser.add_argument('-n', '--vendor', type=str,
                                 help='Vendor name, defaults to "Multi-Tech System Inc."')
    manifest_parser.add_argument('-N', '--vendor-dns', type=str,
                                 help='Vendor DNS, Defaults to "multitech.com"')
    manifest_parser.add_argument('-p', '--patch', metavar='ORIGVER', type=version_arg,
                                 help='Image is a patch for original version ORIGVER')
    manifest_parser.add_argument('-c', '--compressed', action='store_true',
                                 help='Image is compressed')
    manifest_parser.add_argument('-s', '--sign', metavar='KEYFILE', type=str, default=None,
                                 help='Sign manifest with the specified private key')
    manifest_parser.add_argument('-b', '--bootloader', action='store_true',
                                 help='Images contain a bootloader')
    manifest_parser.add_argument('-o', '--output', type=str,
                                 help='Output file path')
    manifest_parser.set_defaults(func=manifest)

    verify_parser = device_subparsers.add_parser('verify',
                                          help='Verify signature and hash of a manifest or image with a manifest')
    verify_parser.add_argument('image', type=str, help='Path to a image file')
    verify_parser.add_argument('pub_key_file', type=str, help='Path to public key file')
    verify_parser.set_defaults(func=verify)

    crc_parser = device_subparsers.add_parser('crc', help='Add a CRC32 to an image')
    crc_parser.add_argument('image', type=str, help='Path to a image file')
    crc_parser.add_argument('-o', '--output', type=str,
                            help='Output file path')
    crc_parser.set_defaults(func=crc)

    upgrade_parser = device_subparsers.add_parser('upgrade', help='Upgrade a device over serial')
    upgrade_parser.add_argument('series', type=str, help=f'Device series ({valid_series})')
    upgrade_parser.add_argument('port', type=str, help='Serial port device name (COM3, /dev/ttyACM0, etc.)')
    upgrade_parser.add_argument('image', type=str, help='Path to firmware image')
    upgrade_parser.add_argument('-b', '--bootloader', action='store_true',
                                help='Images contain a bootloader')
    upgrade_parser.add_argument('--command-interface',  action='store_true',
                                help='Serial port is the device\'s AT command interface.')
    upgrade_parser.add_argument('-r', '--baudrate', type=int, help='Serial port baudrate', default=115200)
    upgrade_parser.add_argument('-x', '--no-processing',  action='store_true', help='Image already has CRC, use as-is')
    upgrade_parser.set_defaults(func=upgrade)
