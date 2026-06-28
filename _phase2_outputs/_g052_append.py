# -*- coding: utf-8 -*-
import json, os, sys, importlib.util

BASE = os.path.dirname(__file__)
CJSON = os.path.join(BASE,'_g052_content.json')

def load():
    return json.load(open(CJSON,encoding='utf-8'))

def save(C):
    json.dump(C, open(CJSON,'w',encoding='utf-8'), ensure_ascii=False)
    print("total now:", len(C))
