from scratch import ccb
from scratch import ceb
from scratch import cmbc
from scratch import abc
from scratch import citic
bl = citic.BanksGetter().fetchBankList();
if bl != None:
    for b in bl:
        print b
