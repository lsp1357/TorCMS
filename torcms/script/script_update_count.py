# -*- coding: utf-8

import sys

from torcms.model.postcatalog_model import MPostCatalog
from torcms.model.inforcatalog_model import MInforCatalog
from torcms.model.infor_model import MInfor


def run_update_count():

    mappcat = MInforCatalog()
    mapp = MInfor()
    for rec in mappcat.query_all():
        uid= rec.uid
        uuvv = mapp.query_extinfo_by_cat(uid)
        print(uid, uuvv.count())
        mappcat.update_count(uid, uuvv.count())