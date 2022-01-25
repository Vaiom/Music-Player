# Program Name: Mp3 Music Player
# Created by: Bryant Liu
# Date Created: December 25 2021

try:
    import math
    from tinytag import TinyTag, TinyTagException
except:
    input("error")


def time_convert(t):
    """convert time to --:-- format"""
    t = math.ceil(t)
    # getting seconds
    sec = str(math.ceil(t % 60))
    if len(sec) == 1:
        sec = "0" + sec
    # getting minutes
    min = str(math.ceil(t//60))
    if len(min) == 1:
        min = "0" + min
    template = "{}:{}"
    return template.format(min, sec)


def bitrate_round(bitrate):
    """rounds bitrate"""
    bitrate = round(bitrate)
    return bitrate


def kb_to_mb(kilobytes):
    """convert kilobytes to megabytes"""
    megabytes = kilobytes/1000000
    megabytes = round(megabytes, 2)
    return megabytes


def get_song_data(filename):
    """attempts to extract tags"""
    try:
        x = filename
        tag = TinyTag.get(x)
    except:
        title = "Unknown"
        artist = "Unknown"
        duration = "--:--"
        file = "Unknown"
        ftype = "Unknown"
        fsize = "-"
        bitrate = "-"
        directory = "Unknown"
        rawsecs = None
        return (title, artist, duration, file,
                ftype, fsize, bitrate, directory, rawsecs)
    # title
    try:
        title = tag.title
        if title is None:
            title = "Unknown"
    except TinyTagException:
        title = "Unknown"
    # artist
    try:
        artist = tag.artist
        if artist is None:
            artist = "Unknown"
    except TinyTagException:
        artist = "Unknown"
    # net duration
    try:
        duration = tag.duration
        try:
            duration = time_convert(duration)
        except:
            duration = "--:--"
    except TinyTagException:
        duration = "--:--"
    # file name
    try:
        temp = x.rindex("/")
        file = x[temp+1:]
        if file is None:
            file = "Unknown"
    except TinyTagException:
        file = "Unknown"
    # type of file
    try:
        temp = x.rindex(".")
        ftype = x[temp:]
        if ftype is None:
            ftype = "Unknown"
    except TinyTagException:
        ftype = "Unknown"
    # file size
    try:
        fsize = tag.filesize
        try:
            fsize = kb_to_mb(fsize)
        except:
            fsize = "-"
    except TinyTagException:
        fsize = "-"
    # file bitrate (audio quality)
    try:
        bitrate = tag.bitrate
        try:
            bitrate = bitrate_round(bitrate)
        except:
            bitrate = "-"
    except TinyTagException:
        bitrate = "-"
    # directory to file
    try:
        directory = x
        if directory is None:
            directory = "Unknown"
    except TinyTagException:
        directory = "Unknown"
    # raw duration in seconds
    try:
        rawsecs = tag.duration
    except TinyTagException:
        rawsecs = None

    return (title, artist, duration, file,
            ftype, fsize, bitrate, directory, rawsecs)
