# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        user
# Purpose:     Common user class
#
# Author:      Evgeniy Semenov
#
# Created:     07.02.2017
# Copyright:   (c) Evgeniy Semenov 2017-2019
# Licence:     MIT
# -------------------------------------------------------------------------------

from . import protouser
from .uac import uac
import string
from .admexept import NotEnoughParams, EmptyParam, WrongParam, TooLong
from . import utill


class CleanSetAttrMeta(type):
    """Metaclass to change setattr method
    """

    def __call__(cls, *args, **kwargs):
        real_setattr = cls.__setattr__
        cls.__setattr__ = object.__setattr__
        self = super(CleanSetAttrMeta, cls).__call__(*args, **kwargs)
        cls.__setattr__ = real_setattr
        return self


class user(protouser.protouser, metaclass=CleanSetAttrMeta):
    """
        Common user class
    """

    _FIELD_MAP = {
        "uid": "uid",
        "login": "sAMAccountName",
        # u'ou':u'',
        "surname": "sn",
        "first_name": "givenName",
        "middle_name": "middleName",
        "initials": "initials",
        "company": "company",
        "department": "department",
        "division": "division",
        "position": "title",
        "mail": "mail",
        "mobile": "mobile",
        "employee_type": "employeeType",
        "other_mailbox": "otherMailbox",
        "other_mobile": "otherMobile",
        "comment": "comment",
        "acc_control": "userAccountControl",
        "full_name": "displayName",
        "description": "description",
        "principal_name": "userPrincipalName",
    }
    # Ключи берём по классу, ограничения из ЛДАП
    _LDAP_LIMITS = {
        "uid": {"min": 0, "max": 256, "fail_min": True, "fail_max": True},
        "login": {
            "min": 1,
            "max": 64,
            "fail_min": True,
            "fail_max": True,
        },  # 20 https://msdn.microsoft.com/en-us/library/ms679635.aspx
        "org_unit": {
            "min": 1,
            "max": 1024,
            "fail_min": True,
            "fail_max": True,
        },
        "surname": {"min": 0, "max": 64, "fail_min": False, "fail_max": False},
        "first_name": {
            "min": 0,
            "max": 64,
            "fail_min": False,
            "fail_max": False,
        },
        "middle_name": {
            "min": 0,
            "max": 64,
            "fail_min": False,
            "fail_max": False,
        },
        "company": {"min": 0, "max": 64, "fail_min": False, "fail_max": False},
        "department": {
            "min": 0,
            "max": 64,
            "fail_min": False,
            "fail_max": False,
        },
        "division": {
            "min": 0,
            "max": 256,
            "fail_min": False,
            "fail_max": False,
        },
        "position": {
            "min": 0,
            "max": 128,
            "fail_min": False,
            "fail_max": False,
        },
        "mail": {"min": 0, "max": 256, "fail_min": False, "fail_max": False},
        "mobile": {"min": 0, "max": 64, "fail_min": False, "fail_max": False},
        "other_mailbox": {
            "min": 0,
            "max": 64,
            "fail_min": False,
            "fail_max": False,
        },
        "other_mobile": {
            "min": 0,
            "max": 64,
            "fail_min": False,
            "fail_max": False,
        },
        "comment": {
            "min": 0,
            "max": 1024,
            "fail_min": False,
            "fail_max": False,
        },
        "employee_type": {
            "min": 0,
            "max": 256,
            "fail_min": False,
            "fail_max": False,
        },
        "description": {
            "min": 0,
            "max": 1024,
            "fail_min": False,
            "fail_max": False,
        },
        "full_name": {
            "min": 0,
            "max": 256,
            "fail_min": False,
            "fail_max": False,
        },
        "initials": {"min": 0, "max": 6, "fail_min": False, "fail_max": False},
        "dn": {
            "min": 1,
            "max": 4096,
            "fail_min": True,
            "fail_max": False,
        },  # max size not found :(
        "principal_name": {
            "min": 0,
            "max": 1024,
            "fail_min": False,
            "fail_max": False,
        },
    }
    _DEFAULT_SORT_ORDER = [
        "login",
        "uid",
        "surname",
        "first_name",
        "middle_name",
        "position",
        "department",
        "division",
        "mail",
        "other_mailbox",
        "mobile",
        "other_mobile",
        "acc_control",
        "description",
        "comment",
        "employee_type",
        "full_name",
        "principal_name",
        "initials",
        "company",
    ]

    def __init__(
        self,
        login,
        uid="",
        org_unit="OU=test,DC=example,DC=com",
        surname="",
        first_name="",
        middle_name="",
        company="",
        department="",
        division="",
        position="",
        mail="",
        mobile="",
        other_mailbox="0",
        other_mobile="0",
        comment="",
        employee_type="",
        acc_control=[uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE],
        description="",
        principal_name="",
        **kwargs
    ):
        """constructor

            Args:
                login (str): user name
                uid (str): user ID
                org_unit (str): Users Organisational Name DN
                surname (str): surname
                first_name (str): first name
                middle_name (str): middle name
                company (str): company name
                department (str): department name
                division (str): division name
                position (str): user position
                mail (str): e-mail
                mobile (str): mobile
                other_mailbox (str): email check sign (as single valued attribute)
                other_mobile (str): mobile check sign (as single valued attribute)
                comment (str): comment
                employee_type (str): employee type
                acc_control (list of :uac: or hex): User Account Controll attribute
                description (str): description
                principal_name (str): user principal name
            Raises:
                WrongParam: The Organisational Unit parameter is not of the correct
                type.
        """
        attr_set = [
            "uid",
            "surname",
            "first_name",
            "middle_name",
            "company",
            "department",
            "division",
            "position",
            "mail",
            "mobile",
            "other_mailbox",
            "other_mobile",
            "comment",
            "employee_type",
            "description",
            "principal_name",
        ]
        super(user, self).__init__(login, **kwargs)

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

        l = locals()
        for attr in attr_set:
            if attr in list(l):
                if not isinstance(l[attr], str):
                    try:
                        param = str(l[attr], "utf-8")
                    except:
                        raise WrongParam(
                            "Unicode string expected ({0}), conversion fails.".format(
                                attr
                            )
                        )
                    self.__setattr__(attr, self.check_length(attr, param))
                else:
                    self.__setattr__(attr, self.check_length(attr, l[attr]))
            else:
                pass
                # Игнорим неизвестные параметры

        if isinstance(acc_control, list):
            if len(acc_control) == 0:
                self.acc_control = acc_control
            else:
                for acc in acc_control:
                    if not isinstance(acc, uac):
                        raise WrongParam(
                            "Unsupported type of acc_control variable."
                        )
                self.acc_control = acc_control
        elif isinstance(acc_control, int):
            self.acc_control = uac.get_uac(acc_control)
        else:
            raise WrongParam("Unsupported type of acc_control variable.")

        self.initials = self.check_length("initials", self.get_initials())
        self.dn = self.check_length("dn", self.get_dn())
        self.full_name = self.check_length("full_name", self.get_fullname())
        if principal_name:
            self.principal_name = self.check_length("principal_name", principal_name)
        else:
            self.principal_name = self.check_length(
                "principal_name", self.login + "@" + self.get_domain()
            )

    @property
    def enabled(self):
        """Get/set enabled account status

        Returns:
            (bool): True if account enabled
        """
        return uac.ACCOUNTDISABLE not in self.acc_control

    @enabled.setter
    def enabled(self, val_bool):
        if val_bool:
            if uac.ACCOUNTDISABLE in self.acc_control:
                self.acc_control.remove(uac.ACCOUNTDISABLE)
        else:
            if uac.ACCOUNTDISABLE not in self.acc_control:
                self.acc_control.append(uac.ACCOUNTDISABLE)

    def __setattr__(self, name, value):
        # без super не работают property
        super(user, self).__setattr__(name, value)
        if name == "middle_name":
            # self.__dict__[name] = value
            super(user, self).__setattr__(name, self.check_length(name, value))
            super(user, self).__setattr__(
                "initials", self.check_length("initials", self.get_initials())
            )
            super(user, self).__setattr__(
                "full_name",
                self.check_length("full_name", self.get_fullname()),
            )
        if name == "org_unit":
            super(user, self).__setattr__(name, self.check_length(name, value))
            super(user, self).__setattr__(
                "dn", self.check_length("dn", self.get_dn())
            )
            super(user, self).__setattr__(
                "principal_name",
                self.check_length(
                    "principal_name", self.login + "@" + self.get_domain()
                ),
            )
        if name == "surname":
            super(user, self).__setattr__(name, self.check_length(name, value))
            super(user, self).__setattr__(
                "full_name",
                self.check_length("full_name", self.get_fullname()),
            )
        if name == "first_name":
            super(user, self).__setattr__(name, self.check_length(name, value))
            super(user, self).__setattr__(
                "full_name",
                self.check_length("full_name", self.get_fullname()),
            )
        else:
            super(user, self).__setattr__(name, self.check_length(name, value))

    def get_initials(self):
        """Get user initials

        Returns:
            (str): initials
        """
        if len(self.middle_name) > 0:
            return self.middle_name[0]
        else:
            return ""

    def get_dn(self):
        """Get Distinguished Name of the user

        Returns:
            (str): Distinguished Name of the user
        """
        # TODO1: Реализовать полное экранирование спецсимволов
        # см. https://msdn.microsoft.com/ru-ru/library/aa366101(v=vs.85).aspx
        if self.login.find(",") == -1:
            return "CN={login},{ou}".format(login=self.login, ou=self.org_unit)
        else:
            masked = "\,".join(self.login.split(","))
            return "CN={login},{ou}".format(login=masked, ou=self.org_unit)

    def get_fullname(self):
        """Get Full Name of the user

        Returns:
            (str): Full Name of the user
        """
        fn = " ".join([self.surname, self.first_name, self.middle_name])
        fn = fn.strip()
        fn = " ".join(fn.split())  # убрать повторные пробелы, если есть
        return fn

    def get_domain(self):
        """Get domain name

        Returns:
            (str): domain name in dot notation
        """
        ou_dn = self.org_unit
        ou_dn = ou_dn.lower()
        ou_dn = ou_dn.replace(" ", "")
        beg = ou_dn.find("dc=")
        if beg == -1:
            raise WrongParam(
                "Parameter org_unit has wrong format. Domain name part not found."
            )
        dom = ou_dn[beg:]
        dom = dom.replace("dc=", "")
        dom = dom.replace(",", ".")
        return dom

    def get_ldap_attrs(self):
        """Get ldap attributes

            Returns:
                (dict): LDAP attributes dictionary of instance.
        """
        _attrs = {}
        for a in list(self._FIELD_MAP.keys()):
            if a == "acc_control":
                _attrs[self._FIELD_MAP[a]] = str(
                    uac.get_control(self.__getitem__(a))
                )
            else:
                _attrs[self._FIELD_MAP[a]] = self.__getitem__(a)
        return _attrs

    def diff_ldap_attrs(self, instance):
        """Get instances difference (in ldap attributes)

            the method returns a dictionary with ldap attributes and their
            values that do not match in two instances of the class (self and
            passed to the instance parameter)

            Args:
                instance (:obj: 'protouser' or inheritor ): instance for
                    comparison

            Returns:
                (dict): dictionary with ldap attributes and their values
                    that do not match in two instances of the class
        """
        if type(instance) is not self.__class__:
            raise WrongParam(
                "%s is not %s instance!" % (instance, self.__class__.__name__)
            )
        ret = {}
        if self == instance:
            return ret
        else:
            for (key, value) in list(self.__dict__.items()):
                if self.__getitem__(key) != instance.__getitem__(key):
                    if key in list(self._FIELD_MAP.keys()):
                        if key == "acc_control":
                            ret[self._FIELD_MAP[key]] = str(
                                uac.get_control(instance.__getitem__(key))
                            )
                        else:
                            ret[self._FIELD_MAP[key]] = instance.__getitem__(
                                key
                            )
            return ret

    def diff_ldap_attrs_by_categories(self, instance):
        """Get instances difference (in ldap attributes with categories)

            the method returns a dictionary with ldap attributes and their
            values that do not match in two instances of the class (self and
            passed to the instance parameter). For the "modify" method from the
            library ldap 3.

            Args:
                instance (:obj: 'user' or inheritor ): instance for
                    comparison

            Returns:
                (dict): dictionary with ldap attributes and their values
                    that do not match in two instances of the class
            Raises:
                WrongParam: The instance parameter is not of the correct
                type.

            Note:
                Does not detect container shifts.
        """
        if type(instance) is not self.__class__:
            raise WrongParam(
                "%s is not %s instance!" % (instance, self.__class__.__name__)
            )
        if self.login != instance.login:
            raise WrongParam(
                "Wrong method call! Logins must be equal (%s!=%s). \
                To rename RDN use special method."
                % (self.login, instance.login)
            )
        ret = {}
        if self == instance:
            return ret
        else:
            for (key, value) in list(self.diff(instance).items()):
                if self.__getitem__(key) != instance.__getitem__(key):
                    if key in list(self._FIELD_MAP.keys()):
                        VL = []
                        if self.__getitem__(key) == "":
                            OP = "MODIFY_ADD"
                            if key == "acc_control":
                                VL.append(
                                    int(
                                        uac.get_control(
                                            instance.__getitem__(key)
                                        ),
                                        16,
                                    )
                                )
                            else:
                                VL.append(instance.__getitem__(key))
                        elif instance.__getitem__(key) == "":
                            OP = "MODIFY_DELETE"
                        else:
                            OP = "MODIFY_REPLACE"
                            if key == "acc_control":
                                VL.append(
                                    int(
                                        uac.get_control(
                                            instance.__getitem__(key)
                                        ),
                                        16,
                                    )
                                )
                            else:
                                VL.append(instance.__getitem__(key))
                        ret[self._FIELD_MAP[key]] = [(OP, VL)]
            return ret

    @property
    def brief(self):
        """Gets brief user information.

        Returns:
            (str): brief user information
        """
        return "{fio} (l:{login}|u:{uid})".format(
            fio=self.full_name, login=self.login, uid=self.uid
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
        for itm in list(names.keys()):
            if itm == "login":
                crr += " '{field}' TEXT PRIMARY KEY,".format(field=itm)
            else:
                crr += " '{field}' TEXT,".format(field=itm)
        crr += "acc_control TEXT, enabled TEXT);"
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
        for itm in list(self._LDAP_LIMITS.keys()):
            ins += "'{itm}', ".format(itm=itm)
            vals += "'{val}', ".format(
                val=utill.sqllite_quote_ap(getattr(self, itm))
            )
        ins += "acc_control , enabled) "
        vals += "'{acc_cont}', '{enabled}');".format(
            acc_cont=uac.get_control(self.acc_control), enabled=self.enabled
        )
        return ins + vals
