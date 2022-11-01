#!/usr/bin/python3

import importlib

modules = ['hampshire','surrey']


def getFetchers(modules):

    fetchers = []

    for m in modules:
        module = importlib.import_module(m)
        fetcher = module.fetcher()
        fetchers.append(fetcher)

    return fetchers





print("Starting...")

fetchers = getFetchers(modules)

for fetcher in fetchers:
    print("module: ", fetcher.__module__)

    byways = fetcher.getByways()

    print(byways)
    print(str(len(byways)) +" current byways")

print("Exiting...")



