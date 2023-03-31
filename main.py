#!/usr/bin/python3

import importlib
import sqlite3
import noticeHelpers
import telegram_send

sqliteConnection = sqlite3.connect("state.db")
sqliteCursor = sqliteConnection.cursor()

print("Starting...")

modules = ['hampshire','surrey']

for m in modules:
    module = importlib.import_module(m)
    fetcher = module.fetcher()

    print("module: ", module.__name__)

    try:
        notices = fetcher.getNotices()
    except Exception as err:
        print("error fetching notices" + err)
        continue

    print(str(len(notices)) +" current notices found")

    r = sqliteCursor.execute("SELECT id, content_hash FROM state_tracker WHERE module=?", [module.__name__])
    lastState = noticeHelpers.rowsToDict(r.fetchall())

    newIds = noticeHelpers.getNewNotices(lastState, notices)
    removedIds = noticeHelpers.getRemovedNotices(lastState, notices)
    changedIds = noticeHelpers.getChangedNotices(lastState, notices)

    for id in newIds:
        sqliteCursor.execute("INSERT INTO state_tracker (module,id,content_hash) VALUES(?,?,?)", [module.__name__, id, noticeHelpers.getNoticeHash(notices[id])])
        telegram_send.send(
                messages=[ noticeHelpers.telegramMessageFormatter('New notice added', module.organisation, notices[id]) ],
                files=noticeHelpers.fileFetcher(notices[id]["attachments"]),
                conf=module.telegramConfig, parse_mode="markdown")

    for id in removedIds:
        sqliteCursor.execute("DELETE FROM state_tracker WHERE module=? AND id=?", [module.__name__, id])

    for id in changedIds:
        sqliteCursor.execute("UPDATE state_tracker SET content_hash=? WHERE module=? AND id=?", [noticeHelpers.getNoticeHash(notices[id]), module.__name__, id])
        telegram_send.send(
                messages=[ noticeHelpers.telegramMessageFormatter('Changed notice', module.organisation, notices[id]) ],
                files=noticeHelpers.fileFetcher(notices[id]["attachments"]),
                conf=module.telegramConfig, parse_mode="markdown")

    sqliteConnection.commit()

    print("newIds=", newIds)
    print("removedIds=", removedIds)
    print("changedIds=", changedIds)


print("Exiting...")
