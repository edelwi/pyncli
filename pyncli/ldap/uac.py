# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        userAccountControlEnum
# Purpose:     User Account Control Enumerator
#
# Author:      Evgeniy Semenov
#
# Created:     07.02.2017
# Copyright:   (c) Evgeniy Semenov 2017-2019
# Licence:     MIT
# -------------------------------------------------------------------------------

from enum import Enum


class uac(Enum):
    """
        userAccountControl Enumerator class
    """

    SCRIPT = 0x0001
    ACCOUNTDISABLE = 0x0002
    HOMEDIR_REQUIRED = 0x0008
    LOCKOUT = 0x0010
    PASSWD_NOTREQD = 0x0020
    PASSWD_CANT_CHANGE = 0x0040
    ENCRYPTED_TEXT_PWD_ALLOWED = 0x0080
    TEMP_DUPLICATE_ACCOUNT = 0x0100
    NORMAL_ACCOUNT = 0x0200
    INTERDOMAIN_TRUST_ACCOUNT = 0x0800
    WORKSTATION_TRUST_ACCOUNT = 0x1000
    SERVER_TRUST_ACCOUNT = 0x2000
    DONT_EXPIRE_PASSWORD = 0x10000
    MNS_LOGON_ACCOUNT = 0x20000
    SMARTCARD_REQUIRED = 0x40000
    TRUSTED_FOR_DELEGATION = 0x80000
    NOT_DELEGATED = 0x100000
    USE_DES_KEY_ONLY = 0x200000
    DONT_REQ_PREAUTH = 0x400000
    PASSWORD_EXPIRED = 0x800000
    TRUSTED_TO_AUTH_FOR_DELEGATION = 0x1000000

    @property
    def hex(self):
        """Get hex representation of uac instance

        Returns:
            (str): hex representation of uac instance
        """
        return hex(self.value)

    @property
    def val(self):
        """Get value of uac instance

        Returns:
            (int): value of uac instance
        """
        return int(self.value)

    def __add__(self, other):
        if self.val == other.val:
            return int(self.val)
        else:
            return int(self.val + other.val)

    def __radd__(self, other):
        fl = uac.get_status(other)
        if self.name not in fl:
            return other + self.val
        else:
            return other

    def __rsub__(self, other):
        if isinstance(other, int):
            fl = uac.get_status(other)
            if self.name in fl:
                return other - self.val
            else:
                return other
        elif isinstance(other, list):
            if len(other) > 0:
                if isinstance(other[0], str):
                    if self.name in other:
                        return [x for x in other if x != self.name]
                elif isinstance(other[0], uac):
                    if self in other:
                        return [x for x in other if x != self]
                else:
                    return other
            else:
                return other
        else:
            return other

    @staticmethod
    def get_status(hex_status_code):
        """Get a list of userAccountControl flags names.

        Args:
            hex_status_code (str): userAccountControl hex value

        Returns:
            (list): userAccountControl flags names.
        """
        rezStatus = []
        # print hex_status_code, type(hex_status_code)
        for sts in uac.__dict__["_member_names_"]:
            if (int(str(hex_status_code)) & uac[sts].val) == uac[sts].val:
                rezStatus.append(sts)
        return rezStatus

    @staticmethod
    def get_uac(hex_status_code):
        """Get a list of userAccountControl flags.

        Args:
            hex_status_code (str): userAccountControl hex value

        Returns:
            (list): userAccountControl flags.
        """
        rezStatus = []
        for sts in uac.__dict__["_member_names_"]:
            if (int(str(hex_status_code)) & uac[sts].val) == uac[sts].val:
                rezStatus.append(uac[sts])
        return rezStatus

    ##    @staticmethod
    ##    def get_code(uac_inst):
    ##        if isinstance(uac_inst, uac):
    ##            return uac_inst.hex
    ##        else:
    ##            _u=uac.get_uac(uac_inst)
    ##            _r=sum(_u)
    ##            return hex(_r )

    @staticmethod
    def get_control(flag_list):
        """Get userAccountControl value.

        Args:
            flag_list (list): userAccountControl list

        Returns:
            (list): userAccountControl hex value or False.
        """
        if isinstance(flag_list, list):
            rez = 0
            for it in flag_list:
                rez += it
            return hex(rez)
        else:
            return False
