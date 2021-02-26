from rcute_cozmars.util import find_service
from rcute_cozmars import AioRobot, AioCube
from rcute_ai import ObjectRecognizer, FaceRecognizer, QRCodeRecognizer, STT, WakeWordDetector
import cv2
import logging, asyncio
logger = logging.getLogger('rcute-scratch-link')

class LinkServer:
    def __init__(self):
        self.localvars = {}
        self.video_preprocessors = {'obj':None, 'face':None, 'qr':None}
        self.video_postprocessors = self.video_preprocessors.copy()
        self.video_settings = {}
        self.wwd=None

    def __del__(self):
        asyncio.gather(*[v.disconnect() for v in self.localvars.values() if hasattr(v, 'disconnect')], return_exceptions=True)

    async def discover_peripheral(self, serv, type):
        return [(a.name.split('.')[0], a.port) for a in await find_service(serv, type)]

    async def connect_peripheral(self, init_cmd, serial):
        a = self.localvars.get(serial)
        if not (a and a.connected):
            self.localvars[serial] = a = self._create(init_cmd)
        await a.connect()

    async def peripheral_event(self, serial):
        a = self.localvars[serial]
        count = 5
        while not hasattr(a, '_event_rpc') and count >0:
            count -=.5
            await asyncio.sleep(.5)
        a._event_task.cancel()
        if isinstance(a, AioRobot):
            a._event_rpc.cancel()
            a._event_rpc = a._rpc.sensor_data(3)
        async for ev in a._event_rpc:
            yield ev

    async def disconnect_peripheral(self, serial):
        a = self.localvars.pop(serial, None)
        if a:
            await a.disconnect()

    def _create(self, init_cmd):
        return eval(init_cmd, {'__builtins__':{}, 'AioRobot': AioRobot, 'AioCube': AioCube,
                                                 'ObjectRecognizer': ObjectRecognizer, 'FaceRecognizer': FaceRecognizer, 'QRCodeRecognizer': QRCodeRecognizer,
                                                 'STT': STT, 'WakeWordDetector': WakeWordDetector})

    async def scmd(self, cmd): # simple command
        if cmd.startswith('await '):
            return await eval(cmd[6:], {'__builtins__':{}, 'lv':self.localvars})
        else:
            return eval(cmd, {'__builtins__':{}, 'lv':self.localvars})

    def set_video(self, k, v):
        self.video_settings[k] =v

    async def video(self, serial):
        def process_img(img):
            rec = {}
            for k,v in self.video_preprocessors.items():
                rec[k] = v(img) if v else None
            for k,v in self.video_postprocessors.items():
                v and rec[k] and v(img, *rec[k])
            return cv2.imencode('.jpg', img)[1].tobytes(), rec

        async with self.localvars[serial].camera.get_buffer() as buf:
            self.video_settings['pause'] = False
            async for img in buf:
                if self.video_settings.get('pause'):
                    continue
                if self.video_settings.get('flip'):
                    img = cv2.flip(img, 1)
                yield await asyncio.get_running_loop().run_in_executor(None, process_img, img)

    async def add_video_processor(self, serial, init_cmd, pre, post):
        a = self.localvars.get(serial)
        if not a:
            self.localvars[serial] = a = await asyncio.get_running_loop().run_in_executor(None, self._create, init_cmd)
        self.video_preprocessors[serial] = getattr(a, pre)
        self.video_postprocessors[serial] = getattr(a, post)

    def rm_video_processor(self, serial):
        self.video_postprocessors[serial] = self.video_preprocessors[serial] = None

    async def audio(self, serial):
        async with self.localvars[serial].microphone.get_buffer() as buf:
            while True:
                if self.wwd:
                    yield await asyncio.get_running_loop().run_in_executor(None, self.wwd.detect, buf)
                else:
                    await asyncio.sleep(1)

    def start_wwd(self, serial, init_cmd):
        a = self.localvars.get(serial)
        if not a:
            self.localvars[serial] = a = self._create(init_cmd)
        self.wwd = a

    def stop_wwd(self):
        self.wwd = None

    async def stt(self, serial, stt_serial):
        rec = self.localvars.get(stt_serial)
        if not rec:
            self.localvars[stt_serial] = rec = await asyncio.get_running_loop().run_in_executor(None, STT, stt_serial.split('-')[1])
        mic = self.localvars[serial].microphone
        if mic.closed:
            raise RuntimeError('Microphone is closed')
        async with mic.get_buffer() as buf:
            return await asyncio.get_running_loop().run_in_executor(None, rec.stt, buf)

    def sst_lang_list(self):
        lang_desc = {'en':'English','zh':'中文'}
        return {l: lang_desc.get(l, l) for l in STT.get_lang_list()}
