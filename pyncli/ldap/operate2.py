# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        operate2
# Purpose:     LDAP operations for cloud.
# Version:     2.0 (py3)
#
# Author:      Evgeniy Semenov
#
# Created:     15.02.2017
# Copyright:   (c) Evgeniy Semenov 2017-2019
# Licence:     MIT
# -------------------------------------------------------------------------------
"""A module that implements the admin class for working with LDAP.
"""
import ldap3
from ldap3.utils import hashed
from ldap3.extend.microsoft.addMembersToGroups import ad_add_members_to_groups
from ldap3.extend.microsoft.removeMembersFromGroups import (
    ad_remove_members_from_groups,
)
import ssl
import sys
from . import user
import copy
import string
import ldap3.core.exceptions as ex
from . import group
from . import ou
from .admexept import (
    AdminException,
    ConnectionFailure,
    EmptyParam,
    NotEnoughParams,
    OperationFailure,
    TooLong,
    WrongParam,
    NotFound,
)

# from https://www.samba.org/ftp/unpacked/ldb/include/ldb.h

#: str: LDAP AND OID comparator.
OID_COMPARATOR_AND = "1.2.840.113556.1.4.803"

#: str: LDAP OR OID comparator.
OID_COMPARATOR_OR = "1.2.840.113556.1.4.804"

# source samba/libds/common/flags.h
# User flags for "userAccountControl"

# NT or Lan Manager Login script must be executed
UF_SCRIPT = 0x00000001
UF_ACCOUNTDISABLE = 0x00000002
UF_00000004 = 0x00000004
UF_HOMEDIR_REQUIRED = 0x00000008

UF_LOCKOUT = 0x00000010
UF_PASSWD_NOTREQD = 0x00000020
UF_PASSWD_CANT_CHANGE = 0x00000040
UF_ENCRYPTED_TEXT_PASSWORD_ALLOWED = 0x00000080

# Local user account in usrmgr
UF_TEMP_DUPLICATE_ACCOUNT = 0x00000100
UF_NORMAL_ACCOUNT = 0x00000200
UF_00000400 = 0x00000400
UF_INTERDOMAIN_TRUST_ACCOUNT = 0x00000800

UF_WORKSTATION_TRUST_ACCOUNT = 0x00001000
UF_SERVER_TRUST_ACCOUNT = 0x00002000
UF_00004000 = 0x00004000
UF_00008000 = 0x00008000

UF_DONT_EXPIRE_PASSWD = 0x00010000
UF_MNS_LOGON_ACCOUNT = 0x00020000
UF_SMARTCARD_REQUIRED = 0x00040000
UF_TRUSTED_FOR_DELEGATION = 0x00080000

UF_NOT_DELEGATED = 0x00100000
UF_USE_DES_KEY_ONLY = 0x00200000
UF_DONT_REQUIRE_PREAUTH = 0x00400000
UF_PASSWORD_EXPIRED = 0x00800000
UF_TRUSTED_TO_AUTHENTICATE_FOR_DELEGATION = 0x01000000
UF_NO_AUTH_DATA_REQUIRED = 0x02000000
UF_PARTIAL_SECRETS_ACCOUNT = 0x04000000
UF_USE_AES_KEYS = 0x08000000


##UF_MACHINE_ACCOUNT_MASK (\
##                UF_INTERDOMAIN_TRUST_ACCOUNT |\
##                UF_WORKSTATION_TRUST_ACCOUNT |\
##                UF_SERVER_TRUST_ACCOUNT \
##                )
##
##UF_ACCOUNT_TYPE_MASK (\
##                UF_TEMP_DUPLICATE_ACCOUNT |\
##                UF_NORMAL_ACCOUNT |\
##                UF_INTERDOMAIN_TRUST_ACCOUNT |\
##                UF_WORKSTATION_TRUST_ACCOUNT |\
##                UF_SERVER_TRUST_ACCOUNT \
##                )
##
##
#### * MS-SAMR 2.2.1.13 UF_FLAG Codes states that some bits are ignored by
#### * clients and servers.  Other flags (like UF_LOCKOUT have special
#### * behaviours, but are not set in the traditional sense).
#### *
#### * See the samldb module for the use of this define.
##
##
##UF_SETTABLE_BITS (\
##                UF_ACCOUNTDISABLE |\
##                UF_HOMEDIR_REQUIRED  |\
##                UF_PASSWD_NOTREQD |\
##                UF_ACCOUNT_TYPE_MASK | \
##                UF_DONT_EXPIRE_PASSWD | \
##                UF_MNS_LOGON_ACCOUNT |\
##                UF_ENCRYPTED_TEXT_PASSWORD_ALLOWED |\
##                UF_SMARTCARD_REQUIRED |\
##                UF_TRUSTED_FOR_DELEGATION |\
##                UF_NOT_DELEGATED |\
##                UF_USE_DES_KEY_ONLY  |\
##                UF_DONT_REQUIRE_PREAUTH |\
##                UF_TRUSTED_TO_AUTHENTICATE_FOR_DELEGATION |\
##                UF_NO_AUTH_DATA_REQUIRED |\
##                UF_PARTIAL_SECRETS_ACCOUNT |\
##                UF_USE_AES_KEYS \
##                )


class admin(object):
    """
        Class for administrative operations
    """

    _tls_configuration = ldap3.Tls(
        validate=ssl.CERT_NONE, version=ssl.PROTOCOL_TLSv1
    )
    _user_class_map = {"common": "user"}

    def __init__(self, ldap_admin, admin_pwd, ldap_server_list):
        srv_obj = []
        for srv in ldap_server_list:
            srv_obj.append(
                ldap3.Server(
                    srv,
                    use_ssl=True,
                    get_info=ldap3.ALL,
                    tls=self._tls_configuration,
                )
            )
        sever_pool = ldap3.ServerPool(
            srv_obj, pool_strategy=ldap3.ROUND_ROBIN, active=True
        )
        self.conn = ldap3.Connection(
            sever_pool, user=ldap_admin, password=admin_pwd
        )
        self.conn.start_tls()
        self.conn.bind()
        d_info = self.conn.server.info.naming_contexts
        d_name = ""
        for it in d_info:
            if it.startswith("CN=Configuration,"):
                d_name = it.replace("CN=Configuration,", "")
        if d_name == "":
            print("Uuuppsss, domain name not found!")
        self.ldap_domain_name = d_name

    def create_user(self, user_instance, new_password):
        """ Creates a user in ldap.

            A user is created based on the data of user_instance, which is an
            instance of the class user.user or its descendants.

            Args:
                user_instance (:obj: 'user.user' or inheritor ): an instance of
                    the class user.user or its descendant with data about the
                    user.
                new_password (str): the password that the new user will have.

            Returns:
                None

            Raises:
                OperationFailure: The operation failed.
                WrongParam: The user_instance parameter is not of the correct
                type.
        """
        if isinstance(user_instance, user.user) or issubclass(
            user_instance.__class__, user.user
        ):
            attrs = {}
            if bytes == str:  # python2, converts to unicode
                new_password = unicode(new_password)
            encoded_new_password = ('"%s"' % new_password).encode("utf-16-le")

            attrs = user_instance.get_ldap_attrs()
            attrs["unicodePwd"] = encoded_new_password

            # to prevent invalidAttributeSyntax 00000057: LdapErr: DSID-0C090C3E
            # on Windows DC
            uac_val = attrs["userAccountControl"]
            attrs["userAccountControl"] = int(uac_val, 0)

            attrs = dict((k, v) for k, v in attrs.items() if v != "")
            dn = user_instance.get_dn()
            self.conn.add(dn, object_class=["user"], attributes=attrs)
            if self.conn.result["result"] != 0:
                raise OperationFailure(
                    "Can not create user: "
                    + "{user}. Server meseage: {desc} - {msgs}.".format(
                        user=user_instance.brief,
                        desc=self.conn.result["description"],
                        msgs=self.conn.result["message"],
                    )
                )
        else:
            raise WrongParam(
                "Type mismatch for user_instance "
                + "{ui}. It must be the user class instance ore its subclass".format(
                    ui=user_instance
                )
            )

    def update_user(self, from_user_inst, to_user_inst, force=False):
        """Updates user data in ldap, except RDN.

            Args:
                from_user_inst (:obj: 'user.user' or inheritor ): an instance
                    of the class user.user or its descendant with source data
                    about the user.
                to_user_inst (:obj: 'user.user' or inheritor ): an instance of
                    the class user.user or its descendant with updated user
                    data.

            Note:
                input parameters must be of the same class.

            Returns:
                None

            Raises:
                OperationFailure: Update failed.
        """
        diff_attrs = from_user_inst.diff_ldap_attrs_by_categories(
            to_user_inst, force
        )
        # print diff_attrs
        self.conn.modify(from_user_inst.get_dn(), diff_attrs)
        if self.conn.result["result"] != 0:
            raise OperationFailure(
                "Can not update user: "
                + "{user}. Server meseage: {desc} - {msgs}.".format(
                    user=from_user_inst.brief,
                    desc=self.conn.result["description"],
                    msgs=self.conn.result["message"],
                )
            )

    def rename_user_rdn(self, from_user_inst, to_user_inst):
        """ Updates user RDN data in LAP (account rename).

            Args:
                from_user_inst (:obj: 'user.user' or inheritor ): an instance
                    of the class user.user or its descendant with source data
                    about the user.
                to_user_inst (:obj: 'user.user' or inheritor ): an instance of
                    the class user.user or its descendant with updated user
                    data.

            Note:
                input parameters must be of the same class.
                From to_user_inst, only data about sAMAccountName is taken,
                everything else is ignored.

            Returns:
                None

            Raises:
                OperationFailure: Update failed.
        """
        rdn = "cn={login}".format(login=to_user_inst.login)
        self.conn.modify_dn(from_user_inst.get_dn(), rdn)
        if self.conn.result["result"] != 0:
            raise OperationFailure(
                "Can not rename RDN user: "
                + "{user}. Server meseage: {desc} - {msgs}.".format(
                    user=user_instance.brief,
                    desc=self.conn.result["description"],
                    msgs=self.conn.result["message"],
                )
            )

    def delete_user(self, user_instance):
        """ Remove user from ldap.

            Args:
                user_instance (:obj: 'user.user' or inheritor ): an instance
                    of the class user.user or its descendant with source data
                    about the user.

            Returns:
                None

            Raises:
                OperationFailure: The operation failed.
        """
        self.conn.delete(user_instance.get_dn())
        if self.conn.result["result"] != 0:
            raise OperationFailure(
                "Can not delete user: "
                + "{user}. Server meseage: {desc} - {msgs}.".format(
                    user=user_instance.brief,
                    desc=self.conn.result["description"],
                    msgs=self.conn.result["message"],
                )
            )

    def disable_user(self, user_instance):
        """ Disable user account in ldap.

            Args:
                user_instance (:obj: 'user.user' or inheritor ): an instance
                    of the class user.user or its descendant with source data
                    about the user.

            Returns:
                user_instance (:obj: 'user.user' or inheritor ): an instance
                    of the class user.user or its descendant with source data
                    about the user. If the account is locked, then an instance
                    of the user class is returned with the userAccountControl
                    field changed.
                    If no change was required, the original instance is
                    returned.

            Raises:
                OperationFailure: Update failed.
        """
        if user_instance.enabled:
            updated = copy.deepcopy(user_instance)
            updated.enabled = False
            self.update_user(user_instance, updated)
            return updated
        return user_instance

    def enable_user(self, user_instance):
        """ Enable user account in ldap.

            Args:
                user_instance (:obj: 'user.user' or inheritor ): an instance
                    of the class user.user or its descendant with source data
                    about the user.

            Returns:
                user_instance (:obj: 'user.user' or inheritor ): an instance
                    of the class user.user or its descendant with source data
                    about the user. If the account has been unblocked, then an
                    instance of the user class is returned with the
                    userAccountControl field changed.
                    If no change was required, the original instance is
                    returned.

            Raises:
                OperationFailure: Update failed.
        """
        if not user_instance.enabled:
            updated = copy.deepcopy(user_instance)
            updated.enabled = True
            self.update_user(user_instance, updated)
            return updated
        return user_instance

    def get_user(self, login, user_class_name):
        """ Find the user of the specified class in ldap.

            The user is searched by login in accordance with the specified
            class name.

            Args:
                login (str): username to search.
                user_class_name (str): class name of the user whose instance
                    should return the method ('user', ...).

            Returns:
                user_instance (:obj: 'user.user' or inheritor ): an instance
                    of the class user.user or its descendant with source data
                    about the user.

            Raises:
                NotFound: User is not found.
        """
        mdl = getattr(sys.modules[__name__], user_class_name)
        cls = getattr(mdl, user_class_name)
        cls_vl = {}

        resp = self.conn.search(
            "dc=unn,dc=global",
            "(sAMAccountName={login})".format(login=login),
            attributes=list(cls._FIELD_MAP.values()),
        )

        if resp == False:
            raise NotFound(
                "User login: {login}, uid: {uid} not found.".format(
                    login=login, uid=uid
                )
            )
        for cls_attr, ldap_attr in cls._FIELD_MAP.items():
            if ldap_attr in self.conn.entries[0]:
                l3_attr = getattr(self.conn.entries[0], ldap_attr)
                cls_vl[cls_attr] = (
                    "" if l3_attr.value is None else l3_attr.value
                )
        usr = cls(**cls_vl)

        return usr

    def get_some_user(self, login):
        """ Find a user in ldap.

            User is searched by login. The user class is determined based on
            the ldap value of the employeeType attribute.

            Args:
                login (str): username to search.

            Returns:
                user_instance (:obj: 'user.user' or inheritor ): an instance
                    of the class user.user or its descendant with source data
                    about the user.

            Raises:
                NotFound: User is not found.
        """
        resp = self.conn.search(
            search_base=self.ldap_domain_name,
            search_filter="(sAMAccountName={login})".format(login=login),
            attributes=ldap3.ALL_ATTRIBUTES,
        )

        if resp == False:
            raise NotFound(
                "User login: {login} not found.".format(login=login)
            )
        else:
            try:
                et = getattr(self.conn.entries[0], "employeeType", None)
            except ex.LDAPCursorError:
                et = None

            if et is not None:
                user_class_name = self._user_class_map[et.value]
            else:
                user_class_name = self._user_class_map["common"]

            mdl = getattr(sys.modules[__name__], user_class_name)
            cls = getattr(mdl, user_class_name)
            cls_vl = {}
            for cls_attr, ldap_attr in cls._FIELD_MAP.items():
                if ldap_attr in self.conn.entries[0]:
                    l3_attr = getattr(self.conn.entries[0], ldap_attr)
                    cls_vl[cls_attr] = (
                        "" if l3_attr.value is None else l3_attr.value
                    )
            usr = cls(**cls_vl)
            return usr

    def search_users(self, ldap_filter, base=""):
        """ Find a user in ldap by ldap filter.

            Users are searched by ldap filter. The user class is determined
            based on the ldap value of the employeeType attribute.

            Args:
                ldap_filter (str): line with ldap request.
                base  (str): ldap base to search for users.

            Returns:
                user_instance (:list: of :obj: 'user.user' or inheritor ):
                    a list of instances of user.user or its descendants with
                    information about ldap users.

            Raises:
                OperationFailure: User is not found.


            Examples:
                You can find users in the other group as follows::

                    filter='(&(objectCategory=person)(objectClass=user)
                        (memberof=CN=other,OU=groups,DC=example,DC=com))'
                    staff_base=u'ou=staff,dc=example,dc=com'
                    result=instance.search_users(ldap_filter=filter,
                        base=staff_base)
        """
        rez = []
        if base == "":
            base = self.ldap_domain_name

        resp = self.conn.search(
            search_base=base,
            search_filter=ldap_filter,
            attributes=ldap3.ALL_ATTRIBUTES,
        )

        if resp == False:
            raise OperationFailure(
                "Search failed. Server meseage: {desc} - {msgs}.".format(
                    desc=self.conn.result["description"],
                    msgs=self.conn.result["message"],
                )
            )
        else:
            for itm in self.conn.entries:
                try:
                    et = getattr(itm, "employeeType", None)
                except ex.LDAPCursorError:
                    et = None
                if et is not None:
                    user_class_name = self._user_class_map[et.value]
                else:
                    user_class_name = self._user_class_map["common"]

                mdl = getattr(sys.modules[__name__], user_class_name)
                cls = getattr(mdl, user_class_name)
                cls_vl = {}
                for cls_attr, ldap_attr in cls._FIELD_MAP.items():
                    if ldap_attr in itm:
                        l3_attr = getattr(itm, ldap_attr)
                        cls_vl[cls_attr] = (
                            "" if l3_attr.value is None else l3_attr.value
                        )
                DN = str(getattr(itm, "distinguishedName"))
                CN = str(getattr(itm, "CN"))
                BASE = DN.replace("CN=" + CN + ",", "")
                cls_vl["org_unit"] = BASE

                usr = cls(**cls_vl)
                rez.append(usr)
            return rez

    def search_users_p(self, ldap_filter, base="", user_class_name=None):
        """ Find a user in ldap by ldap-filter (paged ldap search).

            Users are searched by ldap filter. The search is made page by page,
            but transparent for use. Suitable for unloading a large number of
            results.
            The user class is determined based on the ldap value of the
            employeeType attribute.

            Args:
                ldap_filter (str): line with ldap request.
                base  (str): ldap base to search for users.
                user_class_name (str): The class name of the user whose
                    instances will be returned (if None, the class is
                    determined based on the field employeeType).

            Returns:
                user_instance (:list: of :obj: 'user.user' or inheritor ):
                    a list of instances of user.user or its descendants with
                    information about ldap users.

            Raises:
                OperationFailure: User is not found.


            Examples:
                You can find users in the other group as follows::

                    filter='(&(objectCategory=person)(objectClass=user)
                        (memberof=CN=other,OU=groups,DC=example,DC=com))'
                    staff_base=u'ou=staff,dc=example,dc=com'
                    result=instance.search_users_p(ldap_filter=filter,
                        base=staff_base)
        """
        rez = []
        if base == "":
            base = self.ldap_domain_name

        resp = self.conn.extend.standard.paged_search(
            search_base=base,
            search_filter=ldap_filter,
            attributes=ldap3.ALL_ATTRIBUTES,
            paged_size=1000,
            generator=True,
        )
        if resp == False:
            raise OperationFailure(
                "Search failed. Server meseage: {desc} - {msgs}.".format(
                    desc=self.conn.result["description"],
                    msgs=self.conn.result["message"],
                )
            )
        else:
            for itm in resp:
                if "attributes" in itm:
                    if user_class_name is None:
                        try:
                            et = itm["attributes"]["employeeType"]
                        except (ex.LDAPCursorError, KeyError):
                            et = None
                        if et is not None:
                            user_class_name = self._user_class_map[et]
                        else:
                            user_class_name = self._user_class_map["common"]

                    mdl = getattr(sys.modules[__name__], user_class_name)
                    cls = getattr(mdl, user_class_name)
                    cls_vl = {}
                    for cls_attr, ldap_attr in cls._FIELD_MAP.items():
                        if ldap_attr in itm["attributes"]:
                            l3_attr = itm["attributes"][ldap_attr]
                            if (
                                isinstance(l3_attr, list)
                                and cls_attr != "memberof"
                            ):
                                cls_vl[cls_attr] = l3_attr[0]
                            else:
                                cls_vl[cls_attr] = l3_attr

                    if not isinstance(
                        itm["attributes"]["distinguishedName"], str
                    ):
                        DN = str(itm["attributes"]["distinguishedName"])
                    else:
                        DN = itm["attributes"]["distinguishedName"]
                    if not isinstance(itm["attributes"]["CN"], str):
                        CN = str(itm["attributes"]["CN"])
                    else:
                        CN = itm["attributes"]["CN"]
                    BASE = DN.replace("CN=" + CN + ",", "")
                    cls_vl["org_unit"] = BASE

                    usr = cls(**cls_vl)
                    rez.append(usr)
            return rez

    def _add_users_to_groups(self, members_dn, groups_dn):
        return ad_add_members_to_groups(
            self.conn, members_dn, groups_dn, fix=False
        )

    def add_users_to_groups(self, user_instance_list, group_instance_list):
        """ Add users to groups

            Adds a list of users to the list of groups.

            Args:
                user_instance_list: (:list: of :obj: 'user.user' or inheritor ):
                    the list of instances of user.user or its descendants who
                    should be added to the ldap groups.
                group_instance_list: (:list: of :obj: 'group.group' or
                    inheritor ): the list of instances of group.group or its
                    descendants in which the users should be added.
            Returns:
                status: (bool): a boolean where True means that the operation was
                    successful and False means an error has happened
        """
        members_dn = [u.get_dn() for u in user_instance_list]
        group_list = [g.get_dn() for g in group_instance_list]
        return ad_add_members_to_groups(
            self.conn, members_dn, group_list, fix=True
        )

    def _remove_users_from_groups(self, members_dn, groups_dn):
        return ad_remove_members_from_groups(
            self.conn, members_dn, groups_dn, fix=False
        )

    def remove_users_from_groups(
        self, user_instance_list, group_instance_list
    ):
        """ Remove users to groups

            Removes a list of users to the list of groups.

            Args:
                user_instance_list: (:list: of :obj: 'user.user' or inheritor ):
                    the list of instances of user.user or its descendants who
                    should be removed from the ldap groups.
                group_instance_list: (:list: of :obj: 'group.group' or
                    inheritor ): the list of instances of group.group or its
                    descendants in which the users should be removed.
            Returns:
                status: (bool): a boolean where True means that the operation
                    was successful and False means an error has happened
        """
        members_dn = [u.get_dn() for u in user_instance_list]
        group_list = [g.get_dn() for g in group_instance_list]
        return ad_remove_members_from_groups(
            self.conn, members_dn, group_list, fix=True
        )

    def _get_group(self, group_name):
        rez = {}
        attributes = ["cn", "description", "distinguishedName"]
        resp = self.conn.search(
            search_base=self.ldap_domain_name,
            search_filter="(&(objectClass=group)(cn={grp}))".format(
                grp=group_name
            ),
            attributes=attributes,
        )

        if resp == False:
            raise NotFound("Group cn: {grp} not found.".format(grp=group_name))
        else:
            for itm in attributes:
                try:
                    et = getattr(self.conn.entries[0], itm, None)
                except ex.LDAPCursorError:
                    et = None
                if et is None or et.value is None:
                    rez[itm] = ""
                else:
                    rez[itm] = et.value
            return rez

    def get_group(self, group_name, grp_cls_name):
        """ Find the group of the specified class in ldap.

            The group is searched by login in accordance with the specified
            class name.

            Args:
                group_name (str): groupname to search.
                grp_cls_name (str): class name of the group whose instance
                    should return the method ('group', ...).

            Returns:
                group_instance (:obj: 'group' or inheritor ): an instance
                    of the class group or its descendant with source data
                    about the group.

            Raises:
                NotFound: Group is not found.
        """
        rez = {}
        attributes = ["cn", "description", "distinguishedName"]
        resp = self.conn.search(
            search_base=self.ldap_domain_name,
            search_filter="(&(objectClass=group)(cn={grp}))".format(
                grp=group_name
            ),
            attributes=attributes,
        )
        if resp == False:
            raise NotFound("Group cn: {grp} not found.".format(grp=group_name))
        else:
            if not self.conn.entries:
                raise NotFound(
                    "Group cn: {grp} not found.".format(grp=group_name)
                )
            for itm in attributes:
                try:
                    et = getattr(self.conn.entries[0], itm, None)
                except ex.LDAPCursorError:
                    et = None
                if et is None or et.value is None:
                    rez[itm] = ""
                else:
                    rez[itm] = et.value

            mdl = getattr(sys.modules[__name__], grp_cls_name)
            cls = getattr(mdl, grp_cls_name)
            ou = ",".join(rez["distinguishedName"].split(",")[1:])
            cls_vl = {
                "name": group_name,
                "org_unit": ou,
                "description": rez["description"],
            }
            grp = cls(**cls_vl)
            return grp

    def search_groups(self, ldap_filter, grp_cls_name, base=""):
        rez = []
        if base == "":
            base = self.ldap_domain_name

        resp = self.conn.search(
            search_base=base,
            search_filter=ldap_filter,
            search_scope=ldap3.SUBTREE,
            attributes=ldap3.ALL_ATTRIBUTES,
        )

        if resp == False:
            raise OperationFailure(
                "Search failed. Server meseage: {desc} - {msgs}.".format(
                    desc=self.conn.result["description"],
                    msgs=self.conn.result["message"],
                )
            )
        else:
            for itm in self.conn.entries:
                mdl = getattr(sys.modules[__name__], grp_cls_name)
                cls = getattr(mdl, grp_cls_name)
                cls_vl = {}
                for cls_attr, ldap_attr in cls._FIELD_MAP.items():
                    if ldap_attr in itm:
                        l3_attr = getattr(itm, ldap_attr)
                        cls_vl[cls_attr] = (
                            "" if l3_attr.value is None else l3_attr.value
                        )
                DN = str(getattr(itm, "distinguishedName").value)
                CN = str(getattr(itm, "CN").value)
                BASE = DN.replace("CN=" + CN + ",", "")
                cls_vl["org_unit"] = BASE
                grp = cls(**cls_vl)
                rez.append(grp)
            return rez

    def search_groups_p(self, ldap_filter, grp_cls_name, base=""):
        """ Find a groups in ldap by ldap-filter (paged ldap search).

            Groups are searched by ldap filter. The search is made page by page,
            but transparent for use. Suitable for unloading a large number of
            results.

            Args:
                ldap_filter (str): line with ldap request.
                base  (str): ldap base to search for groups.
                grp_cls_name (str): The class name of the group whose
                    instances will be returned.

            Returns:
                group_instance (:list: of :obj: 'group' or inheritor ):
                    a list of instances of group or its descendants with
                    information about ldap groups.

            Raises:
                OperationFailure: Group is not found.

        """
        rez = []
        if base == "":
            base = self.ldap_domain_name

        resp = self.conn.extend.standard.paged_search(
            search_base=base,
            search_filter=ldap_filter,
            attributes=[
                ldap3.ALL_ATTRIBUTES,
                ldap3.ALL_OPERATIONAL_ATTRIBUTES,
            ],
            paged_size=1000,
            generator=True,
        )
        if resp == False:
            raise OperationFailure(
                "Search failed. Server meseage: {desc} - {msgs}.".format(
                    desc=self.conn.result["description"],
                    msgs=self.conn.result["message"],
                )
            )
        else:
            for itm in resp:
                mdl = getattr(sys.modules[__name__], grp_cls_name)
                cls = getattr(mdl, grp_cls_name)
                cls_vl = {}
                if "attributes" in itm:
                    for cls_attr, ldap_attr in list(cls._FIELD_MAP.items()):
                        if ldap_attr in itm["attributes"]:
                            l3_attr = itm["attributes"][ldap_attr]
                            if isinstance(l3_attr, list):
                                cls_vl[cls_attr] = l3_attr[0]
                            else:
                                cls_vl[cls_attr] = l3_attr
                    DN = str(itm["attributes"]["distinguishedName"])
                    CN = str(itm["attributes"]["CN"])
                    BASE = DN.replace("CN=" + CN + ",", "")
                    cls_vl["org_unit"] = BASE
                    grp = cls(**cls_vl)
                    rez.append(grp)
            return rez

    ##    def search_groups_by_description(self, group_description):
    ##        pass

    def _create_group(self, group_name, base, description=""):
        attrs = {}
        attrs["description"] = description

        # иначе сделает группу с sAMAccountName вида $7BF740F8-B40E4A6D1E1105C4
        # а у меня много кода обращающегося к группам по sAMAccountName
        attrs["sAMAccountName"] = group_name
        attrs = dict((k, v) for k, v in attrs.items() if v != "")
        dn = "cn={group_name},{base}".format(group_name=group_name, base=base)
        self.conn.add(dn, object_class=["group", "top"], attributes=attrs)
        if self.conn.result["result"] != 0:
            raise OperationFailure(
                "Can not create group: "
                + "{dn}. Server meseage: {desc} - {msgs}.".format(
                    dn=dn,
                    desc=self.conn.result["description"],
                    msgs=self.conn.result["message"],
                )
            )

    def create_group(self, group_instance):
        """ Creates a group in ldap.

            Args:
                group_instance (:obj: 'group.group' or inheritor ): an instance
                    of the class group.group or its descendant with data about
                    the ldap group.

            Returns:
                None

            Raises:
                OperationFailure: The operation failed.
                WrongParam: The user_instance parameter is not of the correct
                    type.
        """
        if isinstance(group_instance, group.group) or issubclass(
            group_instance.__class__, group.group
        ):
            attrs = {}
            attrs["description"] = group_instance.description

            # иначе сделает группу с sAMAccountName вида
            # $7BF740F8-B40E4A6D1E1105C4
            # а у меня много кода обращающегося к группам по sAMAccountName
            attrs["sAMAccountName"] = group_instance.name
            attrs = dict((k, v) for k, v in attrs.items() if v != "")
            dn = group_instance.get_dn()
            self.conn.add(dn, object_class=["group", "top"], attributes=attrs)
            if self.conn.result["result"] != 0:
                raise OperationFailure(
                    "Can not create group: "
                    + "{dn}. Server meseage: {desc} - {msgs}.".format(
                        dn=dn,
                        desc=self.conn.result["description"],
                        msgs=self.conn.result["message"],
                    )
                )
        else:
            raise WrongParam(
                "Type mismatch for group_instance "
                + "{gi}. It must be the group class instance or its subclass".format(
                    gi=group_instance
                )
            )

    def delete_group(self, group_name):
        """ Removes a group in ldap.

            Args:
                group_name (str): group name in ldap.

            Returns:
                None

            Raises:
                OperationFailure: The operation failed.
                NotFound: When the deleted group is not found.
        """
        dn = self.get_group(group_name, grp_cls_name="group")["dn"]
        self.conn.delete(dn)
        if self.conn.result["result"] != 0:
            raise OperationFailure(
                "Can not delete group: "
                + "{group}. Server meseage: {desc} - {msgs}.".format(
                    group=group_name,
                    desc=self.conn.result["description"],
                    msgs=self.conn.result["message"],
                )
            )

    def rename_group(self, group_name, new_group_name, new_description=""):
        pass  # не сильно то и необходимая ф-я, писать в последную очередь

    def get_ou(self, ou_name, ou_cls_name, base=""):
        """ Find the Organisational Unit of the specified class in ldap.

            The Organisational Unit is searched by name in accordance with the
            specified class name.

            Args:
                ou_name (str): Organisational Unit to search.
                ou_cls_name (str): class name of the Organisational Unit whose
                    instance should return the method ('ou', ...).

            Returns:
                group_instance (:obj: 'ou' or inheritor ): an instance
                    of the class ou or its descendant with source data
                    about the Organisational Unit.

            Raises:
                NotFound: Organisational Unit is not found.
        """
        # имя OU в LDAP не уникально
        rez = []
        # attributes=[u'name',u'description',u'distinguishedName']
        if base == "":
            base = self.ldap_domain_name
        resp = self.conn.search(
            search_base=base,
            search_filter="(&(objectClass=organizationalUnit)"
            + "(name={ou_name}))".format(ou_name=ou_name),
            attributes=ldap3.ALL_ATTRIBUTES,
        )

        if resp == False:
            raise OperationFailure(
                "Search failed. Server meseage: {desc} - {msgs}.".format(
                    desc=self.conn.result["description"],
                    msgs=self.conn.result["message"],
                )
            )
        else:
            mdl = getattr(sys.modules[__name__], ou_cls_name)
            cls = getattr(mdl, ou_cls_name)
            for itm in self.conn.entries:
                cls_vl = {}
                for cls_attr, ldap_attr in cls._FIELD_MAP.items():
                    if ldap_attr in itm:
                        l3_attr = getattr(itm, ldap_attr)
                        cls_vl[cls_attr] = (
                            "" if l3_attr.value is None else l3_attr.value
                        )
                DN = str(getattr(itm, "distinguishedName").value)
                CN = str(getattr(itm, "name").value)
                BASE = DN.replace("OU=" + CN + ",", "", 1)
                cls_vl["org_unit"] = BASE
                ou = cls(**cls_vl)
                rez.append(ou)
            return rez

    def _create_ou(self, ou_name, base, description=""):
        """ Creates an organizational unit.

            Args:
                ou_name (str): The name of the organizational unit in ldap.
                base (str): container to create an organizational unit
                    (eg: 'ou=some_ou,dc=example,dc=com')
                description (str): description of the organizational unit.

            Returns:
                None

            Raises:
                OperationFailure: The operation failed.
        """

        attrs = {}
        attrs["description"] = description
        attrs = dict((k, v) for k, v in attrs.items() if v != "")
        dn = "ou={ou_name},{base}".format(ou_name=ou_name, base=base)
        self.conn.add(
            dn, object_class=["organizationalUnit", "top"], attributes=attrs
        )
        if self.conn.result["result"] != 0:
            raise OperationFailure(
                "Can not create OU: "
                + "{dn}. Server meseage: {desc} - {msgs}.".format(
                    dn=dn,
                    desc=self.conn.result["description"],
                    msgs=self.conn.result["message"],
                )
            )

    def create_ou(self, ou_instance):
        """ Creates an organizational unit.

            Args:
                ou_instance (str): The organizational unit instance ldap.

            Returns:
                None

            Raises:
                OperationFailure: The operation failed.
        """
        if isinstance(ou_instance, ou.ou) or issubclass(
            ou_instance.__class__, ou.ou
        ):
            attrs = {}
            attrs["description"] = ou_instance.description
            attrs["name"] = ou_instance.name
            attrs = dict((k, v) for k, v in attrs.items() if v != "")
            dn = ou_instance.get_dn()
            self.conn.add(
                dn,
                object_class=["organizationalUnit", "top"],
                attributes=attrs,
            )
            if self.conn.result["result"] != 0:
                raise OperationFailure(
                    "Can not create OU: "
                    + "{dn}. Server meseage: {desc} - {msgs}.".format(
                        dn=dn,
                        desc=self.conn.result["description"],
                        msgs=self.conn.result["message"],
                    )
                )

        else:
            raise WrongParam(
                "Type mismatch for ou_instance "
                + "{gi}. It must be the ou class instance ore its subclass".format(
                    gi=ou_instance
                )
            )

    ##    def delete_ou(self, ou_name):
    ##        pass
    ##
    ##    def rename_ou(self, ou_name, new_ou_name, new_description=''):
    ##        pass

    def search_ous(self, ldap_filter, ou_cls_name, base):
        """ Find the Organisational Unit of the specified class in ldap.

            The Organisational Unit is searched by name in accordance with the
            specified class name.

            Args:
                ldap_filter (str): ldap filter.
                ou_cls_name (str): class name of the Organisational Unit whose
                    instance should return the method ('ou', ...).

            Returns:
                group_instance (:obj: 'ou' or inheritor ): an instance
                    of the class ou or its descendant with source data
                    about the Organisational Unit.

            Raises:
                NotFound: Organisational Unit is not found.
        """
        rez = []
        # attributes=[u'name',u'description',u'distinguishedName']
        if base == "":
            base = self.ldap_domain_name
        resp = self.conn.search(
            search_base=base,
            search_filter=ldap_filter,
            attributes=ldap3.ALL_ATTRIBUTES,
        )

        if resp == False:
            raise OperationFailure(
                "Search failed. Server meseage: {desc} - {msgs}.".format(
                    desc=self.conn.result["description"],
                    msgs=self.conn.result["message"],
                )
            )
        else:
            mdl = getattr(sys.modules[__name__], ou_cls_name)
            cls = getattr(mdl, ou_cls_name)
            for itm in self.conn.entries:
                cls_vl = {}
                for cls_attr, ldap_attr in cls._FIELD_MAP.items():
                    if ldap_attr in itm:
                        l3_attr = getattr(itm, ldap_attr)
                        cls_vl[cls_attr] = (
                            "" if l3_attr.value is None else l3_attr.value
                        )
                DN = str(getattr(itm, "distinguishedName").value)
                CN = str(getattr(itm, "name").value)
                BASE = DN.replace("OU=" + CN + ",", "", 1)
                cls_vl["org_unit"] = BASE
                ou = cls(**cls_vl)
                rez.append(ou)
            return rez

    def __del__(self):
        self.conn.unbind()
