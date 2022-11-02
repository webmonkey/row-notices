import hashlib

def getNewNotices(last,current):

    newNotices = []
    for id in current:
        if id not in last:
            newNotices.append(id)

    return newNotices

def getRemovedNotices(last,current):

    removedNotices = []

    for id in last:
        if id not in current:
            removedNotices.append(id)

    return removedNotices


def getChangedNotices(last,current):

    changedNotices = []
    for id in current:
        if id in last and last[id] != getNoticeHash(current[id]):
            changedNotices.append(id)

    return changedNotices


def getNoticeHash(notice):

    strings = []

    for key in notice:
        strings.append(key)
        strings.append(notice[key])

    return hashlib.md5(" ".join(strings).encode('utf-8')).hexdigest()


def rowsToDict(rows):

    out = {}
    for row in rows:
        out[row[0]] = row[1]

    return out
