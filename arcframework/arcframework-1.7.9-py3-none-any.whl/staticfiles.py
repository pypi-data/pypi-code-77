from starlette.responses import FileResponse
import os


class StaticFile:
    def __init__(self, directory):
        self.directory = directory
    
    async def __call__(self, path):
        return FileResponse(path)