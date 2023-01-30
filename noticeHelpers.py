import hashlib
import urllib
import os
import json

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
    json_blob = json.dumps(notice).encode('utf-8')
    return hashlib.md5(json_blob).hexdigest()


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


def fileFetcher(attachments):
    responses = []

    for file_name in attachments:
        url = attachments[file_name]
        tmp_file = "/tmp/" + file_name

        urllib.request.urlretrieve(url, tmp_file)
        f = open(tmp_file, 'rb')
        responses.append(f)

    return responses
