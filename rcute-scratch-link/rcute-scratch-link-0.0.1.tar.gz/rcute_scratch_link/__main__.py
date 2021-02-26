import asyncio, websockets, argparse, socket, zeroconf, logging
from wsmprpc import RPCServer
from .server import LinkServer

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", default=20111, type=int,
                    help="Default to 20111. Note: port 20110 should be reserved for the offical scratch-link")

parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
args = parser.parse_args()

if args.verbose:
    logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('rcute-scratch-link')

async def handle_ws(ws, path):
    logger.info(f'connect: {ws.remote_address}')
    try:
        serv = LinkServer()
        await RPCServer(ws, serv).run()
    except websockets.exceptions.ConnectionClosedError:
        pass
    except Exception as e:
        logger.exception(e)
    finally:
        logger.info(f'disconnect: {ws.remote_address}')

start_server = websockets.serve(handle_ws, "localhost", args.port)

hostname = socket.gethostname()
info = zeroconf.ServiceInfo(
        "_ws._tcp.local.",
        "rcute-scratch-link._ws._tcp.local.",
        addresses=[socket.inet_aton(socket.gethostbyname(f'{hostname}.local'))],
        port=args.port,
        properties={},
        server=f"{hostname}.local.")

logger.info('Register service')
zc = zeroconf.Zeroconf()
zc.register_service(info)

try:
    asyncio.get_event_loop().run_until_complete(start_server)
    logger.info("Start rcute-scratch-link")
    asyncio.get_event_loop().run_forever()
finally:
    logger.info('Unregister service')
    zc.unregister_service(info)
    zc.close()