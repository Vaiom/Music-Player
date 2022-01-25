# Program Name: Mp3 Music Player
# Created by: Bryant Liu
# Date Created: December 25 2021

import math
from tinytag import TinyTag, TinyTagException

# convert time to --:-- format
def time_convert(t):
    t = math.ceil(t)
    # getting seconds
    sec = str(math.ceil(t%60))
    if len(sec) == 1:
        sec = "0" + sec
    # getting minutes
    min = str(math.ceil(t//60))
    if len(min) == 1:
        min = "0" + min
    template = "{}:{}"
    
    return template.format(min, sec)


    # if t/60 < 1:
    #     timesecs = math.ceil(t)
    #     secsstr = str(timesecs)
    #     if len(secsstr) == 1:
    #         secsstr = "0" + secsstr
    #     return f"00:{secsstr}"
    # else:
    #     
    #     timesecs = t%60
    #     timesecs = math.ceil(timesecs)
    #     secsstr = str(timesecs)
    #     if len(secsstr) == 1:
    #         secsstr = "0" + secsstr
    #  
    #     timemins = int(t//60)
    #     minsstr = str(timemins)
    #     if len(minsstr) == 1:
    #         minsstr = "0" + minsstr
    #     return f"{minsstr}:{secsstr}"
    
# rounds bitrate
def bitrate_round(bitrate):
    bitrate = round(bitrate)
    return bitrate

# converst kilobytes to megabytes (rounded)
def kb_to_mb(kilobytes):
    megabytes = kilobytes/1000000
    megabytes = round(megabytes,2)
    return megabytes

def get_song_data(filename):
    # attempts to tag file
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
        return title, artist, duration, file, ftype, fsize, bitrate, directory, rawsecs
    # title
    try:
        title = tag.title
        if title == None:
            title = "Unknown"
    except TinyTagException:
        title = "Unknown"
    # artist
    try:
        artist = tag.artist
        if artist == None:
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
        if file == None:
            file = "Unknown"
    except TinyTagException:
        file = "Unknown"
    # type of file
    try:
        temp = x.rindex(".")
        ftype = x[temp:]
        if ftype == None:
            ftype = "Unknown"
    except TinyTagException:
        ftype = "Unknown"
    # file size
    try:
        fsize = tag.filesize
        try:
            fsize = kb_to_mb(fsize)
        except:
            fsize= "-"
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
        if directory == None:
            directory = "Unknown"
    except TinyTagException:
        directory = "Unknown"
    # raw duration in seconds
    try:
        rawsecs = tag.duration
    except TinyTagException:
        rawsecs = None
    
    return title, artist, duration, file, ftype, fsize, bitrate, directory, rawsecs

