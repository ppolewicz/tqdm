"""
Sometimes one might want to track progress of stream processing,
which is done by an external library which does not support callbacks.
A good example of such stream is a file-like object.
"""

import os.path
import urllib2

from tqdm import tqdm


def upload_file(file_path, progress_bar):
    size = os.path.getsize(file_path)
    stream = open(file_path, 'rb')
    if progress_bar:
        stream = tqdm(stream=stream,
            total=size,
            unit='B',
            unit_scale=True,
            leave=True,
            miniters=1,
        )
    return upload_finite_stream(stream, size)

def upload_finite_stream(stream, size):
    request = urllib2.Request(
        'http://httpbin.org/put',
        data=stream,
        headers={
            'Content-length': str(size),
        },
    )
    request.get_method = lambda: 'PUT'
    urllib2.urlopen(request)

#upload_file('big_file.dat', True)  # ~4 MB is enough for this

import time

#filename = 'stream_interface.py' ; total=55
filename = 'big_file.dat2'
total = os.path.getsize(filename)

progress_bar = False
progress_bar = True

for mode in [1, 2, 3, 4, 5]:
    print 'mode =', mode
    stream = open(filename, 'rb')
    if progress_bar:
        stream = tqdm(stream=stream,
            total=total,
            unit='B',
            unit_scale=True,
            leave=True,
            miniters=1,
        )
    with stream as f:
        i = 0
        if mode == 1:
            for line in f.readlines():
                i += 1
                #time.sleep(0.01)
        elif mode == 2:
            while 1:
                #data = f.read1(5)
                data = f.read(5) # XXX
                if data:
                    i += 1
                    #time.sleep(0.01)
                else:
                    break
        elif mode == 3: # XXX OK
            while 1:
                data = f.read(5)
                if data:
                    i += 1
                    #time.sleep(0.01)
                else:
                    break
        elif mode == 4: # ok
            for line in f:
                i += 1
                #time.sleep(0.01)
        elif mode == 5:
            for line in f.read().split('\n'):
                i += 1
                #time.sleep(0.01)
        time.sleep(0.3)

print 'all done!'

