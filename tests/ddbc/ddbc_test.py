# -*- coding: utf-8 -*-

from unittest import TestCase
from nose.tools import ok_

import ddbc


class DdbcTestCase(TestCase):
    def test_version(self):
        ok_(ddbc.__version__ is not None)
