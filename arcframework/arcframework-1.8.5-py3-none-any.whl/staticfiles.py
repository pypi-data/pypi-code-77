from starlette.responses import FileResponse
import os


class EmptyWSGI:
    def __init__(self):
        ...


class StaticFile:
    def __init__(self, directory):
        self.directory = directory
    
    async def __call__(self, request, path: str):
        return FileResponse(path, media_type="text/css")