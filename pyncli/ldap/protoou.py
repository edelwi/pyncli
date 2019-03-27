# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        protoou
# Purpose:     To implement base protoou class.
#
# Author:      Evgeniy Semenov
#
# Created:     13.04.2017
# Copyright:   (c) Evgeniy Semenov 2017-2019
# Licence:     MIT
# -------------------------------------------------------------------------------

import sys

from .admexept import NotEnoughParams, EmptyParam, WrongParam, TooLong


class CleanSetAttrMeta(type):
    """Metaclass to change setattr method
    """

    def __call__(cls, *args, **kwargs):
        real_setattr = cls.__setattr__
        cls.__setattr__ = object.__setattr__
        self = super(CleanSetAttrMeta, cls).__call__(*args, **kwargs)
        cls.__setattr__ = real_setattr
        return self


class protoou(object):
    """
        base Organisational Unit class
    """

    # __metaclass__ = CleanSetAttrMeta

    _FIELD_MAP = {"name": "name"}

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
    }
    _DEFAULT_SORT_ORDER = ["name"]

    @classmethod
    def check_length(cls, field_name, field_value):
        """A class method that checks and adjusts a long transmitted setting.

        Args:
            field_name (str): attribute name.
            field_value (str): attribute value.

        Returns:
            (str): attribute value.
        """
        if field_name in list(cls._LDAP_LIMITS.keys()):
            if (
                len(field_value) < cls._LDAP_LIMITS[field_name]["min"]
                and cls._LDAP_LIMITS[field_name]["fail_min"]
            ):
                raise EmptyParam(
                    "{field} must not be blank.".format(field=field_name)
                )
            elif (
                len(field_value) > cls._LDAP_LIMITS[field_name]["max"]
                and cls._LDAP_LIMITS[field_name]["fail_max"]
            ):
                raise TooLong(
                    "{field} must not be blank.".format(field=field_name)
                )
            else:
                return field_value[: cls._LDAP_LIMITS[field_name]["max"]]
        else:
            return field_value

    def __init__(self, name, org_unit, **kwargs):  # uid,
        """constructor

            Args:
                name (str): Organisational Unit name
                org_unit (str): DN of parrent Organisational Unit

            Raises:
                WrongParam: The Organisational Unit parameter is not of the correct
                type.
        """
        if isinstance(name, str):
            self.name = protoou.check_length("name", name)
        else:
            try:
                self.name = str(name, "utf-8")
            except:
                raise WrongParam(
                    "Unicode string expected (name), conversion fails."
                )
            self.name = protoou.check_length("name", self.name)

        if isinstance(org_unit, str):
            self.org_unit = self.check_length("org_unit", org_unit)
        else:
            try:
                self.org_unit = str(org_unit, "utf-8")
            except:
                raise WrongParam(
                    "Unicode string expected (org_unit), conversion fails."
                )
            self.org_unit = self.check_length("org_unit", self.org_unit)

        self.dn = self.check_length("dn", self.get_dn())

    def get_dn(self):
        """Get Distinguished Name of the Organisational Unit

        Returns:
            (str): Distinguished Name of the Organisational Unit
        """
        # TODO1: Реализовать полное экранирование спецсимволов
        # см. https://msdn.microsoft.com/ru-ru/library/aa366101(v=vs.85).aspx
        if self.name.find(",") == -1:
            return "OU={name},{ou}".format(name=self.name, ou=self.org_unit)
        else:
            masked = "\,".join(self.name.split(","))
            return "OU={name},{ou}".format(name=masked, ou=self.org_unit)

    def __getitem__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        else:
            return False
            # may be raise EmptyParam('Value %s not found!' % name)

    def __unicode__(self):
        out = "class {0} instance:\n".format(self.__class__.__name__)
        for (key, value) in list(self.__dict__.items()):
            out += "{key}: {value}\n".format(key=key, value=value)
        return out

    def __str__(self):
        out = "class {0} instance:\n".format(self.__class__.__name__)
        for (key, value) in list(self.__dict__.items()):
            out += "{key}: {value}\n".format(key=key, value=value)

        return out
