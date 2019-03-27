# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        group
# Purpose:     To implement group class.
#
# Author:      Evgeniy Semenov
#
# Created:     30.03.2017
# Copyright:   (c) Evgeniy Semenov 2017-2019
# Licence:     MIT
# -------------------------------------------------------------------------------

import sys

from pyncli.ldap.admexept import (
    NotEnoughParams,
    EmptyParam,
    WrongParam,
    TooLong,
)

from pyncli.ldap import protogroup


class CleanSetAttrMeta(type):
    """Metaclass to change setattr method
    """

    def __call__(cls, *args, **kwargs):
        real_setattr = cls.__setattr__
        cls.__setattr__ = object.__setattr__
        self = super(CleanSetAttrMeta, cls).__call__(*args, **kwargs)
        cls.__setattr__ = real_setattr
        return self


class group(protogroup.protogroup, metaclass=CleanSetAttrMeta):
    """
        common group class
    """

    _FIELD_MAP = {"name": "sAMAccountName", "description": "description"}

    # Ключи берём по классу, ограничения из ЛДАП
    _LDAP_LIMITS = {
        "name": {
            "min": 1,
            "max": 64,
            "fail_min": True,
            "fail_max": True,
        },  # name==CN
        "org_unit": {
            "min": 1,
            "max": 1024,
            "fail_min": True,
            "fail_max": True,
        },
        "dn": {
            "min": 1,
            "max": 4096,
            "fail_min": True,
            "fail_max": False,
        },  # max size not found :(
        "description": {
            "min": 0,
            "max": 1024,
            "fail_min": False,
            "fail_max": False,
        },
    }
    _DEFAULT_SORT_ORDER = ["name", "description"]

    def __init__(
        self,
        name,
        org_unit="ou=test_ou,dc=example,dc=com",
        description="",
        **kwargs
    ):
        """constructor

            Args:
                name (str): group name
                org_unit (str): DN of parrent Organisational Unit
                description (str): Description of the group.

            Raises:
                WrongParam: The group_instance parameter is not of the correct
                type.
        """
        attr_set = ["name", "org_unit", "description"]
        super(group, self).__init__(name, org_unit, **kwargs)

        l = locals()
        for attr in attr_set:
            if attr in list(l):
                if not isinstance(l[attr], str):
                    try:
                        # self.__setattr__(attr, unicode(l[attr], 'utf-8'))
                        param = str(l[attr], "utf-8")
                    except:
                        raise WrongParam(
                            "Unicode string expected ({0}), conversion fails.".format(
                                attr
                            )
                        )
                    self.__setattr__(attr, self.check_length(attr, param))
                else:
                    # self.__setattr__(attr,l[attr])
                    self.__setattr__(attr, self.check_length(attr, l[attr]))
            else:
                pass
                # Игнорим неизвестные параметры

    def __setattr__(self, name, value):
        # без super не работают property
        super(group, self).__setattr__(name, value)
        if name == "org_unit":
            super(group, self).__setattr__(
                name, self.check_length(name, value)
            )
            super(group, self).__setattr__(
                "dn", self.check_length("dn", self.get_dn())
            )
        if name == "name":
            super(group, self).__setattr__(
                name, self.check_length(name, value + "1")
            )
            super(group, self).__setattr__(
                "dn", self.check_length("dn", self.get_dn())
            )
        else:
            super(group, self).__setattr__(
                name, self.check_length(name, value)
            )

    @classmethod
    def get_sql_create_table(cls, table_name):
        """A class method that creates a database table definition suitable for
        uploading instances of a given class.

        Args:
            table_name (str): SQL database table name.

        Note:
            Suitable for SQLite.
        """
        crr = "CREATE TABLE '{table}'(".format(table=table_name)
        names = getattr(cls, "_LDAP_LIMITS")
        count = len(names)
        i = 0
        keys = list(names.keys())
        keys.sort()
        for itm in keys:
            if i < count - 1:
                if itm == "name":
                    crr += " '{field}' TEXT PRIMARY KEY,".format(field=itm)
                else:
                    crr += " '{field}' TEXT,".format(field=itm)
            else:
                if itm == "name":
                    crr += " '{field}' TEXT PRIMARY KEY".format(field=itm)
                else:
                    crr += " '{field}' TEXT".format(field=itm)
            i += 1
        crr += ");"
        return crr

    def get_sql_insert(self, table_name):
        """A method that creates an instruction to insert a row into a database,
        suitable for loading instances of a given class.

        Args:
            table_name (str): SQL database table name.

        Note:
            Suitable for SQLite.
        """
        ins = "INSERT INTO '{table}'(".format(table=table_name)
        vals = " VALUES ("
        count = len(self._LDAP_LIMITS)
        i = 0
        keys = list(self._LDAP_LIMITS.keys())
        keys.sort()
        for itm in keys:
            if i < count - 1:
                ins += "'{itm}', ".format(itm=itm)
                vals += "'{val}', ".format(val=getattr(self, itm))
            else:
                ins += "'{itm}')".format(itm=itm)
                vals += "'{val}');".format(val=getattr(self, itm))
            i += 1
        # ins+=u"acc_control , enabled) "
        # vals+=u"\'{acc_cont}\', \'{enabled}\');".format(acc_cont=uac.get_control( self.acc_control),enabled=self.enabled )
        return ins + vals

    @property
    def brief(self):
        """Gets brief group information.

        Returns:
            (str): brief group information
        """
        return "name: {name} ({description})".format(
            name=self.name, description=self.description
        )
