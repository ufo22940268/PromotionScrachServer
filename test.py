import pkgutil
import scratch

from bank import Bank

from scratch import cmb
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
from scratch import cib
from scratch import pingan
from scratch import beijing
from scratch import nbcb
from scratch import hxb
bl = ccb.BanksGetter().fetchBankList();
if bl != None:
    for b in bl:
        print b

