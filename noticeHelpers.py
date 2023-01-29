import hashlib
import urllib
import os

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
        if isinstance(notice[key], str):
            strings.append(notice[key])
        elif isinstance(notice[key], list):
            for item in notice[key]:
                strings.append(item)

    return hashlib.md5(" ".join(strings).encode('utf-8')).hexdigest()


def rowsToDict(rows):

    out = {}
    for row in rows:
        out[row[0]] = row[1]

    return out


def telegramMessageFormatter(changeDescription, orgName, info):

    lines = []
    lines.append("*" + changeDescription + " by " + orgName + "*")
    lines.append("")
    lines.append("*" + info['title'] + "*")
    lines.append(info['text'])
    lines.append("")
    lines.append(info['url'])

    return "\n".join(lines)


def fileFetcher(urls):
    responses = []

    for url in urls:
        parsed = urllib.parse.urlparse(url)
        file_name = os.path.basename(parsed.path)
        tmp_file = "/tmp/" + file_name

        urllib.request.urlretrieve(url, tmp_file)
        f = open(tmp_file, 'rb')
        responses.append(f)

    return responses
