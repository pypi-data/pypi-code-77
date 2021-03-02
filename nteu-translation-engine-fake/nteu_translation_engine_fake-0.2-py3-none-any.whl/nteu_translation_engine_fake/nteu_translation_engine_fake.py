from aiohttp import web
import signal
import asyncio
import logging
import traceback
import os


async def translate(request) -> web.Response:
    try:
        data = await request.json()
        texts = data["texts"]
        translations = []

        for text in texts:
            command = text.split()

            if len(command) == 2 and "wait" == command[0]:
                await asyncio.sleep(int(command[1]))
            elif len(command) == 1 and "error" == command[0]:
                raise Exception("Error keyword given.")
            elif len(command) == 1 and "shutdown" == command[0]:
                pid = os.getpid()
                os.kill(pid, signal.SIGINT)

            translations.append({
                "text": text,
                "translation": text.upper()
            })

        return web.json_response({
            "translations": translations
        })

    except Exception:
        tb = traceback.format_exc()
        tb_str = str(tb)
        logging.error('Error: %s', tb_str)
        return web.Response(text=tb_str, status=500)


class NTEUTranslationEngineFake:
    @staticmethod
    def run(host, port):

        # Create server
        app = web.Application()
        app.router.add_post(
            "/translate", translate
        )

        web.run_app(
            app,
            host=host,
            port=port,
            handle_signals=False
        )