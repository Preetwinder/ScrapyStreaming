from json import dumps, loads
from inspect import getmembers, isclass

from scrapy.http.request import Request
from scrapy.http.response import Response

import items


def deserializeLine(line):
    obj = loads(line)
    if not isinstance(obj, list):
        obj = [obj]
    lister = []
    if obj[0]['type'] == 'spider_settings':
        return obj[0]
    for element in obj:
        if element['type'] == 'request':
            request = Request(element['url'])      
            request.meta.update(element['meta'])
            request.meta['callback'] = element['callback']
            lister.append(request)
        if element['type'] == 'item':
            item = dictToItem(element['item'], element['name'])
            lister.append(item)
    if len(lister) is 1:
        return lister[0]
    else:
        return lister


ItemDict = {}


def dictToItem(d, name):
    global ItemDict
    if not ItemDict:
        ItemDict = {name:obj for name, obj in getmembers(items) if isclass(obj)}
    return ItemDict[name](d)


def serializeObject(obj):
    if isinstance(obj, Response):
        response = {}
        response['url'] = obj.url
        response['body'] = obj.body
        if 'callback' in obj.meta:
            response['callback'] = obj.meta['callback']
        else:
            response['callback'] = 'parse'
        response['meta'] = obj.meta
        return dumps(response)
