#coding=utf-8
from datetime import datetime
import re

#1922-2-1
def parseDashLineStyle(dateStr):
    if dateStr:
        return datetime.strptime(dateStr, "%Y-%m-%d");

def parseChineseStyle(dateStr):
    if dateStr:
        if dateStr.find("月") != -1 and dateStr.find("日") != -1:
            if dateStr.find("年") != -1:
                return parseChineseStyleYMD(dateStr);
            else:
                return parseChineseStyleMD(dateStr);

def parseChineseStyleYMD(dateStr):
    if dateStr:
         return datetime.strptime(dateStr, "%Y年%m月%d日");

def parseChineseStyleMD(dateStr):
    if dateStr:
         dt = datetime.strptime(dateStr, "%m月%d日");
         return dt.replace(year=datetime.now().year);

def parseSlashStyle(dateStr):
    if dateStr:
        cnt = dateStr.count("/");
        if cnt == 2:
            return datetime.strptime(dateStr, "%Y/%m/%d");
        elif cnt == 1:
            l = dateStr.split("/");
            year = int(l[0]);
            month = int(l[1]);
            return datetime(year=year, month=month, day=1);

def parseZhiStyle(s):
    if s:
        s = re.sub(r".*至(.*)", r"\1", s);
        print "s", s , "$"
        return parseDashLineStyle(s);

