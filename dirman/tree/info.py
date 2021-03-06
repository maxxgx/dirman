"""
Convenience classes for dealing with directory and file properties.
"""
from datetime import datetime
from enum import Enum
import filetype

SIZE_SUFFIXES = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']


def datetime_formatter(time):
    return time.strftime("%Y-%m-%d at %H:%M:%S")


def time_now():
    return datetime_formatter(datetime.now())


class FileType(str, Enum):
    text = 'text'
    image = 'image'
    video = 'video'
    audio = 'audio'
    application = 'application'


class DirInfo:
    """
    Represents the properties of a directory.
    """

    def __init__(
            self, 
            upload_time: str = time_now(), 
            last_accessed: str = time_now(), 
            size: int = None,
            ):
        self.upload_time = upload_time
        self.last_accessed = last_accessed
        self.size = size

    def update(self, size_bytes: int = None) -> None:
        self.last_accessed = time_now()
        self.size = size_bytes or self.size

    def humansize(self):
        """
        Return the number of bytes in a human readable format.

        source: https://stackoverflow.com/questions/14996453/python-libraries-to-calculate-human-readable-filesize-from-bytes
        """
        if self.size is None:
            return "?B"
        i = 0
        nbytes = self.size
        while nbytes >= 1024 and i < len(SIZE_SUFFIXES) - 1:
            nbytes /= 1024.
            i += 1
        f = f"{nbytes:.2f}".rstrip('0').rstrip('.')
        return '%s%s' % (f, SIZE_SUFFIXES[i])

    def __str__(self):
        return f"{self.upload_time} {self.last_accessed} {self.humansize()}"


class FileInfo(DirInfo):
    """
    Represents the properties of a file.
    """

    def __init__(
            self, 
            name: str, 
            ):
        super().__init__()
        ftype = filetype.guess(name)
        if ftype is None: # if not binary -> assume text
            ftype = 'text'
        else:
            ftype = ftype.mime.split('/')[0]
        self.type = FileType[ftype]

    def __str__(self):
        return f"{self.upload_time} {self.humansize()} {self.type}"
