from scratch import ccb
from scratch import ceb
from scratch import cmbc
from scratch import abc
from scratch import citic
from scratch import comm
from scratch import psbc
from scratch import bea
from scratch import dalian
from scratch import cqrcb
from scratch import spdb
bl = spdb.BanksGetter().fetchBankList();
if bl != None:
    for b in bl:
        print b
