# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        runall
# Purpose:     to run all tests
#
# Author:      Evgeniy Semenov
#
# Created:     25.03.2016
# Copyright:   (c) Evgeniy Semenov 2016-2019
# Licence:     MIT
# -------------------------------------------------------------------------------
import unittest
import os
import sys
from importlib import reload

reload(sys)
import re


def expand_mod_name(pack, module):
    return "{0}.{1}".format(pack, module)


def main():
    tst = re.compile(r"^[a-z0-9._-]+_test.py$", re.IGNORECASE)
    cd = os.path.dirname(os.path.abspath(__file__))
    af = os.listdir(cd)
    testmodules = []
    for fs in af:
        rez = tst.findall(fs)
        if len(rez) > 0:
            testmodules.append(rez[0][:-3])

    suite = unittest.TestSuite()

    for t in testmodules:
        try:
            # If the module defines a suite() function, call it to get the suite.
            mod = __import__(
                expand_mod_name("pyncli.test", t),
                globals(),
                locals(),
                ["suite"],
            )
            suitefn = getattr(mod, "suite")
            suite.addTest(suitefn())
        except (ImportError, AttributeError):
            # else, just load all the test cases from the module.
            suite.addTest(
                unittest.defaultTestLoader.loadTestsFromName(
                    expand_mod_name("pyncli.test", t)
                )
            )

    unittest.TextTestRunner().run(suite)


if __name__ == "__main__":
    main()
