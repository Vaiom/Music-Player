# Program Name: Mp3 Music Player
# Created by: Bryant Liu
# Date Created: December 26 2021

def get_settings():
    """
    creating/reading config.txt
    """
    volume_level, shuffle, repeat = 50, "off", "off"
    while True:
        try:
            configFile = open("config.txt", "r")
            volume_level = configFile.readline()
            index = volume_level.find(":")
            volume_level = volume_level[:index]
            shuffle = configFile.readline()
            index = shuffle.find(":")
            shuffle = shuffle[:index]
            repeat = configFile.readline()
            index = repeat.find(":")
            repeat = repeat[:index]
            configFile.close()
            volume_level = int(volume_level)
            shuffle = str(shuffle)
            repeat = str(repeat)
            if volume_level < 0 or volume_level > 100:
                raise Exception
            if shuffle not in ("off", "on"):
                raise Exception
            if repeat not in ("off", "queue", "track"):
                raise Exception
            break
        except:
            # rewrite config if error
            configFile = open("config.txt", "w")
            volume_level = 50
            shuffle = "off"
            repeat = "off"
            configFile.writelines([f"{volume_level}:volume\n",
                                   f"{shuffle}:shuffle\n", f"{repeat}:repeat"])
            configFile.close()
    return volume_level, shuffle, repeat


def write_settings(vol=50, shuffle="off", repeat="off"):
    """
    updating config.txt
    """
    configFile = open("config.txt", "w")
    volume_level = vol
    shuffle = shuffle
    repeat = repeat
    configFile.writelines([f"{volume_level}:volume\n",
                           f"{shuffle}:shuffle\n", f"{repeat}:repeat"])
    configFile.close()


def get_songs():
    """
    creating/reading queue.txt
    """
    while True:
        try:
            queueFile = open("queue.txt", "r", encoding="utf-8")
            list = []
            for x in queueFile:
                x = repr(x)
                list.append(x[1:-3])
            queueFile.close()
            break
        except:
            queueFile = open("queue.txt", "x", encoding="utf-8")
            queueFile.close()
    return list


def write_songs(list=[]):
    """
    updating config.txt
    """
    queueFile = open("queue.txt", "w", encoding="utf-8")
    for entry in list:
        queueFile.write(entry + "\n")
    queueFile.close()
