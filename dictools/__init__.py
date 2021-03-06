# -*- coding: utf-8 -*-

import logging
import traceback

__all__ = ['dict_del_vals', 'get_by_path', 'make_getter',
           'dict2dotnotation']


def dict_del_vals(dictin, vals=[None], stop_recursion=False):
    for key in dictin.keys():
        if dictin.get(key) in vals:
            del dictin[key]
        elif type(dictin[key]) is dict:
            dictin[key] = dict_del_vals(dictin[key], vals)
    if not stop_recursion:
        if {} in vals:
            dict_del_vals(dictin, [{}], stop_recursion=True)
    return dictin


def get_by_path(d, keys, default=None):
    try:
        if "." in keys:
            key, rest = keys.split(".", 1)
            if str(key).isdigit():
                try:
                    key = int(key)
                except:
                    logging.error(traceback.format_exc())
            return get_by_path(d.get(key, {}), rest, default)
        else:
            return d.get(keys, default)
    except:
        return default


def make_getter(d, root=None, default=None):
    def func(keys, default=default, alt=None, alt2=None):
        if type(root) is str and type(keys) is str:
            keys = root + "." + keys
        ret = get_by_path(d, keys, default)
        if ret is None:
            if type(root) is str and type(alt) is str:
                alt = root + "." + alt
            ret = get_by_path(d, alt, default)
            if ret is None:
                if type(root) is str and type(alt2) is str:
                    alt2 = root + "." + alt2
                ret = get_by_path(d, alt2, default)
        return ret
    return func


def dict2dotnotation(ddict, path=[], rdict={}, rec=False):
    dd = ddict
    if rec is False:
        rd = {}
        rec = True
    else:
        rd = rdict

    def listtostr(l, k=None):
        ret = ""
        for i in l:
            if ret != "":
                ret += "."
            ret += i
        if k is not None:
            if ret != "":
                ret += "."
            ret += k
        return ret
    for key in dd:
        if type(dd[key]) is not dict:
            rd[listtostr(path, key)] = dd[key]
        else:
            path.append(key)
            dict2dotnotation(dd[key], path, rd, rec)
            path.pop()
    return rd
