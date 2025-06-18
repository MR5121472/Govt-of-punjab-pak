# imghdr.py (Python 3.13-compatible version)
import struct

def what(file, h=None):
    if h is None:
        if isinstance(file, str):
            with open(file, 'rb') as f:
                h = f.read(32)
        else:
            h = file.read(32)

    for test, kind in tests:
        res = test(h)
        if res:
            return kind
    return None

def test_jpeg(h):
    if h[:3] == b'\xff\xd8\xff':
        return 'jpeg'

def test_png(h):
    if h[:8] == b'\211PNG\r\n\032\n':
        return 'png'

def test_gif(h):
    if h[:6] in (b'GIF87a', b'GIF89a'):
        return 'gif'

def test_bmp(h):
    if h[:2] == b'BM':
        return 'bmp'

def test_webp(h):
    if h[:4] == b'RIFF' and h[8:12] == b'WEBP':
        return 'webp'

tests = [test_jpeg, test_png, test_gif, test_bmp, test_webp]
