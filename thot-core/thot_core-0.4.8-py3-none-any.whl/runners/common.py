# --- Common Functionality

import os
import re

def escape_path( path ):
    # normalize slashes
    path = re.sub( '[/\\\\]', os.sep, path )

    # quote for spaces
    path = f'"{ path }"'
    return path
