import pkgutil
import scratch
import db
import util
from datetime import datetime

from bank import Bank

from scratch import cmb
from scratch import ccb
from scratch import ceb
from scratch import cmbc
from scratch import abc
from scratch import ecitic
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
from scratch import icbc
from scratch import boc
from scratch import wenzhou

banks = [wenzhou,]

for bank in banks:
    bl = bank.BanksGetter().fetchBankList();
    if bl != None:
        for b in bl:
            print b
