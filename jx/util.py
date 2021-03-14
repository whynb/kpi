# coding=utf-8

import sys
import logging
import datetime
from time import *
from dateutil.relativedelta import relativedelta


# logger instance
logger = logging.getLogger('django')


def cascallback(tree):
    logger.info(tree[0][0].text)
    return


def cascallback2(tree):
    return cascallback(tree)


def sys_info():
    info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
    return info


def dictfetchall(cursor):
    # return all rows from db cursor as dict
    try:
        desc = cursor.description
        return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]
    except:
        logger.error(sys_info())
        return []


def uuidToString(_str):
    return _str.replace('-', '') if _str else ''


def create_time():
    return "%.0f" % (mktime(localtime())*1000)


def now():
    current = datetime.datetime.now()
    return current.strftime('%Y-%m-%d %H:%M:%S')


def today():
    current = datetime.datetime.now()
    return current.strftime('%Y-%m-%d')


def string_to_datetime(st):
    import datetime
    return datetime.datetime.strptime(st, "%Y-%m-%d %H:%M:%S")


def month_end(m):
    return str(string_to_datetime(m[:7] + "-01 23:59:59") + relativedelta(months=1) - relativedelta(days=1))


def trim(zstr):
    ystr = zstr.lstrip()
    ystr = ystr.rstrip()
    ystr = ystr.strip()
    return ystr


def row_replace_key(row, key):
    res = {}
    c_str, v_str, u_str = '', '', ''
    for k, v in row.items():
        if k in key:
            res[key[k]] = v
            c_str += str(key[k]) + ', '
            v_str += "'" + str(v).replace("'", "\\'") + "', "
            u_str += str(key[k]) + "='" + str(v).replace("'", "\\'") + "', "
        else:
            res[k] = v
    return res, c_str[:-2], v_str[:-2], u_str[:-2]


if __name__ == '__main__':

    _key = {'ID': 'id', '单位号': 'DWH', '单位名称': 'DWMC', '单位英文名称': 'DWYWMC', '单位简称': 'DWJC'}
    _row = {'单位号': '00000A', '单位名称': '东北大学', '单位英文名称': 'NEU', '建立年月 ': 190901}
    print(row_replace_key(_row, _key))

    exit(0)
