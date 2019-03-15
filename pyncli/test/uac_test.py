# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        uac_test
# Purpose:      tests
#
# Author:      Evgeniy Semenov
#
# Created:     08.02.2017
# Copyright:   (c) Evgeniy Semenov 2017-2019
# Licence:     MIT
#-------------------------------------------------------------------------------

import unittest
import os


pd=os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) )
os.sys.path.insert(0,pd)
from pyncli.ldap.uac import uac

class TestUacMetods(unittest.TestCase):

    def test___flag_TRUSTED_FOR_DELEGATION(self):
    	self.assertEqual(uac.TRUSTED_FOR_DELEGATION.value,0x80000)

    def test___flag_not_TRUSTED_FOR_DELEGATION(self):
    	self.assertNotEqual(uac.TRUSTED_FOR_DELEGATION.value,0x08000)

    def test___flag_ENCRYPTED_TEXT_PWD_ALLOWED(self):
    	self.assertEqual(uac.ENCRYPTED_TEXT_PWD_ALLOWED.value,0x0080)

    def test___flag_HOMEDIR_REQUIRED(self):
    	self.assertEqual(uac.HOMEDIR_REQUIRED.value,0x0008)

    def test___flag_WORKSTATION_TRUST_ACCOUNT(self):
    	self.assertEqual(uac.WORKSTATION_TRUST_ACCOUNT.value,0x1000)

    def test___flag_INTERDOMAIN_TRUST_ACCOUNT(self):
    	self.assertEqual(uac.INTERDOMAIN_TRUST_ACCOUNT.value,0x0800)

    def test___flag_SCRIPT(self):
    	self.assertEqual(uac.SCRIPT.value,0x0001)

    def test___flag_not_SCRIPT(self):
    	self.assertNotEqual(uac.SCRIPT.value,0x00010)


    def test___flag_MNS_LOGON_ACCOUNT(self):
    	self.assertEqual(uac.MNS_LOGON_ACCOUNT.value,0x20000)

    def test___flag_TRUSTED_TO_AUTH_FOR_DELEGATION(self):
    	self.assertEqual(uac.TRUSTED_TO_AUTH_FOR_DELEGATION.value,0x1000000)

    def test___flag_PASSWD_CANT_CHANGE(self):
    	self.assertEqual(uac.PASSWD_CANT_CHANGE.value,0x0040)

    def test___flag_SMARTCARD_REQUIRED(self):
    	self.assertEqual(uac.SMARTCARD_REQUIRED.value,0x40000)

    def test___flag_SERVER_TRUST_ACCOUNT(self):
    	self.assertEqual(uac.SERVER_TRUST_ACCOUNT.value,0x2000)

    def test___flag_PASSWORD_EXPIRED(self):
    	self.assertEqual(uac.PASSWORD_EXPIRED.value,0x800000)

    def test___flag_PASSWD_NOTREQD(self):
    	self.assertEqual(uac.PASSWD_NOTREQD.value,0x0020)

    def test___flag_DONT_EXPIRE_PASSWORD(self):
    	self.assertEqual(uac.DONT_EXPIRE_PASSWORD.value,0x10000)

    def test___flag_LOCKOUT(self):
    	self.assertEqual(uac.LOCKOUT.value,0x0010)

    def test___flag_ACCOUNTDISABLE(self):
    	self.assertEqual(uac.ACCOUNTDISABLE.value,0x0002)

    def test___flag_not_ACCOUNTDISABLE(self):
    	self.assertNotEqual(uac.ACCOUNTDISABLE.value,0x0003)

    def test___flag_NORMAL_ACCOUNT(self):
    	self.assertEqual(uac.NORMAL_ACCOUNT.value,0x0200)

    def test___flag_NOT_DELEGATED(self):
    	self.assertEqual(uac.NOT_DELEGATED.value,0x100000)

    def test___flag_DONT_REQ_PREAUTH(self):
    	self.assertEqual(uac.DONT_REQ_PREAUTH.value,0x400000)

    def test___flag_USE_DES_KEY_ONLY(self):
    	self.assertEqual(uac.USE_DES_KEY_ONLY.value,0x200000)

    def test___flag_TEMP_DUPLICATE_ACCOUNT(self):
    	self.assertEqual(uac.TEMP_DUPLICATE_ACCOUNT.value,0x0100)




    def test___hex_TRUSTED_FOR_DELEGATION(self):
        self.assertEqual(int(uac.TRUSTED_FOR_DELEGATION.hex,16),0x80000)

    def test___hex_ENCRYPTED_TEXT_PWD_ALLOWED(self):
        self.assertEqual(int(uac.ENCRYPTED_TEXT_PWD_ALLOWED.hex,16),0x0080)

    def test___hex_HOMEDIR_REQUIRED(self):
        self.assertEqual(int(uac.HOMEDIR_REQUIRED.hex,16),0x0008)

    def test___hex_WORKSTATION_TRUST_ACCOUNT(self):
        self.assertEqual(int(uac.WORKSTATION_TRUST_ACCOUNT.hex,16),0x1000)

    def test___hex_INTERDOMAIN_TRUST_ACCOUNT(self):
        self.assertEqual(int(uac.INTERDOMAIN_TRUST_ACCOUNT.hex,16),0x0800)

    def test___hex_SCRIPT(self):
        self.assertEqual(int(uac.SCRIPT.hex,16),0x0001)

    def test___hex_MNS_LOGON_ACCOUNT(self):
        self.assertEqual(int(uac.MNS_LOGON_ACCOUNT.hex,16),0x20000)

    def test___hex_TRUSTED_TO_AUTH_FOR_DELEGATION(self):
        self.assertEqual(int(uac.TRUSTED_TO_AUTH_FOR_DELEGATION.hex,16),0x1000000)

    def test___hex_PASSWD_CANT_CHANGE(self):
        self.assertEqual(int(uac.PASSWD_CANT_CHANGE.hex,16),0x0040)

    def test___hex_not_PASSWD_CANT_CHANGE(self):
        self.assertNotEqual(int(uac.PASSWD_CANT_CHANGE.hex,16),0x0044)

    def test___hex_SMARTCARD_REQUIRED(self):
        self.assertEqual(int(uac.SMARTCARD_REQUIRED.hex,16),0x40000)

    def test___hex_SERVER_TRUST_ACCOUNT(self):
        self.assertEqual(int(uac.SERVER_TRUST_ACCOUNT.hex,16),0x2000)

    def test___hex_PASSWORD_EXPIRED(self):
        self.assertEqual(int(uac.PASSWORD_EXPIRED.hex,16),0x800000)

    def test___hex_PASSWD_NOTREQD(self):
        self.assertEqual(int(uac.PASSWD_NOTREQD.hex,16),0x0020)

    def test___hex_DONT_EXPIRE_PASSWORD(self):
        self.assertEqual(int(uac.DONT_EXPIRE_PASSWORD.hex,16),0x10000)

    def test___hex_LOCKOUT(self):
        self.assertEqual(int(uac.LOCKOUT.hex,16),0x0010)

    def test___hex_ACCOUNTDISABLE(self):
        self.assertEqual(int(uac.ACCOUNTDISABLE.hex,16),0x0002)

    def test___hex_NORMAL_ACCOUNT(self):
        self.assertEqual(int(uac.NORMAL_ACCOUNT.hex,16),0x0200)

    def test___hex_not_NORMAL_ACCOUNT(self):
        self.assertNotEqual(int(uac.NORMAL_ACCOUNT.hex,16),0x0001)

    def test___hex_NOT_DELEGATED(self):
        self.assertEqual(int(uac.NOT_DELEGATED.hex,16),0x100000)

    def test___hex_DONT_REQ_PREAUTH(self):
        self.assertEqual(int(uac.DONT_REQ_PREAUTH.hex,16),0x400000)

    def test___hex_USE_DES_KEY_ONLY(self):
        self.assertEqual(int(uac.USE_DES_KEY_ONLY.hex,16),0x200000)

    def test___hex_TEMP_DUPLICATE_ACCOUNT(self):
        self.assertEqual(int(uac.TEMP_DUPLICATE_ACCOUNT.hex,16),0x0100)


    def test___val_TRUSTED_FOR_DELEGATION(self):
        self.assertEqual(uac.TRUSTED_FOR_DELEGATION.val,0x80000)

    def test___val_ENCRYPTED_TEXT_PWD_ALLOWED(self):
        self.assertEqual(uac.ENCRYPTED_TEXT_PWD_ALLOWED.val,0x0080)

    def test___val_HOMEDIR_REQUIRED(self):
        self.assertEqual(uac.HOMEDIR_REQUIRED.val,0x0008)

    def test___val_WORKSTATION_TRUST_ACCOUNT(self):
        self.assertEqual(uac.WORKSTATION_TRUST_ACCOUNT.val,0x1000)

    def test___val_INTERDOMAIN_TRUST_ACCOUNT(self):
        self.assertEqual(uac.INTERDOMAIN_TRUST_ACCOUNT.val,0x0800)

    def test___val_SCRIPT(self):
        self.assertEqual(uac.SCRIPT.val,0x0001)

    def test___val_MNS_LOGON_ACCOUNT(self):
        self.assertEqual(uac.MNS_LOGON_ACCOUNT.val,0x20000)

    def test___val_not_MNS_LOGON_ACCOUNT(self):
        self.assertNotEqual(uac.MNS_LOGON_ACCOUNT.val,0x30000)

    def test___val_TRUSTED_TO_AUTH_FOR_DELEGATION(self):
        self.assertEqual(uac.TRUSTED_TO_AUTH_FOR_DELEGATION.val,0x1000000)

    def test___val_PASSWD_CANT_CHANGE(self):
        self.assertEqual(uac.PASSWD_CANT_CHANGE.val,0x0040)

    def test___val_SMARTCARD_REQUIRED(self):
        self.assertEqual(uac.SMARTCARD_REQUIRED.val,0x40000)

    def test___val_SERVER_TRUST_ACCOUNT(self):
        self.assertEqual(uac.SERVER_TRUST_ACCOUNT.val,0x2000)

    def test___val_PASSWORD_EXPIRED(self):
        self.assertEqual(uac.PASSWORD_EXPIRED.val,0x800000)

    def test___val_PASSWD_NOTREQD(self):
        self.assertEqual(uac.PASSWD_NOTREQD.val,0x0020)

    def test___val_DONT_EXPIRE_PASSWORD(self):
        self.assertEqual(uac.DONT_EXPIRE_PASSWORD.val,0x10000)

    def test___val_LOCKOUT(self):
        self.assertEqual(uac.LOCKOUT.val,0x0010)

    def test___val_ACCOUNTDISABLE(self):
        self.assertEqual(uac.ACCOUNTDISABLE.val,0x0002)

    def test___val_NORMAL_ACCOUNT(self):
        self.assertEqual(uac.NORMAL_ACCOUNT.val,0x0200)

    def test___val_NOT_DELEGATED(self):
        self.assertEqual(uac.NOT_DELEGATED.val,0x100000)

    def test___val_DONT_REQ_PREAUTH(self):
        self.assertEqual(uac.DONT_REQ_PREAUTH.val,0x400000)

    def test___val_USE_DES_KEY_ONLY(self):
        self.assertEqual(uac.USE_DES_KEY_ONLY.val,0x200000)

    def test___val_not_USE_DES_KEY_ONLY(self):
        self.assertNotEqual(uac.USE_DES_KEY_ONLY.val,0x200002)

    def test___val_TEMP_DUPLICATE_ACCOUNT(self):
        self.assertEqual(uac.TEMP_DUPLICATE_ACCOUNT.val,0x0100)



    def test___add_1(self):
        self.assertEqual(uac.TRUSTED_FOR_DELEGATION + uac.NORMAL_ACCOUNT,0x80000+0x0200)

    def test___add_2(self):
        self.assertEqual(uac.ENCRYPTED_TEXT_PWD_ALLOWED + uac.NORMAL_ACCOUNT,0x0080+0x0200)

    def test___add_3(self):
        self.assertEqual(uac.HOMEDIR_REQUIRED + uac.ACCOUNTDISABLE,0x0008+0x0002)

    def test___add_4(self):
        self.assertEqual(uac.WORKSTATION_TRUST_ACCOUNT + uac.PASSWD_NOTREQD,0x1000+0x0020)

    def test___add_5(self):
        self.assertEqual(uac.INTERDOMAIN_TRUST_ACCOUNT + uac.SCRIPT,0x0800+0x0001)

    def test___add_6(self):
        self.assertEqual(uac.SCRIPT + uac.NORMAL_ACCOUNT,0x0001+0x0200)

    def test___add_7(self):
        self.assertEqual(uac.MNS_LOGON_ACCOUNT + uac.NORMAL_ACCOUNT,0x20000+0x0200)

    def test___add_8(self):
        self.assertEqual(uac.TRUSTED_TO_AUTH_FOR_DELEGATION + uac.WORKSTATION_TRUST_ACCOUNT,0x1000000+0x1000)

    def test___add_9(self):
        self.assertEqual(uac.PASSWD_CANT_CHANGE + uac.NOT_DELEGATED,0x0040+0x100000)

    def test___add_10(self):
        self.assertEqual(uac.SMARTCARD_REQUIRED + uac.HOMEDIR_REQUIRED,0x40000+0x0008)

    def test___add_not_10(self):
        self.assertNotEqual(uac.SMARTCARD_REQUIRED + uac.HOMEDIR_REQUIRED,0x40000+0x0004)

    def test___add_11(self):
        self.assertEqual(uac.SERVER_TRUST_ACCOUNT + uac.DONT_REQ_PREAUTH,0x2000+0x400000)

    def test___add_12(self):
        self.assertEqual(uac.PASSWORD_EXPIRED + uac.HOMEDIR_REQUIRED,0x800000+0x0008)

    def test___add_13(self):
        self.assertEqual(uac.PASSWD_NOTREQD + uac.NORMAL_ACCOUNT,0x0020+0x0200)

    def test___add_14(self):
        self.assertEqual(uac.DONT_EXPIRE_PASSWORD + uac.HOMEDIR_REQUIRED,0x10000+0x0008)

    def test___add_15(self):
        self.assertEqual(uac.LOCKOUT + uac.HOMEDIR_REQUIRED,0x0010+0x0008)

    def test___add_16(self):
        self.assertEqual(uac.ACCOUNTDISABLE + uac.TRUSTED_FOR_DELEGATION,0x0002+0x80000)

    def test___add_17(self):
        self.assertEqual(uac.NORMAL_ACCOUNT + uac.TRUSTED_TO_AUTH_FOR_DELEGATION,0x0200+0x1000000)

    def test___add_18(self):
        self.assertEqual(uac.NOT_DELEGATED + uac.ENCRYPTED_TEXT_PWD_ALLOWED,0x100000+0x0080)

    def test___add_19(self):
        self.assertEqual(uac.DONT_REQ_PREAUTH + uac.DONT_EXPIRE_PASSWORD,0x400000+0x10000)

    def test___add_20(self):
        self.assertEqual(uac.USE_DES_KEY_ONLY + uac.SCRIPT,0x200000+0x0001)

    def test___add_not_20(self):
        self.assertNotEqual(uac.USE_DES_KEY_ONLY + uac.SCRIPT,0x200000+0x00011)

    def test___add_21(self):
        self.assertEqual(uac.TEMP_DUPLICATE_ACCOUNT + uac.TRUSTED_TO_AUTH_FOR_DELEGATION,0x0100+0x1000000)

    def test___add_22(self):
        self.assertEqual(uac.SMARTCARD_REQUIRED + uac.SMARTCARD_REQUIRED,0x40000)

    def test___add_23(self):
        self.assertEqual(uac.ACCOUNTDISABLE + uac.ACCOUNTDISABLE,0x0002)

    def test___add2_1(self):
        self.assertNotEqual(uac.TRUSTED_FOR_DELEGATION + uac.INTERDOMAIN_TRUST_ACCOUNT + uac.INTERDOMAIN_TRUST_ACCOUNT,0x80000+0x0800+0x0800)

    def test___add2_2(self):
        self.assertEqual(uac.ENCRYPTED_TEXT_PWD_ALLOWED + uac.DONT_REQ_PREAUTH + uac.PASSWORD_EXPIRED,0x0080+0x400000+0x800000)

    def test___add2_3(self):
        self.assertEqual(uac.HOMEDIR_REQUIRED + uac.SMARTCARD_REQUIRED + uac.NOT_DELEGATED,0x0008+0x40000+0x100000)

    def test___add2_4(self):
        self.assertEqual(uac.WORKSTATION_TRUST_ACCOUNT + uac.TEMP_DUPLICATE_ACCOUNT + uac.USE_DES_KEY_ONLY,0x1000+0x0100+0x200000)

    def test___add2_5(self):
        self.assertEqual(uac.INTERDOMAIN_TRUST_ACCOUNT + uac.WORKSTATION_TRUST_ACCOUNT + uac.NOT_DELEGATED,0x0800+0x1000+0x100000)

    def test___add2_6(self):
        self.assertEqual(uac.SCRIPT + uac.NOT_DELEGATED + uac.INTERDOMAIN_TRUST_ACCOUNT,0x0001+0x100000+0x0800)

    def test___add2_not_6(self):
        self.assertNotEqual(uac.SCRIPT + uac.NOT_DELEGATED + uac.INTERDOMAIN_TRUST_ACCOUNT,0x0002+0x100000+0x0800)

    def test___add2_7(self):
        self.assertEqual(uac.MNS_LOGON_ACCOUNT + uac.DONT_EXPIRE_PASSWORD + uac.TRUSTED_FOR_DELEGATION,0x20000+0x10000+0x80000)

    def test___add2_8(self):
        self.assertEqual(uac.TRUSTED_TO_AUTH_FOR_DELEGATION + uac.ENCRYPTED_TEXT_PWD_ALLOWED + uac.ACCOUNTDISABLE,0x1000000+0x0080+0x0002)

    def test___add2_9(self):
        self.assertEqual(uac.PASSWD_CANT_CHANGE + uac.PASSWORD_EXPIRED + uac.TRUSTED_FOR_DELEGATION,0x0040+0x800000+0x80000)

    def test___add2_10(self):
        self.assertEqual(uac.SMARTCARD_REQUIRED + uac.INTERDOMAIN_TRUST_ACCOUNT + uac.TRUSTED_TO_AUTH_FOR_DELEGATION,0x40000+0x0800+0x1000000)

    def test___add2_11(self):
        self.assertEqual(uac.SERVER_TRUST_ACCOUNT + uac.NORMAL_ACCOUNT + uac.WORKSTATION_TRUST_ACCOUNT,0x2000+0x0200+0x1000)

    def test___add2_12(self):
        self.assertEqual(uac.PASSWORD_EXPIRED + uac.LOCKOUT + uac.TEMP_DUPLICATE_ACCOUNT,0x800000+0x0010+0x0100)

    def test___add2_13(self):
        self.assertEqual(uac.PASSWD_NOTREQD + uac.TEMP_DUPLICATE_ACCOUNT + uac.USE_DES_KEY_ONLY,0x0020+0x0100+0x200000)

    def test___add2_not_13(self):
        self.assertNotEqual(uac.PASSWD_NOTREQD + uac.LOCKOUT + uac.USE_DES_KEY_ONLY,0x0020+0x0100+0x200000)

    def test___add2_14(self):
        self.assertEqual(uac.DONT_EXPIRE_PASSWORD + uac.DONT_REQ_PREAUTH + uac.WORKSTATION_TRUST_ACCOUNT,0x10000+0x400000+0x1000)

    def test___add2_15(self):
        self.assertEqual(uac.LOCKOUT + uac.TRUSTED_TO_AUTH_FOR_DELEGATION + uac.TRUSTED_TO_AUTH_FOR_DELEGATION,0x0010+0x1000000)

    def test___add2_16(self):
        self.assertEqual(uac.ACCOUNTDISABLE + uac.INTERDOMAIN_TRUST_ACCOUNT + uac.LOCKOUT,0x0002+0x0800+0x0010)

    def test___add2_17(self):
        self.assertEqual(uac.NORMAL_ACCOUNT + uac.SCRIPT + uac.NOT_DELEGATED,0x0200+0x0001+0x100000)

    def test___add2_18(self):
        self.assertEqual(uac.NOT_DELEGATED + uac.SMARTCARD_REQUIRED + uac.TEMP_DUPLICATE_ACCOUNT,0x100000+0x40000+0x0100)

    def test___add2_19(self):
        self.assertEqual(uac.DONT_REQ_PREAUTH + uac.LOCKOUT + uac.TRUSTED_TO_AUTH_FOR_DELEGATION,0x400000+0x0010+0x1000000)

    def test___add2_20(self):
        self.assertEqual(uac.USE_DES_KEY_ONLY + uac.SCRIPT + uac.INTERDOMAIN_TRUST_ACCOUNT,0x200000+0x0001+0x0800)

    def test___add2_21(self):
        self.assertEqual(uac.TEMP_DUPLICATE_ACCOUNT + uac.PASSWD_CANT_CHANGE + uac.SERVER_TRUST_ACCOUNT,0x0100+0x0040+0x2000)




    def test___status_1(self):
        u=uac.get_status(0x1003000) ; u.sort()
        self.assertListEqual(u,['SERVER_TRUST_ACCOUNT', 'TRUSTED_TO_AUTH_FOR_DELEGATION', 'WORKSTATION_TRUST_ACCOUNT'])

    def test___status_2(self):
        u=uac.get_status(0x140040) ; u.sort()
        self.assertListEqual(u,['NOT_DELEGATED', 'PASSWD_CANT_CHANGE', 'SMARTCARD_REQUIRED'])

    def test___status_3(self):
        u=uac.get_status(0x41040) ; u.sort()
        self.assertListEqual(u,['PASSWD_CANT_CHANGE', 'SMARTCARD_REQUIRED', 'WORKSTATION_TRUST_ACCOUNT'])

    def test___status_4(self):
        u=uac.get_status(0x82002) ; u.sort()
        self.assertListEqual(u,['ACCOUNTDISABLE', 'SERVER_TRUST_ACCOUNT', 'TRUSTED_FOR_DELEGATION'])

    def test___status_5(self):
        u=uac.get_status(0x1000208) ; u.sort()
        self.assertListEqual(u,['HOMEDIR_REQUIRED', 'NORMAL_ACCOUNT', 'TRUSTED_TO_AUTH_FOR_DELEGATION'])

    def test___status_6(self):
        u=uac.get_status(0x222) ; u.sort()
        self.assertListEqual(u,['ACCOUNTDISABLE', 'NORMAL_ACCOUNT', 'PASSWD_NOTREQD'])

    def test___status_7(self):
        u=uac.get_status(0x210010) ; u.sort()
        self.assertListEqual(u,['DONT_EXPIRE_PASSWORD', 'LOCKOUT', 'USE_DES_KEY_ONLY'])

    def test___status_8(self):
        u=uac.get_status(0x1000a00) ; u.sort()
        self.assertListEqual(u,['INTERDOMAIN_TRUST_ACCOUNT', 'NORMAL_ACCOUNT', 'TRUSTED_TO_AUTH_FOR_DELEGATION'])

    def test___status_9(self):
        u=uac.get_status(0x820800) ; u.sort()
        self.assertListEqual(u,['INTERDOMAIN_TRUST_ACCOUNT', 'MNS_LOGON_ACCOUNT', 'PASSWORD_EXPIRED'])

    def test___status_10(self):
        u=uac.get_status(0x20060) ; u.sort()
        self.assertListEqual(u,['MNS_LOGON_ACCOUNT', 'PASSWD_CANT_CHANGE', 'PASSWD_NOTREQD'])

    def test___status_11(self):
        u=uac.get_status(0x800101) ; u.sort()
        self.assertListEqual(u,['PASSWORD_EXPIRED', 'SCRIPT', 'TEMP_DUPLICATE_ACCOUNT'])

    def test___status_12(self):
        u=uac.get_status(0x401000) ; u.sort()
        self.assertListEqual(u,['DONT_REQ_PREAUTH', 'WORKSTATION_TRUST_ACCOUNT'])

    def test___status_13(self):
        u=uac.get_status(0x610000) ; u.sort()
        self.assertListEqual(u,['DONT_EXPIRE_PASSWORD', 'DONT_REQ_PREAUTH', 'USE_DES_KEY_ONLY'])

    def test___status_14(self):
        u=uac.get_status(0x40120) ; u.sort()
        self.assertListEqual(u,['PASSWD_NOTREQD', 'SMARTCARD_REQUIRED', 'TEMP_DUPLICATE_ACCOUNT'])

    def test___status_15(self):
        u=uac.get_status(0x500200) ; u.sort()
        self.assertListEqual(u,['DONT_REQ_PREAUTH', 'NORMAL_ACCOUNT', 'NOT_DELEGATED'])

    def test___status_16(self):
        u=uac.get_status(0x810200) ; u.sort()
        self.assertListEqual(u,['DONT_EXPIRE_PASSWORD', 'NORMAL_ACCOUNT', 'PASSWORD_EXPIRED'])

    def test___status_17(self):
        u=uac.get_status(0x840000) ; u.sort()
        self.assertListEqual(u,['PASSWORD_EXPIRED', 'SMARTCARD_REQUIRED'])

    def test___status_not_17(self):
        u=uac.get_status(0x440000) ; u.sort()
        self.assertNotEqual(u,['PASSWORD_EXPIRED', 'SMARTCARD_REQUIRED'])


    def test___status_18(self):
        u=uac.get_status(0x40810) ; u.sort()
        self.assertListEqual(u,['INTERDOMAIN_TRUST_ACCOUNT', 'LOCKOUT', 'SMARTCARD_REQUIRED'])

    def test___status_19(self):
        u=uac.get_status(0x91) ; u.sort()
        self.assertListEqual(u,['ENCRYPTED_TEXT_PWD_ALLOWED', 'LOCKOUT', 'SCRIPT'])

    def test___status_20(self):
        u=uac.get_status(0x300040) ; u.sort()
        self.assertListEqual(u,['NOT_DELEGATED', 'PASSWD_CANT_CHANGE', 'USE_DES_KEY_ONLY'])

    def test___status_not_20(self):
        u=uac.get_status(0x300020) ; u.sort()
        self.assertNotEqual(u,['NOT_DELEGATED', 'PASSWD_CANT_CHANGE', 'USE_DES_KEY_ONLY'])


    def test___status_21(self):
        u=uac.get_status(0x60) ; u.sort()
        self.assertListEqual(u,['PASSWD_CANT_CHANGE', 'PASSWD_NOTREQD'])


    def test___uac_1(self):
        u=uac.get_uac(0x400000)
        self.assertListEqual(u,[uac.DONT_REQ_PREAUTH])

    def test___uac_2(self):
        u=uac.get_uac(0x0040)
        self.assertListEqual(u,[uac.PASSWD_CANT_CHANGE])

    def test___uac_3(self):
        u=uac.get_uac(0x0080)
        self.assertListEqual(u,[uac.ENCRYPTED_TEXT_PWD_ALLOWED])

    def test___uac_4(self):
        u=uac.get_uac(0x0020)
        self.assertListEqual(u,[uac.PASSWD_NOTREQD])

    def test___uac_5(self):
        u=uac.get_uac(0x400000)
        self.assertListEqual(u,[uac.DONT_REQ_PREAUTH])

    def test___uac_6(self):
        u=uac.get_uac(0x0008)
        self.assertListEqual(u,[uac.HOMEDIR_REQUIRED])

    def test___uac_7(self):
        u=uac.get_uac(0x100000)
        self.assertListEqual(u,[uac.NOT_DELEGATED])

    def test___uac_8(self):
        u=uac.get_uac(0x0100)
        self.assertListEqual(u,[uac.TEMP_DUPLICATE_ACCOUNT])

    def test___uac_9(self):
        u=uac.get_uac(0x0040)
        self.assertListEqual(u,[uac.PASSWD_CANT_CHANGE])

    def test___uac_10(self):
        u=uac.get_uac(0x100000)
        self.assertListEqual(u,[uac.NOT_DELEGATED])

    def test___uac_11(self):
        u=uac.get_uac(0x1000)
        self.assertListEqual(u,[uac.WORKSTATION_TRUST_ACCOUNT])

    def test___uac_12(self):
        u=uac.get_uac(0x100000)
        self.assertListEqual(u,[uac.NOT_DELEGATED])

    def test___uac_13(self):
        u=uac.get_uac(0x20000)
        self.assertListEqual(u,[uac.MNS_LOGON_ACCOUNT])

    def test___uac_14(self):
        u=uac.get_uac(0x0020)
        self.assertListEqual(u,[uac.PASSWD_NOTREQD])

    def test___uac_not_14(self):
        u=uac.get_uac(0x0002)
        self.assertNotEqual(u,[uac.PASSWD_NOTREQD])

    def test___uac_15(self):
        u=uac.get_uac(0x0002)
        self.assertListEqual(u,[uac.ACCOUNTDISABLE])

    def test___uac_16(self):
        u=uac.get_uac(0x2000)
        self.assertListEqual(u,[uac.SERVER_TRUST_ACCOUNT])

    def test___uac_17(self):
        u=uac.get_uac(0x0001)
        self.assertListEqual(u,[uac.SCRIPT])

    def test___uac_18(self):
        u=uac.get_uac(0x1000)
        self.assertListEqual(u,[uac.WORKSTATION_TRUST_ACCOUNT])

    def test___uac_19(self):
        u=uac.get_uac(0x80000)
        self.assertListEqual(u,[uac.TRUSTED_FOR_DELEGATION])

    def test___uac_20(self):
        u=uac.get_uac(0x20000)
        self.assertListEqual(u,[uac.MNS_LOGON_ACCOUNT])

    def test___uac_21(self):
        u=uac.get_uac(0x0080)
        self.assertListEqual(u,[uac.ENCRYPTED_TEXT_PWD_ALLOWED])

    def test___uac_not_21(self):
        u=uac.get_uac(0x0040)
        self.assertNotEqual(u,[uac.ENCRYPTED_TEXT_PWD_ALLOWED])

    def test___rsub_1(self):
        #TRUSTED_TO_AUTH_FOR_DELEGATION TRUSTED_TO_AUTH_FOR_DELEGATION TRUSTED_TO_AUTH_FOR_DELEGATION
        #0x1000000 0x1000000 0x1000000
        #1+2+3-3 int:33554432 hex:0x2000000 <-rezult
        #1+2+3 int:50331648 hex:0x3000000
        u=50331648-uac['TRUSTED_TO_AUTH_FOR_DELEGATION']
        self.assertEqual(u,33554432)

    def test___rsub_2(self):
        #WORKSTATION_TRUST_ACCOUNT ACCOUNTDISABLE TEMP_DUPLICATE_ACCOUNT
        #0x1000 0x0002 0x0100
        #1+2+3-3 int:4098 hex:0x1002 <-rezult
        #1+2+3 int:4354 hex:0x1102
        u=4354-uac['TEMP_DUPLICATE_ACCOUNT']
        self.assertEqual(u,4098)

    def test___rsub_3(self):
        #PASSWD_CANT_CHANGE ENCRYPTED_TEXT_PWD_ALLOWED WORKSTATION_TRUST_ACCOUNT
        #0x0040 0x0080 0x1000
        #1+2+3-3 int:192 hex:0xc0 <-rezult
        #1+2+3 int:4288 hex:0x10c0
        u=4288-uac['WORKSTATION_TRUST_ACCOUNT']
        self.assertEqual(u,192)

    def test___rsub_4(self):
        #INTERDOMAIN_TRUST_ACCOUNT PASSWD_CANT_CHANGE USE_DES_KEY_ONLY
        #0x0800 0x0040 0x200000
        #1+2+3-3 int:2112 hex:0x840 <-rezult
        #1+2+3 int:2099264 hex:0x200840
        u=2099264-uac['USE_DES_KEY_ONLY']
        self.assertEqual(u,2112)

    def test___rsub_5(self):
        #NORMAL_ACCOUNT SERVER_TRUST_ACCOUNT PASSWD_NOTREQD
        #0x0200 0x2000 0x0020
        #1+2+3-3 int:8704 hex:0x2200 <-rezult
        #1+2+3 int:8736 hex:0x2220
        u=8736-uac['PASSWD_NOTREQD']
        self.assertEqual(u,8704)

    def test___rsub_6(self):
        #MNS_LOGON_ACCOUNT INTERDOMAIN_TRUST_ACCOUNT LOCKOUT
        #0x20000 0x0800 0x0010
        #1+2+3-3 int:133120 hex:0x20800 <-rezult
        #1+2+3 int:133136 hex:0x20810
        u=133136-uac['LOCKOUT']
        self.assertEqual(u,133120)

    def test___rsub_7(self):
        #PASSWD_NOTREQD SERVER_TRUST_ACCOUNT MNS_LOGON_ACCOUNT
        #0x0020 0x2000 0x20000
        #1+2+3-3 int:8224 hex:0x2020 <-rezult
        #1+2+3 int:139296 hex:0x22020
        u=139296-uac['MNS_LOGON_ACCOUNT']
        self.assertEqual(u,8224)

    def test___rsub_8(self):
        #PASSWD_CANT_CHANGE PASSWD_NOTREQD ACCOUNTDISABLE
        #0x0040 0x0020 0x0002
        #1+2+3-3 int:96 hex:0x60 <-rezult
        #1+2+3 int:98 hex:0x62
        u=98-uac['ACCOUNTDISABLE']
        self.assertEqual(u,96)

    def test___rsub_9(self):
        #ENCRYPTED_TEXT_PWD_ALLOWED DONT_REQ_PREAUTH DONT_EXPIRE_PASSWORD
        #0x0080 0x400000 0x10000
        #1+2+3-3 int:4194432 hex:0x400080 <-rezult
        #1+2+3 int:4259968 hex:0x410080
        u=4259968-uac['DONT_EXPIRE_PASSWORD']
        self.assertEqual(u,4194432)

    def test___rsub_10(self):
        #PASSWD_CANT_CHANGE WORKSTATION_TRUST_ACCOUNT MNS_LOGON_ACCOUNT
        #0x0040 0x1000 0x20000
        #1+2+3-3 int:4160 hex:0x1040 <-rezult
        #1+2+3 int:135232 hex:0x21040
        u=135232-uac['MNS_LOGON_ACCOUNT']
        self.assertEqual(u,4160)

    def test___rsub_11(self):
        #DONT_REQ_PREAUTH SMARTCARD_REQUIRED TRUSTED_TO_AUTH_FOR_DELEGATION
        #0x400000 0x40000 0x1000000
        #1+2+3-3 int:4456448 hex:0x440000 <-rezult
        #1+2+3 int:21233664 hex:0x1440000
        u=21233664-uac['TRUSTED_TO_AUTH_FOR_DELEGATION']
        self.assertEqual(u,4456448)

    def test___rsub_12(self):
        #HOMEDIR_REQUIRED INTERDOMAIN_TRUST_ACCOUNT USE_DES_KEY_ONLY
        #0x0008 0x0800 0x200000
        #1+2+3-3 int:2056 hex:0x808 <-rezult
        #1+2+3 int:2099208 hex:0x200808
        u=2099208-uac['USE_DES_KEY_ONLY']
        self.assertEqual(u,2056)

    def test___rsub_13(self):
        #DONT_REQ_PREAUTH NORMAL_ACCOUNT PASSWORD_EXPIRED
        #0x400000 0x0200 0x800000
        #1+2+3-3 int:4194816 hex:0x400200 <-rezult
        #1+2+3 int:12583424 hex:0xc00200
        u=12583424-uac['PASSWORD_EXPIRED']
        self.assertEqual(u,4194816)

    def test___rsub_14(self):
        #ENCRYPTED_TEXT_PWD_ALLOWED SERVER_TRUST_ACCOUNT PASSWD_NOTREQD
        #0x0080 0x2000 0x0020
        #1+2+3-3 int:8320 hex:0x2080 <-rezult
        #1+2+3 int:8352 hex:0x20a0
        u=8352-uac['PASSWD_NOTREQD']
        self.assertEqual(u,8320)

    def test___rsub_15(self):
        #TRUSTED_FOR_DELEGATION TRUSTED_FOR_DELEGATION HOMEDIR_REQUIRED
        #0x80000 0x80000 0x0008
        #1+2+3-3 int:1048576 hex:0x100000 <-rezult
        #1+2+3 int:1048584 hex:0x100008
        u=1048584-uac['HOMEDIR_REQUIRED']
        self.assertEqual(u,1048576)

    def test___rsub_16(self):
        #DONT_REQ_PREAUTH ACCOUNTDISABLE TRUSTED_FOR_DELEGATION
        #0x400000 0x0002 0x80000
        #1+2+3-3 int:4194306 hex:0x400002 <-rezult
        #1+2+3 int:4718594 hex:0x480002
        u=4718594-uac['TRUSTED_FOR_DELEGATION']
        self.assertEqual(u,4194306)

    def test___rsub_17(self):
        #PASSWORD_EXPIRED HOMEDIR_REQUIRED DONT_REQ_PREAUTH
        #0x800000 0x0008 0x400000
        #1+2+3-3 int:8388616 hex:0x800008 <-rezult
        #1+2+3 int:12582920 hex:0xc00008
        u=12582920-uac['DONT_REQ_PREAUTH']
        self.assertEqual(u,8388616)

    def test___rsub_18(self):
        #SERVER_TRUST_ACCOUNT PASSWORD_EXPIRED WORKSTATION_TRUST_ACCOUNT
        #0x2000 0x800000 0x1000
        #1+2+3-3 int:8396800 hex:0x802000 <-rezult
        #1+2+3 int:8400896 hex:0x803000
        u=8400896-uac['WORKSTATION_TRUST_ACCOUNT']
        self.assertEqual(u,8396800)

    def test___rsub_19(self):
        #USE_DES_KEY_ONLY WORKSTATION_TRUST_ACCOUNT NORMAL_ACCOUNT
        #0x200000 0x1000 0x0200
        #1+2+3-3 int:2101248 hex:0x201000 <-rezult
        #1+2+3 int:2101760 hex:0x201200
        u=2101760-uac['NORMAL_ACCOUNT']
        self.assertEqual(u,2101248)

    def test___rsub_20(self):
        #SMARTCARD_REQUIRED MNS_LOGON_ACCOUNT TEMP_DUPLICATE_ACCOUNT
        #0x40000 0x20000 0x0100
        #1+2+3-3 int:393216 hex:0x60000 <-rezult
        #1+2+3 int:393472 hex:0x60100
        u=393472-uac['TEMP_DUPLICATE_ACCOUNT']
        self.assertEqual(u,393216)

    def test___rsub_21(self):
        #SMARTCARD_REQUIRED ACCOUNTDISABLE PASSWD_NOTREQD
        #0x40000 0x0002 0x0020
        #1+2+3-3 int:262146 hex:0x40002 <-rezult
        #1+2+3 int:262178 hex:0x40022
        u=262178-uac['PASSWD_NOTREQD']
        self.assertEqual(u,262146)

    def test___rsub_22(self):
        #TEMP_DUPLICATE_ACCOUNT USE_DES_KEY_ONLY INTERDOMAIN_TRUST_ACCOUNT
        #0x0100 0x200000 0x0800
        #1+2+3-3 int:2097408 hex:0x200100 <-rezult
        #1+2+3 int:2099456 hex:0x200900
        u=2099456-uac['INTERDOMAIN_TRUST_ACCOUNT']
        self.assertEqual(u,2097408)

    def test___rsub_23(self):
        #SCRIPT PASSWORD_EXPIRED
        #0x0001 0x800000
        #1+2-2 int:8388609 hex:0x00001 <-rezult
        #1+2 int:8388609 hex:0x800001
        u=8388609-uac['PASSWORD_EXPIRED']
        self.assertEqual(u,1)

    def test___rsub_24(self):
        #TEMP_DUPLICATE_ACCOUNT USE_DES_KEY_ONLY SCRIPT
        #0x0100 0x200000 0x0001
        #1+2+3-3 int:2097408 hex:0x200100 <-rezult
        #1+2+3 int:2097409 hex:0x200101
        u=2097409-uac['SCRIPT']
        self.assertEqual(u,2097408)

    def test___rsub_25(self):
        #PASSWORD_EXPIRED NOT_DELEGATED LOCKOUT
        #0x800000 0x100000 0x0010
        #1+2+3-3 int:9437184 hex:0x900000 <-rezult
        #1+2+3 int:9437200 hex:0x900010
        u=9437200-uac['LOCKOUT']
        self.assertEqual(u,9437184)

    def test___rsub_26(self):
        #ENCRYPTED_TEXT_PWD_ALLOWED USE_DES_KEY_ONLY LOCKOUT
        #0x0080 0x200000 0x0010
        #1+2+3-3 int:2097280 hex:0x200080 <-rezult
        #1+2+3 int:2097296 hex:0x200090
        u=2097296-uac['LOCKOUT']
        self.assertEqual(u,2097280)

    def test___rsub_27(self):
        #SMARTCARD_REQUIRED PASSWD_CANT_CHANGE PASSWD_CANT_CHANGE (флаги повторно не суммируются)
        #0x40000 0x0040 0x0040

        u=262272-uac['PASSWD_CANT_CHANGE']
        self.assertNotEqual(u,262208)

    def test___rsub_28(self):
        #NORMAL_ACCOUNT ENCRYPTED_TEXT_PWD_ALLOWED PASSWD_NOTREQD
        #0x0200 0x0080 0x0020
        #1+2+3-3 int:640 hex:0x280 <-rezult
        #1+2+3 int:672 hex:0x2a0
        u=672-uac['PASSWD_NOTREQD']
        self.assertEqual(u,640)

    def test___rsub_29(self):
        #SMARTCARD_REQUIRED HOMEDIR_REQUIRED SERVER_TRUST_ACCOUNT
        #0x40000 0x0008 0x2000
        #1+2+3-3 int:262152 hex:0x40008 <-rezult
        #1+2+3 int:270344 hex:0x42008
        u=270344-uac['SERVER_TRUST_ACCOUNT']
        self.assertEqual(u,262152)

    def test___rsub_30(self):
        #TRUSTED_FOR_DELEGATION PASSWORD_EXPIRED TRUSTED_TO_AUTH_FOR_DELEGATION
        #0x80000 0x800000 0x1000000
        #1+2+3-3 int:8912896 hex:0x880000 <-rezult
        #1+2+3 int:25690112 hex:0x1880000
        u=25690112-uac['TRUSTED_TO_AUTH_FOR_DELEGATION']
        self.assertEqual(u,8912896)

    def test___rsub_31(self):
        #TRUSTED_TO_AUTH_FOR_DELEGATION TRUSTED_TO_AUTH_FOR_DELEGATION INTERDOMAIN_TRUST_ACCOUNT
        #0x1000000 0x1000000 0x0800
        #1+2+3-3 int:33554432 hex:0x2000000 <-rezult
        #1+2+3 int:33556480 hex:0x2000800
        u=33556480-uac['INTERDOMAIN_TRUST_ACCOUNT']
        self.assertEqual(u,33554432)

    def test___rsub_32(self):
        #LOCKOUT PASSWD_NOTREQD NOT_DELEGATED
        #0x0010 0x0020 0x100000
        #1+2+3-3 int:48 hex:0x30 <-rezult
        #1+2+3 int:1048624 hex:0x100030
        u=1048624-uac['NOT_DELEGATED']
        self.assertEqual(u,48)

    def test___rsub_33(self):
        #NOT_DELEGATED MNS_LOGON_ACCOUNT ACCOUNTDISABLE
        #0x100000 0x20000 0x0002
        #1+2+3-3 int:1179648 hex:0x120000 <-rezult
        #1+2+3 int:1179650 hex:0x120002
        u=1179650-uac['ACCOUNTDISABLE']
        self.assertEqual(u,1179648)

    def test___rsub_34(self):
        #TRUSTED_FOR_DELEGATION HOMEDIR_REQUIRED WORKSTATION_TRUST_ACCOUNT
        #0x80000 0x0008 0x1000
        #1+2+3-3 int:524296 hex:0x80008 <-rezult
        #1+2+3 int:528392 hex:0x81008
        u=528392-uac['WORKSTATION_TRUST_ACCOUNT']
        self.assertEqual(u,524296)

    def test___rsub_35(self):
        #TRUSTED_TO_AUTH_FOR_DELEGATION ACCOUNTDISABLE PASSWORD_EXPIRED
        #0x1000000 0x0002 0x800000
        #1+2+3-3 int:16777218 hex:0x1000002 <-rezult
        #1+2+3 int:25165826 hex:0x1800002
        u=25165826-uac['PASSWORD_EXPIRED']
        self.assertEqual(u,16777218)

    def test___rsub_36(self):
        #LOCKOUT PASSWD_CANT_CHANGE NOT_DELEGATED
        #0x0010 0x0040 0x100000
        #1+2+3-3 int:80 hex:0x50 <-rezult
        #1+2+3 int:1048656 hex:0x100050
        u=1048656-uac['NOT_DELEGATED']
        self.assertEqual(u,80)

    def test___rsub_37(self):
        #SMARTCARD_REQUIRED TRUSTED_TO_AUTH_FOR_DELEGATION ACCOUNTDISABLE
        #0x40000 0x1000000 0x0002
        #1+2+3-3 int:17039360 hex:0x1040000 <-rezult
        #1+2+3 int:17039362 hex:0x1040002
        u=17039362-uac['ACCOUNTDISABLE']
        self.assertEqual(u,17039360)

    def test___rsub_38(self):
        #ACCOUNTDISABLE SCRIPT SCRIPT (флаги повторно не суммируются)
        #0x0002 0x0001 0x0001

        u=4-uac['SCRIPT']
        self.assertNotEqual(u,3)

    def test___rsub_39(self):
        #USE_DES_KEY_ONLY SERVER_TRUST_ACCOUNT NOT_DELEGATED
        #0x200000 0x2000 0x100000
        #1+2+3-3 int:2105344 hex:0x202000 <-rezult
        #1+2+3 int:3153920 hex:0x302000
        u=3153920-uac['NOT_DELEGATED']
        self.assertEqual(u,2105344)

    def test___rsub_40(self):
        #LOCKOUT HOMEDIR_REQUIRED NORMAL_ACCOUNT
        #0x0010 0x0008 0x0200
        #1+2+3-3 int:24 hex:0x18 <-rezult
        #1+2+3 int:536 hex:0x218
        u=536-uac['NORMAL_ACCOUNT']
        self.assertEqual(u,24)

    def test___rsub_41(self):
        #NOT_DELEGATED PASSWD_CANT_CHANGE DONT_EXPIRE_PASSWORD
        #0x100000 0x0040 0x10000
        #1+2+3-3 int:1048640 hex:0x100040 <-rezult
        #1+2+3 int:1114176 hex:0x110040
        u=1114176-uac['DONT_EXPIRE_PASSWORD']
        self.assertEqual(u,1048640)

    def test___rsub_42(self):
        #NORMAL_ACCOUNT LOCKOUT INTERDOMAIN_TRUST_ACCOUNT
        #0x0200 0x0010 0x0800
        #1+2+3-3 int:528 hex:0x210 <-rezult
        #1+2+3 int:2576 hex:0xa10
        u=2576-uac['INTERDOMAIN_TRUST_ACCOUNT']
        self.assertEqual(u,528)

    def test___control_1(self):
        self.assertEqual(uac.get_control([uac.PASSWD_CANT_CHANGE, uac.INTERDOMAIN_TRUST_ACCOUNT, uac.HOMEDIR_REQUIRED, uac.PASSWD_NOTREQD, uac.ENCRYPTED_TEXT_PWD_ALLOWED, ]),hex(0x0040+0x0800+0x0008+0x0020+0x0080))

    def test___control_not_1(self):
        self.assertNotEqual(uac.get_control([uac.PASSWD_CANT_CHANGE, uac.INTERDOMAIN_TRUST_ACCOUNT, uac.HOMEDIR_REQUIRED, uac.PASSWD_NOTREQD, uac.ENCRYPTED_TEXT_PWD_ALLOWED, ]),hex(0x0040+0x0800+0x0008+0x0020+0x0040))

    def test___control_2(self):
        self.assertEqual(uac.get_control([uac.USE_DES_KEY_ONLY, uac.DONT_EXPIRE_PASSWORD, uac.HOMEDIR_REQUIRED, uac.SCRIPT, uac.PASSWD_NOTREQD, uac.LOCKOUT, ]),hex(0x200000+0x10000+0x0008+0x0001+0x0020+0x0010))

    def test___control_3(self):
        self.assertEqual(uac.get_control([uac.MNS_LOGON_ACCOUNT, uac.TRUSTED_FOR_DELEGATION, uac.NORMAL_ACCOUNT, uac.LOCKOUT, uac.WORKSTATION_TRUST_ACCOUNT, uac.USE_DES_KEY_ONLY, uac.PASSWD_NOTREQD, ]),hex(0x20000+0x80000+0x0200+0x0010+0x1000+0x200000+0x0020))

    def test___control_4(self):
        self.assertEqual(uac.get_control([uac.DONT_REQ_PREAUTH, uac.USE_DES_KEY_ONLY, uac.PASSWD_NOTREQD, uac.MNS_LOGON_ACCOUNT, uac.TRUSTED_FOR_DELEGATION, ]),hex(0x400000+0x200000+0x0020+0x20000+0x80000))

    def test___control_5(self):
        self.assertEqual(uac.get_control([uac.WORKSTATION_TRUST_ACCOUNT, uac.NORMAL_ACCOUNT, uac.PASSWD_NOTREQD, uac.ENCRYPTED_TEXT_PWD_ALLOWED, uac.MNS_LOGON_ACCOUNT, uac.DONT_EXPIRE_PASSWORD, ]),hex(0x1000+0x0200+0x0020+0x0080+0x20000+0x10000))

    def test___control_6(self):
        self.assertEqual(uac.get_control([uac.HOMEDIR_REQUIRED, uac.DONT_REQ_PREAUTH, uac.USE_DES_KEY_ONLY, uac.LOCKOUT, ]),hex(0x0008+0x400000+0x200000+0x0010))

    def test___control_7(self):
        self.assertEqual(uac.get_control([uac.SCRIPT, uac.NOT_DELEGATED, uac.WORKSTATION_TRUST_ACCOUNT, uac.PASSWORD_EXPIRED, uac.SMARTCARD_REQUIRED, uac.ACCOUNTDISABLE, uac.USE_DES_KEY_ONLY, ]),hex(0x0001+0x100000+0x1000+0x800000+0x40000+0x0002+0x200000))

    def test___control_8(self):
        self.assertEqual(uac.get_control([uac.PASSWD_CANT_CHANGE, uac.SCRIPT, uac.USE_DES_KEY_ONLY, uac.HOMEDIR_REQUIRED, ]),hex(0x0040+0x0001+0x200000+0x0008))

    def test___control_9(self):
        self.assertEqual(uac.get_control([uac.TRUSTED_FOR_DELEGATION, uac.LOCKOUT, uac.DONT_REQ_PREAUTH, uac.PASSWORD_EXPIRED, uac.MNS_LOGON_ACCOUNT, uac.PASSWD_NOTREQD, uac.SMARTCARD_REQUIRED, ]),hex(0x80000+0x0010+0x400000+0x800000+0x20000+0x0020+0x40000))

    def test___control_10(self):
        self.assertEqual(uac.get_control([uac.ENCRYPTED_TEXT_PWD_ALLOWED, uac.NOT_DELEGATED, uac.DONT_EXPIRE_PASSWORD, uac.TRUSTED_FOR_DELEGATION, ]),hex(0x0080+0x100000+0x10000+0x80000))

    def test___control_11(self):
        self.assertEqual(uac.get_control([uac.NOT_DELEGATED, uac.PASSWD_NOTREQD, uac.SMARTCARD_REQUIRED, uac.DONT_REQ_PREAUTH, uac.PASSWD_CANT_CHANGE, uac.PASSWORD_EXPIRED, uac.TEMP_DUPLICATE_ACCOUNT, ]),hex(0x100000+0x0020+0x40000+0x400000+0x0040+0x800000+0x0100))

    def test___control_12(self):
        self.assertEqual(uac.get_control([uac.PASSWD_CANT_CHANGE, uac.TRUSTED_FOR_DELEGATION, uac.HOMEDIR_REQUIRED, uac.ACCOUNTDISABLE, ]),hex(0x0040+0x80000+0x0008+0x0002))

    def test___control_13(self):
        self.assertEqual(uac.get_control([uac.NORMAL_ACCOUNT, uac.TEMP_DUPLICATE_ACCOUNT, uac.WORKSTATION_TRUST_ACCOUNT, uac.ENCRYPTED_TEXT_PWD_ALLOWED, ]),hex(0x0200+0x0100+0x1000+0x0080))

    def test___control_14(self):
        self.assertEqual(uac.get_control([uac.MNS_LOGON_ACCOUNT, uac.ENCRYPTED_TEXT_PWD_ALLOWED, uac.INTERDOMAIN_TRUST_ACCOUNT, uac.SCRIPT, uac.HOMEDIR_REQUIRED, ]),hex(0x20000+0x0080+0x0800+0x0001+0x0008))

    def test___control_15(self):
        self.assertEqual(uac.get_control([uac.TEMP_DUPLICATE_ACCOUNT, uac.LOCKOUT, uac.TRUSTED_TO_AUTH_FOR_DELEGATION, uac.PASSWD_CANT_CHANGE, uac.WORKSTATION_TRUST_ACCOUNT, ]),hex(0x0100+0x0010+0x1000000+0x0040+0x1000))

    def test___control_not_15(self):
        self.assertNotEqual(uac.get_control([uac.USE_DES_KEY_ONLY, uac.LOCKOUT, uac.TRUSTED_TO_AUTH_FOR_DELEGATION, uac.PASSWD_CANT_CHANGE, uac.WORKSTATION_TRUST_ACCOUNT, ]),hex(0x0100+0x0010+0x1000000+0x0040+0x1000))

    def test___control_16(self):
        self.assertEqual(uac.get_control([uac.MNS_LOGON_ACCOUNT, uac.DONT_REQ_PREAUTH, uac.USE_DES_KEY_ONLY, uac.INTERDOMAIN_TRUST_ACCOUNT, uac.TRUSTED_FOR_DELEGATION, uac.PASSWORD_EXPIRED, uac.TEMP_DUPLICATE_ACCOUNT, ]),hex(0x20000+0x400000+0x200000+0x0800+0x80000+0x800000+0x0100))

    def test___control_17(self):
        self.assertEqual(uac.get_control([uac.PASSWORD_EXPIRED, uac.TRUSTED_TO_AUTH_FOR_DELEGATION, uac.DONT_REQ_PREAUTH, uac.LOCKOUT, uac.PASSWD_CANT_CHANGE, uac.INTERDOMAIN_TRUST_ACCOUNT, uac.WORKSTATION_TRUST_ACCOUNT, ]),hex(0x800000+0x1000000+0x400000+0x0010+0x0040+0x0800+0x1000))

    def test___control_18(self):
        self.assertEqual(uac.get_control([uac.HOMEDIR_REQUIRED, uac.LOCKOUT, uac.TRUSTED_FOR_DELEGATION, uac.NOT_DELEGATED, uac.PASSWORD_EXPIRED, uac.NORMAL_ACCOUNT, ]),hex(0x0008+0x0010+0x80000+0x100000+0x800000+0x0200))

    def test___control_19(self):
        self.assertEqual(uac.get_control([uac.INTERDOMAIN_TRUST_ACCOUNT, uac.TEMP_DUPLICATE_ACCOUNT, uac.PASSWD_CANT_CHANGE, uac.TRUSTED_TO_AUTH_FOR_DELEGATION, ]),hex(0x0800+0x0100+0x0040+0x1000000))

    def test___control_20(self):
        self.assertEqual(uac.get_control([uac.WORKSTATION_TRUST_ACCOUNT, uac.DONT_REQ_PREAUTH, uac.SERVER_TRUST_ACCOUNT, uac.NORMAL_ACCOUNT, uac.PASSWORD_EXPIRED, ]),hex(0x1000+0x400000+0x2000+0x0200+0x800000))

    def test___control_21(self):
        self.assertEqual(uac.get_control([uac.SCRIPT, uac.DONT_REQ_PREAUTH, uac.TEMP_DUPLICATE_ACCOUNT, uac.TRUSTED_FOR_DELEGATION, uac.HOMEDIR_REQUIRED, uac.MNS_LOGON_ACCOUNT, ]),hex(0x0001+0x400000+0x0100+0x80000+0x0008+0x20000))

    def test___control_not_21(self):
        self.assertNotEqual(uac.get_control([uac.SCRIPT, uac.DONT_REQ_PREAUTH, uac.WORKSTATION_TRUST_ACCOUNT, uac.TRUSTED_FOR_DELEGATION, uac.HOMEDIR_REQUIRED, uac.MNS_LOGON_ACCOUNT, ]),hex(0x0002+0x400000+0x0100+0x80000+0x0008+0x20000))

    def test___control_not_22(self):
        self.assertFalse(uac.get_control('some str'))

if __name__ == '__main__':
    unittest.main()