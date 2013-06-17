#coding=utf-8
from datetime import datetime

#1922-2-1
def parseBottomDashLineStyle(dateStr):
    return datetime.strptime(dateStr, "%Y-%m-%d");

def parseChineseStyle(dateStr):
    return datetime.strptime(dateStr, "%Y年%m月%d日");
