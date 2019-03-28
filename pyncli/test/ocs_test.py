# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        ocs_test
# Purpose:      tests
#
# Author:      Evgeniy Semenov
#
# Created:     15.03.2019
# Copyright:   (c) Evgeniy Semenov 2019
# Licence:     MIT
# -------------------------------------------------------------------------------

import unittest
import os
from datetime import datetime
pd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, pd)
from copy import deepcopy
from urllib.parse import urljoin, urlparse
import responses
from ocs.ocs import (
    PERMISSION_CREATE,
    PERMISSION_READ,
    PERMISSION_UPDATE,
    PERMISSION_DELETE,
    PERMISSION_SHARE,
    PERMISSION_ALL,
)
from pyncli.ldap.admexept import AdminException, OperationFailure, WrongParam
from pyncli.ocs import ocs
from pyncli.test.fixtures import *


class TestFuncs(unittest.TestCase):
    def test___human_size_0(self):
        self.assertEqual(ocs.human_size(100), "100")

    def test___human_size_1(self):
        self.assertEqual(ocs.human_size(1000), "1000")

    def test___human_size_2(self):
        self.assertEqual(ocs.human_size(10000), "9.77k")

    def test___human_size_3(self):
        self.assertEqual(ocs.human_size(100000), "97.66k")

    def test___human_size_4(self):
        self.assertEqual(ocs.human_size(1000000), "976.56k")

    def test___human_size_5(self):
        self.assertEqual(ocs.human_size(10000000), "9.54m")

    def test___human_size_6(self):
        self.assertEqual(ocs.human_size(100000000), "95.37m")

    def test___human_size_7(self):
        self.assertEqual(ocs.human_size(1000000000), "953.67m")

    def test___human_size_8(self):
        self.assertEqual(ocs.human_size(10000000000), "9.31g")

    def test___human_size_9(self):
        self.assertEqual(ocs.human_size(100000000000), "93.13g")

    def test___human_size_10(self):
        self.assertEqual(ocs.human_size(1000000000000), "931.32g")

    def test___human_size_11(self):
        self.assertEqual(ocs.human_size(10000000000000), "9.09t")

    def test___human_size_12(self):
        self.assertEqual(ocs.human_size(100000000000000), "90.95t")

    def test___human_size_13(self):
        self.assertEqual(ocs.human_size(1000000000000000), "909.49t")

    def test___human_size_14(self):
        self.assertEqual(ocs.human_size(10000000000000000), "9094.95t")

    def test___human_size_15(self):
        self.assertIsNone(ocs.human_size("ooo"))

    def test___human_permissions_0(self):
        self.assertIsNone(ocs.human_permissions("X"))

    def test___human_permissions_1(self):
        self.assertEqual(ocs.human_permissions(-3), "")

    def test___human_permissions_2(self):
        self.assertEqual(ocs.human_permissions(33), "")

    def test___human_permissions_3(self):
        for key, value in ocs.PERMISSIONS.items():
            self.assertEqual(ocs.human_permissions(value), key)

    def test___human_permissions_4(self):
        self.assertEqual(
            ocs.human_permissions(3), "PERMISSION_READ | PERMISSION_UPDATE"
        )

    def test___human_permissions_5(self):
        self.assertEqual(
            ocs.human_permissions(5), "PERMISSION_CREATE | PERMISSION_READ"
        )

    def test___human_permissions_6(self):
        self.assertEqual(
            ocs.human_permissions(9), "PERMISSION_READ | PERMISSION_DELETE"
        )

    def test___human_permissions_7(self):
        self.assertEqual(
            ocs.human_permissions(17), "PERMISSION_READ | PERMISSION_SHARE"
        )

    def test___human_permissions_8(self):
        self.assertEqual(
            ocs.human_permissions(31),
            "PERMISSION_CREATE | PERMISSION_READ | PERMISSION_UPDATE | PERMISSION_DELETE | PERMISSION_SHARE",
        )

    def test___human_permissions_9(self):
        self.assertEqual(ocs.human_permissions(3, short=True), "ru")

    def test___human_permissions_10(self):
        self.assertEqual(ocs.human_permissions(6, short=True), "cu")

    def test___human_permissions_11(self):
        self.assertEqual(ocs.human_permissions(7, short=True), "cru")

    def test___human_permissions_12(self):
        self.assertEqual(ocs.human_permissions(10, short=True), "ud")

    def test___human_permissions_13(self):
        self.assertEqual(ocs.human_permissions(31, short=True), "cruds")


class TestGroupMembers(unittest.TestCase):
    def setUp(self):
        self.gm = ocs.GroupMembers("member")

    def tearDown(self):
        self.gm = None

    def test___init__0(self):
        self.assertEqual(self.gm.user_id, "member")

    def test___str__0(self):
        self.assertEqual(str(self.gm), "user_id: member")


class TestCreateGroupFolder(unittest.TestCase):
    def setUp(self):
        self.cgf = ocs.CreateGroupFolder(10)

    def tearDown(self):
        self.cgf = None

    def test___init__0(self):
        self.assertEqual(self.cgf.id, 10)

    def test___str__0(self):
        self.assertEqual(str(self.cgf), "<CreateGroupFolder> id: 10")


class TestGroup(unittest.TestCase):
    def setUp(self):
        self.g = ocs.Group(group_id=50, permissions=PERMISSION_ALL)

    def tearDown(self):
        self.g = None

    def test___init__0(self):
        self.assertEqual(self.g.group_id, 50)
        self.assertEqual(self.g.permissions, 31)

    def test___str__0(self):
        self.assertEqual(str(self.g), '<Group> "50" [cruds]')

    def test___info__0(self):
        self.assertEqual(self.g.info, '<Group> "50"')

    def test__eq__0(self):
        self.assertEqual(
            self.g, ocs.Group(group_id=50, permissions=PERMISSION_ALL)
        )

    def test__ne__0(self):
        self.assertNotEqual(
            self.g, ocs.Group(group_id=51, permissions=PERMISSION_ALL)
        )

    def test__ne__1(self):
        self.assertNotEqual(
            self.g, ocs.Group(group_id=50, permissions=PERMISSION_READ)
        )

    def test__ne__2(self):
        self.assertNotEqual(self.g, "q")


class TestGroupFolder(unittest.TestCase):
    def setUp(self):
        self.gf = ocs.GroupFolder(
            id=10,
            mount_point="share",
            groups=["IT", "Admins"],
            quota=-3,
            size=54546540,
        )

    def tearDown(self):
        self.gf = None

    def test___init__0(self):
        self.assertEqual(self.gf.id, 10)
        self.assertEqual(self.gf.mount_point, "share")
        self.assertListEqual(self.gf.groups, ["IT", "Admins"])
        self.assertEqual(self.gf.quota, -3)
        self.assertEqual(self.gf.size, 54546540)

    def test___str__0(self):
        self.assertEqual(str(self.gf), TEST_STR_GROUPFOLDER)


class TestUser(unittest.TestCase):
    def setUp(self):
        self.grp_1 = ocs.Group("IT")
        self.grp_2 = ocs.Group("tester")
        self.user = ocs.User(
            id="user",
            enabled=True,
            storageLocation="/home/nextcloud/user@example.com",
            lastLogin="1544530113000",
            backend="LDAP",
            subadmin=[],
            quota=None,
            email="user@example.com",
            displayname="Pupkin Vasiliy",
            phone="+79010010101",
            address="Russia, Sochi",
            website="https://www.leningrad.spb.ru",
            twitter="@new_account",
            groups=[self.grp_1, self.grp_2],
            language="ru",
            locale="ru",
            backendCapabilities=None,
        )

    def tearDown(self):
        self.user = None
        self.grp_1 = None
        self.grp_2 = None

    def test___init__0(self):
        self.assertEqual(self.user.id, "user")
        self.assertEqual(self.user.enabled, True)
        self.assertEqual(
            self.user.storage_location, "/home/nextcloud/user@example.com"
        )
        self.assertEqual(
            self.user.last_login, datetime(2018, 12, 11, 15, 8, 33)
        )
        self.assertEqual(self.user.backend, "LDAP")
        self.assertListEqual(self.user.subadmin, [])

        # self.assertEqual( self.user.quota, ocs.UserQuota(-3))  #!
        self.assertIsNone(self.user.quota)
        self.assertEqual(self.user.email, "user@example.com")
        self.assertEqual(self.user.displayname, "Pupkin Vasiliy")
        self.assertEqual(self.user.website, "https://www.leningrad.spb.ru")
        self.assertEqual(self.user.twitter, "@new_account")
        self.assertListEqual(self.user.groups, [self.grp_1, self.grp_2])
        self.assertEqual(self.user.language, "ru")
        self.assertEqual(self.user.locale, "ru")
        self.assertIsNone(self.user.backend_capabilities)

    def test___str__0(self):
        self.assertEqual(str(self.user), TEST_STR_USER)


class TestUser2(unittest.TestCase):
    def setUp(self):
        self.grp_1 = ocs.Group("HR")
        self.grp_2 = ocs.Group("staff")
        self.quota_1 = ocs.UserQuota(
            quota=10737418240,
            used=2431492563,
            free=8305925677,
            total=10737418240,
            relative=22.65,
        )
        self.bc = ocs.BackendCapabilities(setDisplayName=1, setPassword=1)
        self.user = ocs.User(
            id="alex",
            enabled=1,
            storageLocation="/home/nextcloud/alex@example.com",
            lastLogin=0,
            backend="Database",
            subadmin=[],
            quota=self.quota_1,
            email="alex_hr@example.com",
            displayname="Ivanov Alex",
            phone="+79010010102",
            address="Russia, Surgut",
            website="https://www.example.ru",
            twitter="@alex_hr",
            groups=[self.grp_1, self.grp_2],
            language="en",
            locale="en",
            backendCapabilities=self.bc,
        )

    def tearDown(self):
        self.user = None
        self.grp_1 = None
        self.grp_2 = None
        self.quota_1 = None
        self.bc

    def test___init__0(self):

        self.assertEqual(self.user.id, "alex")
        self.assertEqual(self.user.enabled, True)
        self.assertEqual(
            self.user.storage_location, "/home/nextcloud/alex@example.com"
        )
        self.assertEqual(self.user.last_login, datetime(1970, 1, 1, 0, 0))
        self.assertEqual(self.user.backend, "Database")
        self.assertListEqual(self.user.subadmin, [])

        self.assertEqual(self.user.quota, self.quota_1)
        self.assertEqual(self.user.email, "alex_hr@example.com")
        self.assertEqual(self.user.displayname, "Ivanov Alex")
        self.assertEqual(self.user.website, "https://www.example.ru")
        self.assertEqual(self.user.twitter, "@alex_hr")
        self.assertListEqual(self.user.groups, [self.grp_1, self.grp_2])
        self.assertEqual(self.user.language, "en")
        self.assertEqual(self.user.locale, "en")
        self.assertEqual(self.user.backend_capabilities, self.bc)

    def test___str__0(self):
        self.assertEqual(str(self.user), TEST_STR_USER_2)


class TestUser3(unittest.TestCase):
    def setUp(self):
        self.grp_1 = ocs.Group("HR")
        self.grp_2 = ocs.Group("staff")
        self.quota_1 = ocs.UserQuota(
            quota=10737418240,
            used=2431492563,
            free=8305925677,
            total=10737418240,
            relative=22.65,
        )
        self.bc = ocs.BackendCapabilities(setDisplayName=1, setPassword=1)
        self.user = ocs.User(
            id="alex",
            enabled=1,
            storageLocation="/home/nextcloud/alex@example.com",
            lastLogin=0,
            backend="Database",
            subadmin=["HR"],
            quota=self.quota_1,
            email="alex_hr@example.com",
            displayname="Ivanov Alex",
            phone="+79010010102",
            address="Russia, Surgut",
            website="https://www.example.ru",
            twitter="@alex_hr",
            groups=[self.grp_1, self.grp_2],
            language="en",
            locale="en",
            backendCapabilities=self.bc,
        )

    def tearDown(self):
        self.user = None
        self.grp_1 = None
        self.grp_2 = None
        self.quota_1 = None
        self.bc

    def test___init__0(self):

        self.assertEqual(self.user.id, "alex")
        self.assertEqual(self.user.enabled, True)
        self.assertEqual(
            self.user.storage_location, "/home/nextcloud/alex@example.com"
        )
        self.assertEqual(self.user.last_login, datetime(1970, 1, 1, 0, 0))
        self.assertEqual(self.user.backend, "Database")
        self.assertListEqual(self.user.subadmin, ["HR"])

        self.assertEqual(self.user.quota, self.quota_1)
        self.assertEqual(self.user.email, "alex_hr@example.com")
        self.assertEqual(self.user.displayname, "Ivanov Alex")
        self.assertEqual(self.user.website, "https://www.example.ru")
        self.assertEqual(self.user.twitter, "@alex_hr")
        self.assertListEqual(self.user.groups, [self.grp_1, self.grp_2])
        self.assertEqual(self.user.language, "en")
        self.assertEqual(self.user.locale, "en")
        self.assertEqual(self.user.backend_capabilities, self.bc)

    def test___str__0(self):
        self.assertEqual(str(self.user), TEST_STR_USER_3_FULL)


class TestUserQuota(unittest.TestCase):
    def setUp(self):
        self.quota = ocs.UserQuota(
            quota=10737418240,
            used=2431492563,
            free=8305925677,
            total=10737418240,
            relative=22.65,
        )

    def tearDown(self):
        self.quota = None

    def test___init__0(self):
        self.assertEqual(self.quota.quota, 10737418240)
        self.assertEqual(self.quota.used, 2431492563)
        self.assertEqual(self.quota.free, 8305925677)
        self.assertEqual(self.quota.total, 10737418240)
        self.assertEqual(self.quota.relative, 22.65)

    def test___str__0(self):
        self.assertEqual(str(self.quota), TEST_STR_QUOTA)


class TestUserQuota2(unittest.TestCase):
    def setUp(self):
        self.quota = ocs.UserQuota(
            quota=5368709120,
            used=0,
            free=5368709120,
            total=5368709120,
            relative=0,
        )

    def tearDown(self):
        self.quota = None

    def test___init__0(self):
        self.assertEqual(self.quota.quota, 5368709120)
        self.assertEqual(self.quota.used, 0)
        self.assertEqual(self.quota.free, 5368709120)
        self.assertEqual(self.quota.total, 5368709120)
        self.assertEqual(self.quota.relative, 0)

    def test___str__0(self):
        self.assertEqual(str(self.quota), TEST_STR_QUOTA_2)

class TestUserQuota3(unittest.TestCase):
    def setUp(self):
        self.quota = ocs.UserQuota('')

    def tearDown(self):
        self.quota = None

    def test___init__0(self):
        self.assertEqual(self.quota.quota, -3)
        self.assertEqual(self.quota.used, 0)


class TestBackendCapabilities(unittest.TestCase):
    def setUp(self):
        self.bc = ocs.BackendCapabilities(setDisplayName=1, setPassword=1)

    def tearDown(self):
        self.bc = None

    def test___init__0(self):
        self.assertTrue(self.bc.set_display_name)
        self.assertTrue(self.bc.set_password)

    def test___str__0(self):
        self.assertEqual(str(self.bc), TEST_STR_BACKENDCAPABILITIES)


class TestBackendCapabilities2(unittest.TestCase):
    def setUp(self):
        self.bc = ocs.BackendCapabilities()

    def tearDown(self):
        self.bc = None

    def test___init__0(self):
        self.assertFalse(self.bc.set_display_name)
        self.assertFalse(self.bc.set_password)

    def test___str__0(self):
        self.assertEqual(str(self.bc), TEST_STR_BACKENDCAPABILITIES_2)


class TestOcsXmlResponse(unittest.TestCase):
    def setUp(self):
        self.resp = TEST_XML_RESPONSE_OK
        self.resp2 = TEST_XML_RESPONSE_FAILURE

    def tearDown(self):
        self.resp = None
        self.resp2 = None

    def test__init__0(self):
        self.assertRaises(
            WrongParam,
            ocs.OcsXmlResponse,
            self.resp,
            data_class_name="WrongClassName",
        )

    def test__init__1(self):
        self.assertRaises(WrongParam, ocs.OcsXmlResponse, "")

    def test__init__2(self):
        self.assertRaises(WrongParam, ocs.OcsXmlResponse, 555)

    def test__init__3(self):
        rsp = ocs.OcsXmlResponse(self.resp)
        self.assertEqual(rsp.status, "ok")
        self.assertEqual(rsp.statuscode, "100")
        self.assertEqual(rsp.message, "OK")

    def test__init__4(self):
        rsp = ocs.OcsXmlResponse(self.resp2)
        self.assertEqual(rsp.status, "failure")
        self.assertEqual(rsp.statuscode, "997")
        self.assertEqual(rsp.message, "Current user is not logged in")

    def test_get_status(self):
        rsp = ocs.OcsXmlResponse(self.resp2)
        self.assertEqual(
            rsp.get_status(),
            "Status: failure, code: 997, message: Current user is not logged in",
        )


class TestOcsXmlResponseGroupFolder(unittest.TestCase):
    def setUp(self):
        self.resp = TEST_XML_RESPONSE_GROUPFOLDERS
        self.obj = ocs.OcsXmlResponse(self.resp, data_class_name="GroupFolder")

    def tearDown(self):
        self.resp = None
        self.obj = None

    def test__init__0(self):
        gf1 = ocs.GroupFolder(
            id="1",
            mount_point="{IT}",
            groups=[ocs.Group(group_id="IT", permissions=PERMISSION_ALL)],
            quota="-3",
            size="39136618129",
        )
        gf2 = ocs.GroupFolder(
            id="2",
            mount_point="{FIS}",
            groups=[ocs.Group(group_id="FIS", permissions=PERMISSION_ALL)],
            quota="32212254720",
            size="11052652856",
        )
        gf3 = ocs.GroupFolder(
            id="19",
            mount_point="{SECURITY}",
            groups=[
                ocs.Group(group_id="SECURITY", permissions=PERMISSION_ALL)
            ],
            quota="21474836480",
            size="6834174935",
        )
        gf4 = ocs.GroupFolder(
            id="22",
            mount_point="{TEST_NC1}",
            groups=[
                ocs.Group(group_id="TEST_NC1", permissions=PERMISSION_ALL)
            ],
            quota="8589934592",
            size="113153",
        )

        self.assertEqual(self.obj.status, "ok")
        self.assertEqual(self.obj.statuscode, "100")
        self.assertEqual(self.obj.message, "OK")
        self.assertListEqual(self.obj.data, [gf1, gf2, gf3, gf4])

    def test__str__(self):
        st = TEST_STR_GROUPFOLDERS
        self.assertEqual(str(self.obj), st)


class TestOcsXmlResponseGroup(unittest.TestCase):
    def setUp(self):
        self.resp = TEST_XML_RESPONSE_GROUPS
        self.obj = ocs.OcsXmlResponse(self.resp, data_class_name="Group")

    def tearDown(self):
        self.resp = None
        self.obj = None

    def test__init__0(self):
        g1 = ocs.Group(group_id="FIS")
        g2 = ocs.Group(group_id="IT")
        g3 = ocs.Group(group_id="PHD")
        g4 = ocs.Group(group_id="SECURITY")
        g5 = ocs.Group(group_id="TEST_NC1")
        self.assertEqual(self.obj.status, "ok")
        self.assertEqual(self.obj.statuscode, "100")
        self.assertEqual(self.obj.message, "OK")
        self.assertListEqual(self.obj.data, [g1, g2, g3, g4, g5])

    def test__str__(self):
        self.assertEqual(str(self.obj), TEST_STR_GROUPS)


class TestOcsXmlResponseCreateGroupFolder(unittest.TestCase):
    def setUp(self):
        self.resp = TEST_XML_RESPONSE_CTEATE_GROUPFOLDER
        self.obj = ocs.OcsXmlResponse(self.resp, data_class_name="CreateGroupFolder")

    def tearDown(self):
        self.resp = None
        self.obj = None

    def test__init__0(self):
        cgf = ocs.CreateGroupFolder(id="13")
        self.assertEqual(self.obj.status, "ok")
        self.assertEqual(self.obj.statuscode, "100")
        self.assertEqual(self.obj.message, "OK")
        self.assertListEqual(self.obj.data, [cgf])

    def test__str__(self):
        self.assertEqual(str(self.obj), TEST_STR_CREATE_GROUPFOLDER)


class TestOcsXmlResponseGroupMembers(unittest.TestCase):
    def setUp(self):
        self.resp = TEST_XML_RESPONSE_GROUP_MEMBERS
        self.obj = ocs.OcsXmlResponse(self.resp, data_class_name="GroupMembers")

    def tearDown(self):
        self.resp = None
        self.obj = None

    def test__init__0(self):
        u1 = ocs.GroupMembers(user_id="tester1@example.com")
        u2 = ocs.GroupMembers(user_id="tester2@example.com")
        u3 = ocs.GroupMembers(user_id="tester3@example.com")
        u4 = ocs.GroupMembers(user_id="tester4@example.com")
        u5 = ocs.GroupMembers(user_id="tester5@example.com")

        self.assertEqual(self.obj.status, "ok")
        self.assertEqual(self.obj.statuscode, "100")
        self.assertEqual(self.obj.message, "OK")
        self.assertListEqual(self.obj.data, [u1, u2, u3, u4, u5])

    def test__str__(self):
        self.assertEqual(str(self.obj), TEST_STR_GROUP_MEMBERS)


class TestOcsXmlResponseGroupFolder2(unittest.TestCase):
    def setUp(self):
        self.resp = TEST_XML_RESPONSE_CTEATE_GROUPFOLDER
        self.obj = ocs.OcsXmlResponse(self.resp, data_class_name="GroupFolder")

    def tearDown(self):
        self.resp = None
        self.obj = None

    def test__init__0(self):
        gf1 = ocs.GroupFolder(id="13")
        self.assertEqual(self.obj.status, "ok")
        self.assertEqual(self.obj.statuscode, "100")
        self.assertEqual(self.obj.message, "OK")
        self.assertListEqual(self.obj.data, [gf1])

    def test__str__(self):
        self.assertEqual(str(self.obj), TEST_STR_GROUPFOLDER_2)


class TestOcsXmlResponseUser(unittest.TestCase):
    def setUp(self):
        self.resp = TEST_XML_RESPONSE_USER
        self.obj = ocs.OcsXmlResponse(self.resp, data_class_name="User")

    def tearDown(self):
        self.resp = None
        self.obj = None

    def test__init__0(self):
        user1 = ocs.User(
            id="tester1@example.com",
            enabled="1",
            storageLocation="/home/nextcloud/tester1@example.com",
            lastLogin="1544530113000",
            backend="LDAP",
            subadmin=["testers"],
            quota=ocs.UserQuota(
                quota="10737418240",
                used="2431492563",
                free="8305925677",
                total="10737418240",
                relative="22.65",
            ),
            email=None,
            displayname="Пупкин Василий Алибабаевич",
            phone="+3333333333",
            address="Russia, St. Petersburg",
            website="https://www.example.com",
            twitter="@_twitt_me_",
            groups=[ocs.Group("testers"), ocs.Group("staff")],
            language="ru",
            locale=None,
            backendCapabilities=ocs.BackendCapabilities(
                setDisplayName=None, setPassword=None
            ),
        )

        self.assertEqual(self.obj.status, "ok")
        self.assertEqual(self.obj.statuscode, "100")
        self.assertEqual(self.obj.message, "OK")
        self.assertListEqual(self.obj.data, [user1])

    def test__str__(self):
        self.assertEqual(str(self.obj), TEST_STR_USER_DETAILS)


class TestOcsXmlResponseApps(unittest.TestCase):
    def setUp(self):
        self.resp = TEST_XML_RESPONSE_APP_LDAP
        self.obj = ocs.OcsXmlResponse(self.resp, data_class_name="Apps")

    def tearDown(self):
        self.resp = None
        self.obj = None

    def test__init__0(self):
        self.assertEqual(self.obj.status, "ok")
        self.assertEqual(self.obj.statuscode, "100")
        self.assertEqual(self.obj.message, "OK")
        self.assertListEqual(self.obj.data, TEST_LIST_APPS)

    def test__str__(self):
        self.assertEqual(str(self.obj), TEST_STR_APPS)


class TestOcsXmlResponseSubadmins(unittest.TestCase):
    def setUp(self):
        self.resp = TEST_XML_RESPONSE_SUBADMINS
        self.obj = ocs.OcsXmlResponse(self.resp, data_class_name="Subadmins")

    def tearDown(self):
        self.resp = None
        self.obj = None

    def test__init__0(self):
        admins = ["admin@example.com", "admin2@example.com"]
        self.assertEqual(self.obj.status, "ok")
        self.assertEqual(self.obj.statuscode, "100")
        self.assertEqual(self.obj.message, "OK")
        self.assertListEqual(self.obj.data, admins)

    def test__str__(self):
        self.assertEqual(str(self.obj), TEST_STR_SUBADMINS)


class Ocs0(unittest.TestCase):
    def test__init__0(self):
        self.assertRaises(
            OperationFailure,
            ocs.Ocs,
            cloud_user=None,
            cloud_user_pwd=None,
            cloud_URL=None,
        )

    def test__init__1(self):
        self.assertRaises(
            OperationFailure,
            ocs.Ocs,
            cloud_user="admin",
            cloud_user_pwd=None,
            cloud_URL=None,
        )

    def test__init__2(self):
        self.assertRaises(
            OperationFailure,
            ocs.Ocs,
            cloud_user="admin",
            cloud_user_pwd="passwd",
            cloud_URL=None,
        )

    @responses.activate
    def test__init__3(self):
        payload = TEST_XML_RESPONSE_APP_LDAP
        responses.add(
            responses.GET,
            "https://cloud.example.com/ocs/v1.php/cloud/apps",
            body=payload,
        )
        self.ocs_inst = ocs.Ocs(
            cloud_user="admin",
            cloud_user_pwd="passwd",
            cloud_URL="https://cloud.example.com",
        )
        self.assertEqual(self.ocs_inst.cl_user, "admin")
        self.assertEqual(self.ocs_inst.cl_user_pwd, "passwd")
        self.assertEqual(
            self.ocs_inst.cloud_url, urlparse("https://cloud.example.com")
        )
        self.assertDictEqual(self.ocs_inst.headers, {"OCS-APIRequest": "true"})
        self.assertListEqual(self.ocs_inst._apps, TEST_LIST_APPS_OCS)
        self.assertEqual(self.ocs_inst.__class__.__name__, "OcsMix")

    def test__init__4(self):
        self.assertRaises(
            OperationFailure,
            ocs.Ocs,
            cloud_user="admin",
            cloud_user_pwd="passwd",
            cloud_URL="https://cloud.example.com",
        )

    @responses.activate
    def test__get_apps_failed(self):
        payload = TEST_XML_RESPONSE_FAILURE
        responses.add(
            responses.GET,
            "https://cloud.example.com/ocs/v1.php/cloud/apps",
            body=payload,
        )
        self.assertRaises(
            OperationFailure,
            ocs.Ocs,
            cloud_user="admin",
            cloud_user_pwd="passwd",
            cloud_URL="https://cloud.example.com",
        )

    @responses.activate
    def test__get_groups(self):
        responses.add(
            responses.GET,
            "https://cloud.example.com/ocs/v1.php/cloud/apps",
            body=TEST_XML_RESPONSE_APP_LDAP,
        )
        responses.add(
            responses.GET,
            "https://cloud.example.com/ocs/v1.php/cloud/groups",
            body=TEST_XML_RESPONSE_GROUPS,
        )
        ocs_inst = ocs.Ocs(
            cloud_user="admin",
            cloud_user_pwd="passwd",
            cloud_URL="https://cloud.example.com",
        )
        groups = ocs_inst.get_groups()
        group_1 = ocs.Group(group_id="FIS")
        group_2 = ocs.Group(group_id="IT")
        group_3 = ocs.Group(group_id="PHD")
        group_4 = ocs.Group(group_id="SECURITY")
        group_5 = ocs.Group(group_id="TEST_NC1")
        self.assertListEqual(
            groups,
            [group_1, group_2, group_3, group_4, group_5]
        )

    @responses.activate
    def test__get_groups_failed(self):
        responses.add(
            responses.GET,
            "https://cloud.example.com/ocs/v1.php/cloud/apps",
            body=TEST_XML_RESPONSE_APP_LDAP,
        )
        responses.add(
            responses.GET,
            "https://cloud.example.com/ocs/v1.php/cloud/groups",
            body=TEST_XML_RESPONSE_FAILURE,
        )
        ocs_inst = ocs.Ocs(
            cloud_user="admin",
            cloud_user_pwd="passwd",
            cloud_URL="https://cloud.example.com",
        )
        self.assertRaises(
            OperationFailure,
            ocs_inst.get_groups,
        )

if __name__ == "__main__":
    unittest.main()
