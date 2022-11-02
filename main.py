#!/usr/bin/python3

import importlib
import sqlite3
import noticeHelpers

sqliteConnection = sqlite3.connect("row_state.db")
sqliteCursor = sqliteConnection.cursor()

print("Starting...")

modules = ['hampshire','surrey']

for m in modules:
    module = importlib.import_module(m)
    fetcher = module.fetcher()

    print("module: ", module.__name__)

    notices = fetcher.getByways()
    print(str(len(notices)) +" current notices found")

    currentIds = []
    for id in notices:
        currentIds.append(id)

    print("currentIds=", currentIds)

    r = sqliteCursor.execute("SELECT id, content_hash FROM state_tracker WHERE module=?", [module.__name__])
    lastState = noticeHelpers.rowsToDict(r.fetchall())

    newIds = noticeHelpers.getNewNotices(lastState, notices)
    removedIds = noticeHelpers.getRemovedNotices(lastState, notices)
    changedIds = noticeHelpers.getChangedNotices(lastState, notices)

    for id in newIds:
        sqliteCursor.execute("INSERT INTO state_tracker (module,id,content_hash) VALUES(?,?,?)", [module.__name__, id, noticeHelpers.getNoticeHash(notices[id])])


    sqliteConnection.commit()

    print("newIds=", newIds)
    print("removedIds=", removedIds)
    print("changedIds=", changedIds)


print("Exiting...")
