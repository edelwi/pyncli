# -*- coding: UTF-8 -*-
# -------------------------------------------------------------------------------
# Name:        ocs API
# Purpose:
#
# Author:      Evgeniy Semenov
#
# Created:     06.12.2018
# Copyright:   (c) Evgeniy Semenov 2018-2019
# Licence:     MIT
# -------------------------------------------------------------------------------
"""This module implements little part of the web API for the NextCloud server.
"""
import logging
import sys
import urllib.parse
import xml.etree.ElementTree as ET
# import types
from collections import OrderedDict
from copy import deepcopy
from datetime import datetime
from urllib.parse import urljoin, urlparse
from xml.etree.ElementTree import ParseError

import requests

from pyncli.ldap.admexept import OperationFailure, WrongParam

logging.getLogger("ocs").addHandler(logging.NullHandler())

PERMISSION_READ = 1
"""int: Read permission """

PERMISSION_UPDATE = 2
"""int: Update permission """

PERMISSION_CREATE = 4
"""int: Create permission """

PERMISSION_DELETE = 8
"""int: Delete permission """

PERMISSION_SHARE = 16
"""int: Share permission """

PERMISSION_ALL = 31
"""int: Shortcut for combinations of all possible permission (full controll) """

PERMISSIONS = {
    "PERMISSION_CREATE": PERMISSION_CREATE,
    "PERMISSION_READ": PERMISSION_READ,
    "PERMISSION_UPDATE": PERMISSION_UPDATE,
    "PERMISSION_DELETE": PERMISSION_DELETE,
    "PERMISSION_SHARE": PERMISSION_SHARE,
    # 'PERMISSION_ALL':PERMISSION_ALL
}
"""Dict: Permissions and its values """

MUL = OrderedDict(
    [
        ("k", 1024),
        ("m", 1024 * 1024),
        ("g", 1024 * 1024 * 1024),
        ("t", 1024 * 1024 * 1024 * 1024),
    ]
)
"""OrderedDict: Quota size multiplicators an its values. """

CLS_MAP = {"ocs": "Ocs", "groupfolders": "GroupFolderMixin"}
"""Dict: Relations of the cloud applications to class mixin. """


def human_size(size_in_bytes):
    """Get size in kilo,Mega,Giga... bytes.
    """
    try:
        size_in_bytes = int(size_in_bytes)
    except:
        return None  # size_in_bytes
    if size_in_bytes <= MUL[next(iter(MUL))]:
        return str(size_in_bytes)
    else:
        for k, v in MUL.items():
            vl = size_in_bytes / v
            if vl <= MUL[next(iter(MUL))]:
                return "{vl:.2f}{m}".format(vl=vl, m=k)
        return "{vl:.2f}{m}".format(vl=vl, m=k)


def human_permissions(permissions, short=False):
    """Get permissions in readable form.
    """
    try:
        permissions = int(permissions)
    except:
        return None
    if permissions > sum(PERMISSIONS.values()) or permissions < min(
            PERMISSIONS.values()
    ):
        return ""
    rez = []
    for k, v in PERMISSIONS.items():
        if permissions & v == v:
            rez.append(k)
    if short:
        return "".join(((x.split("_")[1][:1]).lower() for x in rez))
    else:
        return " | ".join(rez)


class Comparer(object):
    """
        Mixin class to add compare methods
    """

    def __getitem__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        else:
            return False

    def __eq__(self, instance):
        if type(instance) is not self.__class__:
            return False
        for (key, value) in list(self.__dict__.items()):
            if self.__getitem__(key) != instance.__getitem__(key):
                return False
        return True

    def __ne__(self, instance):
        return not self.__eq__(instance)


class GroupMembers(Comparer):
    """
        GroupMembers class
    """

    def __init__(self, user_id):
        self.user_id = user_id

    def __str__(self):
        return "user_id: {id}".format(id=self.user_id)


class CreateGroupFolder(Comparer):
    """
        CreateGroupFolder class
    """

    def __init__(self, id):
        self.id = id

    def __str__(self):
        return "<CreateGroupFolder> id: {id}".format(id=self.id)


class Group(Comparer):
    """
        Group class
    """

    def __init__(self, group_id=None, permissions=None):
        self.group_id = group_id
        try:
            self.permissions = int(permissions)
        except (ValueError, TypeError):
            # raise WrongParam("Invalid permissions: {p}".format(p=permissions))
            self.permissions = None

    def __str__(self):
        return '<Group> "{gr}" [{per}]'.format(
            gr=self.group_id,
            per=human_permissions(self.permissions, short=True),
        )

    @property
    def info(self):
        return '<Group> "{gr}"'.format(gr=self.group_id)


class GroupFolder(Comparer):
    """
        GroupFolder class
    """

    def __init__(
            self, id=None, mount_point=None, groups=None, quota=None, size=None,
            **kwargs
    ):
        self.id = id
        self.mount_point = mount_point
        self.groups = [x for x in groups] if groups else []
        self.quota = quota
        self.size = size

    def __str__(self):
        out = '<GroupFolder> ({id}) "{mp}" quota: {q}, size: {s}\n'.format(
            mp=self.mount_point,
            id=self.id,
            q=human_size(self.quota),
            s=human_size(self.size),
        )
        for it in self.groups:
            out += "  {grp}\n".format(grp=it.__str__())
        else:
            out = out[:-1]
        return out


class AppInfo(Comparer):
    """
        AppInfo class, contains detailed information about application.
    """

    def __init__(
            self,
            id,
            info=None,
            remote={},
            public=None,
            name=None,
            description=None,
            licence=None,
            author=None,
            require=None,
            shipped=None,
            standalone=None,
            default_enable=None,
            types=[]
    ):
        self.id = id
        self.info = info
        self.remote = remote
        self.public = public
        self.name = name
        self.description = description
        self.licence = licence
        self.author = author
        self.require = require
        self.shipped = shipped
        self.standalone = standalone
        self.default_enable = default_enable
        self.types = types

    def __str__(self):
        out = '<AppInfo> ({id}) "{name}" author: {a}, licence: {lic}\n'.format(
            name=self.name,
            id=self.id,
            a=self.author,
            lic=self.licence,
        )
        out += "  description: {dsc}\n".format(dsc=self.description)
        out += "  require: {r}, shipped: {s}, standalone: {sa}\n".format(
            r=self.require,
            sa=self.standalone,
            s=self.shipped
        )
        out += "  default_enable: {de}, public: {pub}, remote: ({rem})\n".format(
            de=self.default_enable,
            pub=self.public,
            rem=', '.join(
                ['{0}: "{1}"'.format(k, v) for k, v in self.remote.items()]
            )
        )
        out += "  types: {tps}, info: {inf}".format(
            tps=', '.join(self.types),
            inf=self.info
        )
        return out


class User(Comparer):
    """
        NextCloud User
    """

    def __init__(
            self,
            id=None,
            enabled=None,
            storageLocation=None,
            lastLogin=None,
            backend=None,
            subadmin=None,
            quota=None,
            email=None,
            displayname=None,
            phone=None,
            address=None,
            website=None,
            twitter=None,
            groups=None,
            language=None,
            locale=None,
            backendCapabilities=None,
    ):

        self.id = id
        self.enabled = bool(enabled)
        self.storage_location = storageLocation
        if lastLogin == "0" or lastLogin == 0:
            self.last_login = datetime(1970, 1, 1, 0, 0)
        else:
            try:
                self.last_login = datetime.fromtimestamp(int(lastLogin) / 1e3)
            except:
                self.last_login = datetime(1970, 1, 1, 0, 0)
        self.backend = backend
        # TODO: add check
        self.subadmin = subadmin
        # TODO: add check
        self.quota = quota
        self.email = email
        self.displayname = displayname
        self.phone = phone
        self.address = address
        self.website = website
        self.twitter = twitter
        # TODO: add check
        self.groups = groups
        self.language = language
        self.locale = locale
        # TODO: add check
        self.backend_capabilities = backendCapabilities  # !

    def __str__(self):
        out = '<User> ({id}) "{dn}" enabled: {en}, e-mail: {em}\n'.format(
            dn=self.displayname, id=self.id, en=self.enabled, em=self.email
        )
        out += "\tbackend: {bk}, storage location: {pt}, last logon: {ll}\n".format(
            bk=self.backend,
            pt=self.storage_location,
            ll=self.last_login.replace(microsecond=0).isoformat(),
        )
        out += "\tquota: {q}".format(q=self.quota)
        out += "\tphone: {ph}, twitter: {tw}, website: {www}\n".format(
            ph=self.phone, tw=self.twitter, www=self.website
        )
        out += "\taddress: {address}\n".format_map(self.__dict__)
        out += "\tlanguage: {language}, locale: {locale}\n".format_map(
            self.__dict__
        )
        for itm in self.groups:
            if itm.group_id in self.subadmin:
                out += "\t" + itm.info + " [Subadmin]\n"
            else:
                out += "\t" + itm.info + "\n"
        out += "\t{backend}".format(backend=self.backend_capabilities)
        return out


class UserQuota(Comparer):
    """
        NextCloud user quota class
    """

    def __init__(self, quota, used=0, free=None, total=None, relative=None):
        try:
            self.quota = int(quota)
        except ValueError as e:
            self.quota = -3
        self.used = int(used)
        self.free = free
        self.total = total
        self.relative = relative

    def __str__(self):
        out = "Quota: {quota}, used: {used}".format(
            quota=human_size(self.quota), used=human_size(self.used)
        )
        if self.free:
            out += ", free: {free}".format(free=human_size(int(self.free)))
        if self.total:
            out += ", total: {total}".format(total=human_size(int(self.total)))
        if self.relative:
            out += ", relative: {relative}".format(relative=self.relative)
        return out + "\n"


class BackendCapabilities(Comparer):
    """
        NectCloud BackendCapabilities class
    """

    def __init__(self, setDisplayName=None, setPassword=None):
        self.set_display_name = bool(setPassword)
        self.set_password = bool(setPassword)

    def __str__(self):
        out = "<BackendCapabilities> setDisplayName: {dn},  setPassword: {p}"
        return out.format(dn=self.set_display_name, p=self.set_password)


class OcsXmlResponse(object):
    """NextCloud answer parser class."""

    _SUPPORTED_CLASS_NAMES = [
        "GroupFolder",
        "Group",
        "CreateGroupFolder",
        "GroupMembers",
        "User",
        "Apps",
        "Subadmins",
        "AppInfo"
    ]

    def __init__(self, xml_text, data_class_name=None):
        """Parsing xml response NextCloud server.

        Args:
            xml_text (str): XML string from NextCloud server.
            data_class_name (str): Allows you to determine the content type of
                the response.

        Raises:
            WrongParam: The instance parameter is not of the correct
            type.

        """
        if (
                data_class_name is not None
                and data_class_name not in self._SUPPORTED_CLASS_NAMES
        ):
            raise WrongParam(
                "Unsupported class name: {cls}".format(cls=data_class_name)
            )
        if not isinstance(xml_text, str):
            raise WrongParam(
                "Invalid xml_text parameter type: {t}".format(t=type(xml_text))
            )
        try:
            self.respose = ET.fromstring(xml_text)
        except ParseError as e:
            raise WrongParam(
                "Invalid xml_text parameter value. XML Parse Error."
            )
        self.status = (
            self.respose.find(".//meta/status").text
            if self.respose.find(".//meta/status") is not None
            else "unknown"
        )
        self.statuscode = (
            self.respose.find(".//meta/statuscode").text
            if self.respose.find(".//meta/statuscode") is not None
            else "unknown"
        )
        self.message = (
            self.respose.find(".//meta/message").text
            if self.respose.find(".//meta/message") is not None
            else "unknown"
        )

        self.data_class_name = data_class_name
        if self.statuscode != "100":
            return

        parser = self.get_parser(data_class_name)
        if parser is not None:
            self.data = parser(self.respose)
        else:
            self.data = []

    @staticmethod
    def get_parser(data_class_name):
        if data_class_name == "GroupFolder":
            return OcsXmlResponse._parse_group_folder
        elif data_class_name == "Group":
            return OcsXmlResponse._parse_group
        elif data_class_name == "CreateGroupFolder":
            return OcsXmlResponse._parse_create_group_folder
        elif data_class_name == "GroupMembers":
            return OcsXmlResponse._parse_group_members
        elif data_class_name == "User":
            return OcsXmlResponse._parse_user
        elif data_class_name == "Apps":
            return OcsXmlResponse._parse_apps
        elif data_class_name == "Subadmins":
            return OcsXmlResponse._parse_subadmins
        elif data_class_name == "AppInfo":
            return OcsXmlResponse._parse_app_info

    @staticmethod
    def _parse_group_folder(et_object):
        result = []
        data = et_object.findall(".//data/element")
        if data:
            for element in data:
                group_folder = {}
                for subelement in element.getchildren():
                    sub = subelement.getchildren()
                    groups = []
                    if sub:
                        for item in sub:
                            groups.append(Group(**item.attrib))
                        group_folder["groups"] = groups
                    else:
                        group_folder[subelement.tag] = subelement.text
                result.append(GroupFolder(**group_folder))
        else:
            data = et_object.find(".//data")
            group_folder = {}
            for subelement in data:
                sub = subelement.getchildren()
                groups = []
                if sub:
                    for item in sub:
                        groups.append(Group(**item.attrib))
                    group_folder["groups"] = groups
                else:
                    group_folder[subelement.tag] = subelement.text
            result.append(GroupFolder(**group_folder))
        return result

    @staticmethod
    def _parse_group(et_object):
        result = []
        data = et_object.findall(".//data/groups/element")
        for element in data:
            result.append(Group(group_id=element.text))
        return result

    @staticmethod
    def _parse_create_group_folder(et_object):
        result = []
        data = et_object.findall(".//data/id")
        result.append(CreateGroupFolder(id=data[0].text))
        return result

    @staticmethod
    def _parse_group_members(et_object):
        result = []
        data = et_object.findall(".//data/users/element")
        for element in data:
            result.append(GroupMembers(user_id=element.text))
        return result

    @staticmethod
    def _parse_user(et_object):
        result = []
        data = et_object.find(".//data")
        user = {}
        for subelement in data:
            sub = subelement.getchildren()
            groups = []
            if subelement.tag == "groups":
                for item in sub:
                    groups.append(Group(group_id=item.text))
                user["groups"] = groups
            elif subelement.tag == "quota":
                quota = {}
                for item in sub:
                    quota[item.tag] = item.text
                user["quota"] = UserQuota(**quota)
            elif subelement.tag == "subadmin":
                subadmins = []
                for item in sub:
                    subadmins.append(item.text)
                user["subadmin"] = subadmins
            elif subelement.tag == "backendCapabilities":
                backend = {}
                for item in sub:
                    backend[item.tag] = item.text
                user["backendCapabilities"] = BackendCapabilities(**backend)
            else:
                user[subelement.tag] = subelement.text
        result.append(User(**user))
        return result

    @staticmethod
    def _parse_apps(et_object):
        result = []
        data = et_object.findall(".//data/apps/element")
        for element in data:
            result.append(element.text)
        return result

    @staticmethod
    def _parse_subadmins(et_object):
        result = []
        data = et_object.findall(".//data/element")
        for element in data:
            result.append(element.text)
        return result

    @staticmethod
    def _parse_app_info(et_object):
        result = []
        data = et_object.find(".//data")
        app_info = {}
        for subelement in data:
            sub = subelement.getchildren()
            types = []
            if subelement.tag == "types":
                for item in sub:
                    types.append(item.text)
                app_info["types"] = types
            elif subelement.tag == "remote":
                remote = {}
                for item in sub:
                    remote[item.tag] = item.text
                app_info["remote"] = remote
            else:
                app_info[subelement.tag] = subelement.text
        result.append(AppInfo(**app_info))
        return result

    def get_status(self):
        return "Status: {s}, code: {c}, message: {m}".format(
            s=self.status, c=self.statuscode, m=self.message
        )

    def __str__(self):
        out = "<OcsXmlResponse> {status} ({code}): {msg}\n".format(
            status=self.status, code=self.statuscode, msg=self.message
        )
        for d in self.data:
            out += "{data}\n".format(data=d.__str__())
        return out


class GroupFolderMixin(object):
    """
        GroupFolder Mixin for Ocs class
    """

    URL_FOLDERS = "index.php/apps/groupfolders/folders"

    def set_group_folder_quota(self, gfolder_id, quota_bites):
        """Set quota for group folder.

        Sets a quota for the specified group folder.

        Args:
            gfolder_id (int): Group Folder ID (this is a number!).
            quota_bites (int): The quota applied to this folder (in bytes,
                -3 - unlimited).

        Raises:
            OperationFailure: The operation failed.
        """
        resp = self.post_data(
            self.URL_FOLDERS
            + "/{gfolder_id}/quota".format(gfolder_id=gfolder_id),
            {"quota": quota_bites},
        )
        x = OcsXmlResponse(resp)
        if x.statuscode != "100":
            Ocs.logger.exception(
                "An exception was caught in Ocs.set_group_folder_quota due to "
                + "negative server response code: {q}".format(q=x.get_status())
            )
            raise OperationFailure(
                "Ocs.set_group_folder_quota response:{e}".format(
                    e=x.get_status()
                )
            )

    def set_group_folder_group_permissions(
            self, gfolder_id, group_id, permissions
    ):
        """Set permissions for group folder per group.

        Sets permissions for the specified group folder for this group.

        Args:
            gfolder_id (int): Group Folder ID (this is a number!).
            group_id (str): Group ID (group name).
            permissions (byte): Permissions bitmap:
                PERMISSION_CREATE = 4
                PERMISSION_READ = 1
                PERMISSION_UPDATE = 2
                PERMISSION_DELETE = 8
                PERMISSION_SHARE = 16
                PERMISSION_ALL = 31

        Raises:
            OperationFailure: The operation failed.
        """
        resp = self.post_data(
            self.URL_FOLDERS
            + "/{gfolder_id}/groups/{group_id}".format(
                gfolder_id=gfolder_id, group_id=group_id
            ),
            {"permissions": permissions},
        )
        x = OcsXmlResponse(resp)
        if x.statuscode != "100":
            Ocs.logger.exception(
                "An exception was caught in Ocs.set_group_folder_group_permissions"
                + " due to negative server response code: {q}".format(
                    q=x.get_status()
                )
            )
            raise OperationFailure(
                "Ocs.set_group_folder_group_permissions response:{e}".format(
                    e=x.get_status()
                )
            )

    def grant_access_to_group_folder(self, gfolder_id, group_id):
        """Grant access to the group folder for the group.

        Grants the specified group access to the specified group folder.

        Args:
            gfolder_id (int): Group Folder ID (this is a number!).
            group_id (str): Group ID (group name).

        Raises:
            OperationFailure: The operation failed.
        """
        resp = self.post_data(
            self.URL_FOLDERS
            + "/{gfolder_id}/groups".format(gfolder_id=gfolder_id),
            {"group": group_id},
        )
        x = OcsXmlResponse(resp)
        if x.statuscode != "100":
            Ocs.logger.exception(
                "An exception was caught in Ocs.grant_access_to_group_folder"
                + " due to negative server response code: {q}".format(
                    q=x.get_status()
                )
            )
            raise OperationFailure(
                "Ocs.grant_access_to_group_folder response:{e}".format(
                    e=x.get_status()
                )
            )

    def revoke_access_to_group_folder(self, gfolder_id, group_id):
        """Revoke group folder access for group.

        Stops the specified group access to the specified group folder.

        Args:
            gfolder_id (int): Group Folder ID (this is a number!).
            group_id (str): Group ID (group name).

        Raises:
            OperationFailure: The operation failed.
        """
        resp = self.delete_data(
            self.URL_FOLDERS
            + "/{gfolder_id}/groups/{group_id}".format(
                group_id=group_id, gfolder_id=gfolder_id
            ),
            {},
        )
        x = OcsXmlResponse(resp)
        if x.statuscode != "100":
            Ocs.logger.exception(
                "An exception was caught in Ocs.revoke_access_to_group_folder"
                + " due to negative server response code: {q}".format(
                    q=x.get_status()
                )
            )
            raise OperationFailure(
                "Ocs.revoke_access_to_group_folder response:{e}".format(
                    e=x.get_status()
                )
            )

    def rename_group_folder(self, gfolder_id, new_name):
        """Rename group folder.

        Renames the specified group folder.

        Args:
            gfolder_id (int): Group Folder ID (this is a number!).
            new_name (str): New folder name (mountpoint).

        Raises:
            OperationFailure: The operation failed.
        """
        resp = self.post_data(
            self.URL_FOLDERS
            + "/{gfolder_id}/mountpoint".format(gfolder_id=gfolder_id),
            {"mountpoint": new_name},
        )
        x = OcsXmlResponse(resp)
        if x.statuscode != "100":
            Ocs.logger.exception(
                "An exception was caught in Ocs.rename_group_folder"
                + " due to negative server response code: {q}".format(
                    q=x.get_status()
                )
            )
            raise OperationFailure(
                "Ocs.rename_group_folder response:{e}".format(e=x.get_status())
            )

    def new_group_folder(self, mountpoint):
        """Create a group folder.

        Creates the specified group folder.

        Args:
            mountpoint (str): Folder name.

        Returns:
            int: ID of the created folder.

        Raises:
            OperationFailure: The operation failed.
        """
        resp = self.post_data(self.URL_FOLDERS, {"mountpoint": mountpoint})
        x = OcsXmlResponse(resp, data_class_name="CreateGroupFolder")
        if x.statuscode != "100":
            Ocs.logger.exception(
                "An exception was caught in Ocs.new_group_folder"
                + " due to negative server response code: {q}".format(
                    q=x.get_status()
                )
            )
            raise OperationFailure(
                "Ocs.new_group_folder response:{e}".format(e=x.get_status())
            )
        return x.data[0].id

    def remove_group_folder(self, gfolder_id):
        """Deletes a group folder.

        Deletes the specified group folder. The operation can not be canceled!

        Args:
            gfolder_id (int): Group Folder ID (this is a number!).

        Raises:
            OperationFailure: The operation failed.
        """
        resp = self.delete_data(
            self.URL_FOLDERS + "/{gfolder_id}".format(gfolder_id=gfolder_id),
            {},
        )
        x = OcsXmlResponse(resp)
        if x.statuscode != "100":
            Ocs.logger.exception(
                "An exception was caught in Ocs.remove_group_folder"
                + " due to negative server response code: {q}".format(
                    q=x.get_status()
                )
            )
            raise OperationFailure(
                "Ocs.remove_group_folder response:{e}".format(e=x.get_status())
            )

    def get_group_folders(self):
        """Group Folders

        Returns all group folders.

        Returns:
            (:obj: list of GroupFolder): List of GroupFolder instances.

        Raises:
            OperationFailure: The operation failed.
        """
        resp = self.get_data(self.URL_FOLDERS)
        x = OcsXmlResponse(resp, "GroupFolder")
        if x.statuscode != "100":
            Ocs.logger.exception(
                "An exception was caught in Ocs.get_group_folders"
                + " due to negative server response code: {q}".format(
                    q=x.get_status()
                )
            )
            raise OperationFailure(
                "Ocs.get_group_folders response:{e}".format(e=x.get_status())
            )
        return x.data

    def get_group_folder(self, gfolder_id):
        """Group Folder.

        Returns information about the specified group folder.

        Args:
            gfolder_id (int): Group Folder ID (this is a number!).

        Returns:
            (:obj: GroupFolder): GroupFolder instance.

        Raises:
            OperationFailure: The operation failed.
        """
        resp = self.get_data(self.URL_FOLDERS + "/{id}".format(id=gfolder_id))
        x = OcsXmlResponse(resp, "GroupFolder")
        if x.statuscode != "100":
            Ocs.logger.exception(
                "An exception was caught in Ocs.get_group_folder"
                + " due to negative server response code: {q}".format(
                    q=x.get_status()
                )
            )
            raise OperationFailure(
                "Ocs.get_group_folder response:{e}".format(e=x.get_status())
            )
        return x.data[0]

    def batch_new_group_folder(self, group_folder_obj):
        """Batch create group folder.

        Creates a group folder, creates all groups from a group folder instance,
        sets permissions for groups, associates groups with a group folder, and
        set the quota for the group folder.

        Args:
            group_folder_obj (:obj: GroupFolder): Group Folder instance.

        Returns:
            None.

        Raises:
            OperationFailure: The operation failed.
        """
        Ocs.logger.info("Batch create group folder.")

        Ocs.logger.info(
            "Creates a group folder {mp}.".format(
                mp=group_folder_obj.mount_point
            )
        )
        try:
            # 1 folder
            fid = self.new_group_folder(group_folder_obj.mount_point)
            group_folder_obj.id = fid
            Ocs.logger.debug(
                "Created group folder {mp}.".format(mp=group_folder_obj)
            )

            for grp in group_folder_obj.groups:
                # 2 add group
                Ocs.logger.debug(
                    "Create a group {mp}.".format(mp=grp.group_id)
                )
                self.new_group(grp.group_id)

                # 3 add permissions
                Ocs.logger.debug(
                    "Add group {g} permissions {r} ".format(
                        g=grp.group_id, r=grp.permissions
                    )
                    + "to group folder {p} ({id}).".format(
                        p=group_folder_obj.mount_point, id=group_folder_obj.id
                    )
                )
                self.set_group_folder_group_permissions(
                    group_folder_obj.id, grp.group_id, grp.permissions
                )

                # 4 link group
                Ocs.logger.debug(
                    "Grants group {g} access".format(g=grp.group_id)
                    + " to the group folder {p} ({id}).".format(
                        p=group_folder_obj.mount_point, id=group_folder_obj.id
                    )
                )
                self.grant_access_to_group_folder(
                    group_folder_obj.id, grp.group_id
                )

            # 5 add quota
            Ocs.logger.debug(
                "Sets the quota {q}".format(q=group_folder_obj.quota)
                + " to the group folder {p} ({id}).".format(
                    p=group_folder_obj.mount_point, id=group_folder_obj.id
                )
            )
            self.set_group_folder_quota(
                group_folder_obj.id, group_folder_obj.quota
            )
        except OperationFailure as e:
            Ocs.logger.exception(
                "Exception in Ocs.batch_new_group_folder {e}".format(e=e.value)
            )


class Base(object):
    pass


class Ocs(Base):
    """
        Class wrapper over ocs.
        Dynamically expandable class.
    """

    URL_GROUPS = "ocs/v1.php/cloud/groups"
    URL_USERS = "ocs/v1.php/cloud/users"
    URL_USER_SEARCH = "ocs/v1.php/cloud/users?search="
    URL_APPS = "ocs/v1.php/cloud/apps"

    logger = logging.getLogger("ocs")

    def __init__(self, cloud_user, cloud_user_pwd, cloud_URL):
        """Constructor.

        Args:
            cloud_user (str): Cloud user name (administrator),
            cloud_user_pwd (str): Cloud user password,
            cloud_URL (str): Cloud URL (for example
                https://cloud.example.com),

        Raises:
            OperationFailure: The operation failed.
        """
        if not cloud_user:
            raise OperationFailure("Not specified value cloud_user.")
        else:
            self.cl_user = cloud_user

        if not cloud_user_pwd:
            raise OperationFailure("Not specified value cloud_user_pwd.")
        else:
            self.cl_user_pwd = cloud_user_pwd

        if not cloud_URL:
            raise OperationFailure("Not specified value cloud_URL.")
        else:
            self.cloud_url = urlparse(cloud_URL)

        self.headers = {"OCS-APIRequest": "true"}

        self.client = requests.session()

        self._apps = self.get_apps()
        self._apps.append("ocs")

        available_classes = set(CLS_MAP.keys())
        to_mix = set(self._apps).intersection(available_classes)
        if to_mix:
            re_mix = tuple(
                getattr(sys.modules[__name__], class_name)
                for class_name in (CLS_MAP[x] for x in to_mix)
            )
            self.__class__ = type("OcsMix", re_mix, {})

    def get_data(self, url_path):
        """Run a GET request to the cloud.

        Performs a GET request to the cloud on a partial path (without the base
        part).

        Args:
            url_path (str): The request address without the base part.

        Returns:
            str: Server response text (xml).

        Raises:
            OperationFailure: The operation failed.
        """
        try:
            url = urljoin(self.cloud_url.geturl(), url_path)
            Ocs.logger.debug(
                "Trying to execute a GET request: {q}".format(q=url)
            )
            self.client.get(url)
            response = requests.get(
                url,
                auth=requests.auth.HTTPBasicAuth(
                    self.cl_user, self.cl_user_pwd
                ),
                headers=self.headers,
            )
            Ocs.logger.debug(
                "Server response received: {q}".format(q=response.text)
            )
            return response.text
        except IOError as e:
            Ocs.logger.exception(
                "Intercepted exception in Ocs.get_data: {q}. Escalate.".format(
                    q=e
                )
            )
            raise OperationFailure("Ocs.get_data error:{e}".format(e=e))

    def post_data(self, url_path, data_js):
        """Run a POST request to the cloud.

        Performs a POST request to the cloud on a partial path (without the base
        part).

        Args:
            url_path (str): The request address without the base part.
            data_js (json): Request payload.

        Returns:
            str: Server response text (xml).

        Raises:
            OperationFailure: The operation failed.
        """
        ##        header_add={'Content-Type':'application/x-www-form-urlencoded'}
        ##        headers= deepcopy( self.headers )
        ##        headers.update(header_add)
        try:
            url = urljoin(self.cloud_url.geturl(), url_path)
            Ocs.logger.debug(
                "Trying to execute a POST request: "
                + "{q}, payload: {d}".format(q=url, d=data_js)
            )
            response = requests.post(
                url,
                json=data_js,
                auth=requests.auth.HTTPBasicAuth(
                    self.cl_user, self.cl_user_pwd
                ),
                headers=self.headers,
            )
            Ocs.logger.debug(
                "Server response received: {q}".format(q=response.text)
            )
            return response.text
        except IOError as e:
            Ocs.logger.exception(
                "Intercepted exception in Ocs.post_data:"
                + " {q}. Escalate.".format(q=e)
            )
            raise OperationFailure("Ocs.post_data error:{e}".format(e=e))

    def delete_data(self, url_path, data_js={}):
        """Run a DELETE request to the cloud.

        Performs a DELETE request to the cloud on a partial path (without the
        base part).

        Args:
            url_path (str): The request address without the base part.
            data_js (json): Request payload (default is empty json).

        Returns:
            str: Server response text (xml).

        Raises:
            OperationFailure: The operation failed.
        """
        try:
            url = urljoin(self.cloud_url.geturl(), url_path)
            Ocs.logger.debug(
                "Trying to execute a DELETE request: "
                + "{q}, payload: {d}".format(q=url, d=data_js)
            )
            response = requests.delete(
                url,
                json=data_js,
                auth=requests.auth.HTTPBasicAuth(
                    self.cl_user, self.cl_user_pwd
                ),
                headers=self.headers,
            )
            Ocs.logger.debug(
                "Server response received: {q}".format(q=response.text)
            )
            return response.text
        except IOError as e:
            Ocs.logger.exception(
                "Intercepted exception in Ocs.delete_data:"
                + " {q}. Escalate.".format(q=e)
            )
            raise OperationFailure("Ocs.delete_data error:{e}".format(e=e))

    def put_data(self, url_path, data_js={}):
        """Run a PUT request to the cloud.

        Performs a PUT request to the cloud on a partial path (without the
        base part).

        Args:
            url_path (str): The request address without the base part.
            data_js (json): Request payload (default is empty json).

        Returns:
            str: Server response text (xml).

        Raises:
            OperationFailure: The operation failed.
        """
        header_add = {"Content-Type": "application/x-www-form-urlencoded"}
        headers = deepcopy(self.headers)
        headers.update(header_add)
        try:
            url = urljoin(self.cloud_url.geturl(), url_path)
            Ocs.logger.debug(
                "Trying to execute a PUT request: "
                + "{q}, payload: {d}".format(q=url, d=data_js)
            )
            response = requests.put(
                url,
                data=data_js,
                auth=requests.auth.HTTPBasicAuth(
                    self.cl_user, self.cl_user_pwd
                ),
                headers=headers,
            )
            Ocs.logger.debug(
                "Server response received: {q}".format(q=response.text)
            )
            return response.text
        except IOError as e:
            Ocs.logger.exception(
                "Intercepted exception in Ocs.put_data:"
                + " {q}. Escalate.".format(q=e)
            )
            raise OperationFailure("Ocs.put_data error:{e}".format(e=e))

    def get_apps(self, filter='enabled'):
        """Applications.

        Get list of installed applications.

        Args:
            filter (str): Filter by application accessibility:
                'enabled' - filter by enabled application,
                'disabled' - filter by disabled application,
                'nofilter' - unfiltered applications.

        Returns:
            list: List of applications name.

        Raises:
            OperationFailure: The operation failed.
        """
        if filter == 'enabled':
            resp = self.get_data(self.URL_APPS + '?filter=enabled')
        elif filter == 'disabled':
            resp = self.get_data(self.URL_APPS + '?filter=disabled')
        elif filter == 'nofilter':
            resp = self.get_data(self.URL_APPS)

        x = OcsXmlResponse(resp, "Apps")
        if x.statuscode != "100":
            Ocs.logger.exception(
                "Fire exeption Ocs.get_apps"
                + " due to negative server response code: {q}".format(
                    q=x.get_status()
                )
            )
            raise OperationFailure(
                "Ocs.get_apps response:{e}".format(e=x.get_status())
            )
        return x.data

    def get_app_info(self, app_id):
        """Application information.

        Get detailed information about installed application.

        Args:
            app_id (str): Application ID.

        Returns:
            (:obj: AppInfo): NextCloud application object.

        Raises:
            OperationFailure: The operation failed.
        """
        resp = self.get_data(self.URL_APPS + "/{id}".format(id=app_id))
        x = OcsXmlResponse(resp, "AppsInfo")
        if x.statuscode != "100":
            Ocs.logger.exception(
                "Fire exeption Ocs.get_app_info"
                + " due to negative server response code: {q}".format(
                    q=x.get_status()
                )
            )
            raise OperationFailure(
                "Ocs.get_app_info response:{e}".format(e=x.get_status())
            )
        return x.data

    def get_groups(self):
        """Groups.

        Returns all cloud groups.

        Returns:
            (:obj: list of Group): List of group objects.

        Raises:
            OperationFailure: The operation failed.
        """
        resp = self.get_data(self.URL_GROUPS)
        x = OcsXmlResponse(resp, "Group")
        if x.statuscode != "100":
            Ocs.logger.exception(
                "An exception was caught in Ocs.get_groups"
                + " due to negative server response code: {q}".format(
                    q=x.get_status()
                )
            )
            raise OperationFailure(
                "Ocs.get_groups response:{e}".format(e=x.get_status())
            )
        return x.data

    def add_user_to_group(self, user_id, group_id):
        """Add user to group.

        Adds a user with user_id to group group_id.

        Args:
            user_id (str): The user ID of the cloud (like bill or
                bill@example.com when ldap backend used).
            group_id (str): Group ID (group name).

        Raises:
            OperationFailure: The operation failed.
        """
        resp = self.post_data(
            self.URL_USERS + "/{user_id}/groups".format(user_id=user_id),
            {"groupid": group_id},
        )
        cloud_answer = OcsXmlResponse(resp)
        fail_reason = ''
        if cloud_answer.statuscode == '100':
            return  # successful
        elif cloud_answer.statuscode == '101':
            fail_reason = 'no group specified'
        elif cloud_answer.statuscode == '102':
            fail_reason = 'group does not exist'
        elif cloud_answer.statuscode == '103':
            fail_reason = 'user does not exist'
        elif cloud_answer.statuscode == '104':
            fail_reason = 'insufficient privileges'
        elif cloud_answer.statuscode == '105':
            fail_reason = 'failed to add user to group'
        else:
            fail_reason = 'unknown error'

        Ocs.logger.error(
            "An exception was caught in Ocs.add_user_to_group due to "
            + "negative server response code: {code} - {reason}".format(
                code=cloud_answer.statuscode,
                reason=fail_reason
            )
        )
        raise OperationFailure(
            "Ocs.add_user_to_group response: Error: {code} - {reaon}".format(
                code=cloud_answer.statuscode,
                reason=fail_reason
            )
        )

    def remove_user_from_group(self, user_id, group_id):
        """Remove user from group.

        Removes the user with user_id from group group_id.

        Args:
            user_id (str): The user ID of the cloud (like bill or
                bill@example.com when ldap backend used).
            group_id (str): Group ID (group name).

        Raises:
            OperationFailure: The operation failed.
        """
        resp = self.delete_data(
            self.URL_USERS + "/{user_id}/groups".format(user_id=user_id),
            {"groupid": group_id},
        )
        cloud_answer = OcsXmlResponse(resp)
        fail_reason = ''
        if cloud_answer.statuscode == '100':
            return  # successful
        elif cloud_answer.statuscode == '101':
            fail_reason = 'no group specified'
        elif cloud_answer.statuscode == '102':
            fail_reason = 'group does not exist'
        elif cloud_answer.statuscode == '103':
            fail_reason = 'user does not exist'
        elif cloud_answer.statuscode == '104':
            fail_reason = 'insufficient privileges'
        elif cloud_answer.statuscode == '105':
            fail_reason = 'failed to remove user from group'
        else:
            fail_reason = 'unknown error'

        Ocs.logger.error(
            "An exception was caught in Ocs.remove_user_from_group due to "
            + "negative server response code: {code} - {reason}".format(
                code=cloud_answer.statuscode,
                reason=fail_reason
            )
        )
        raise OperationFailure(
            "Ocs.remove_user_from_group Error: {code} - {reaon}".format(
                code=cloud_answer.statuscode,
                reason=fail_reason
            )
        )

    def new_user(self, userid, password, groups=[]):
        """To create a new user.

        Creates a user in the cloud with the login of user id and password.
        Optional Inputs user into specified groups.

        Args:
            userid (str): username
            password (str): password
            groups (list): List of Group ID (group name).

        Raises:
            OperationFailure: The operation failed.
        """
        if groups:
            resp = self.post_data(
                self.URL_USERS,
                {"userid": userid, "password": password, "groups": groups},
            )
        else:
            resp = self.post_data(
                self.URL_USERS, {"userid": userid, "password": password}
            )

        x = OcsXmlResponse(resp)
        if x.statuscode != "100":
            Ocs.logger.exception(
                "An exception was caught in Ocs.new_user due to "
                + "negative server response code: {q}".format(q=x.get_status())
            )
            raise OperationFailure(
                "Ocs.new_user response:{e}".format(e=x.get_status())
            )

    def new_group(self, group_name):
        """To create a group.

        Creates a group in the cloud with the name of group_name.

        Args:
            group_name (str): Group ID (group name).

        Raises:
            OperationFailure: The operation failed.
        """
        resp = self.post_data(self.URL_GROUPS, {"groupid": group_name})
        x = OcsXmlResponse(resp)
        if x.statuscode != "100":
            Ocs.logger.exception(
                "An exception was caught in Ocs.new_group due to "
                + "negative server response code: {q}".format(q=x.get_status())
            )
            raise OperationFailure(
                "Ocs.new_group response:{e}".format(e=x.get_status())
            )

    def get_group_members(self, group_id):
        """Group members.

        Returns members of the requested group.

        Args:
            group_id (str): Group ID (group name).

        Returns:
            (:obj: list of GroupMembers): List of group member objects.

        Raises:
            OperationFailure: The operation failed.
        """
        resp = self.get_data(self.URL_GROUPS + "/{grp}".format(grp=group_id))
        x = OcsXmlResponse(resp, "GroupMembers")
        if x.statuscode != "100":
            Ocs.logger.exception(
                "An exception was caught in Ocs.get_group_members due to "
                + "negative server response code: {q}".format(q=x.get_status())
            )
            raise OperationFailure(
                "Ocs.get_group_members response:{e}".format(e=x.get_status())
            )
        return x.data

    ##    def search_group(self, group):
    ##        pass

    def search_user(self, search=None, limit=None, offset=None):
        """Search users.

        Returns a list of usernames found by users.

        Args:
            search (str): Search string (by users full name).
            limit (int): Restriction on the number of returned records.
            offset (int): List offset from the beginning at the specified limit.

        Returns:
            (:obj: list of str): List of found users.

        Raises:
            OperationFailure: The operation failed.
        """
        srch = self.URL_USERS
        parameters = {"search": search, "limit": limit, "offset": offset}
        parameters = {k: v for (k, v) in parameters.items() if v is not None}
        resp = self.get_data(srch + "?" + urllib.parse.urlencode(parameters))
        x = OcsXmlResponse(resp, "GroupMembers")
        if x.statuscode != "100":
            Ocs.logger.exception(
                "An exception was caught in Ocs.search_user due to "
                + "negative server response code: {q}".format(q=x.get_status())
            )
            raise OperationFailure(
                "Ocs.search_user response:{e}".format(e=x.get_status())
            )
        return x.data

    def get_user(self, user_id):
        """Output information about the user.

        Returns detailed information about the user.

        Args:
            user_id (str): User ID (login).

        Returns:
            (:obj: User): User instance.

        Raises:
            OperationFailure: The operation failed.
        """
        resp = self.get_data(self.URL_USERS + "/{usr}".format(usr=user_id))
        x = OcsXmlResponse(resp, "User")
        if x.statuscode != "100":
            Ocs.logger.exception(
                "An exception was caught in Ocs.get_user due to "
                + "negative server response code: {q}".format(q=x.get_status())
            )
            raise OperationFailure(
                "Ocs.get_user response:{e}".format(e=x.get_status())
            )
        return x.data

    def set_user_parameter(self, user_id, param_name, param_value):
        """Set/change information about the user.

        Edits attributes related to a user. Users are able to edit email,
        displayname and password; admins can also edit the quota value.

        Args:
            user_id (str): User ID (login).
            param_name (str): users parameter name (supported parameters:
                'email','quota','displayname','phone','address','website',
                'twitter','password')
            param_value (str): quota

        Raises:
            OperationFailure: The operation failed.
            WrongParam: No any parameters to change
        """
        parameters = [
            "email",
            "quota",
            "displayname",
            "phone",
            "address",
            "website",
            "twitter",
            "password",
        ]
        if param_name in parameters:
            resp = self.put_data(
                self.URL_USERS + "/{usr}".format(usr=user_id),
                data_js={"key": param_name, "value": param_value},
            )
            x = OcsXmlResponse(resp)
            if x.statuscode != "100":
                Ocs.logger.exception(
                    "An exception was caught in Ocs.set_user due to "
                    + "negative server response code: {q}".format(
                        q=x.get_status()
                    )
                )
                raise OperationFailure(
                    "Ocs.set_user_parameter response:{e}".format(
                        e=x.get_status()
                    )
                )
        else:
            raise WrongParam(
                "Ocs.set_user_parameter wrong parameter name :{e}".format(
                    e=param_name
                )
            )

    def set_user(
            self,
            user_id,
            email=None,
            quota=None,
            displayname=None,
            phone=None,
            address=None,
            website=None,
            twitter=None,
            password=None,
            **kvargs
    ):
        """Set/change information about the user.

        Edits attributes related to a user. Users are able to edit email,
        displayname and password; admins can also edit the quota value.

        Args:
            user_id (str): User ID (login).
            email (str): email
            quota (str): quota
            displayname (str): display name
            address (str): address
            website (str): web site
            twitter (str): twitter
            password (str): new password

        Raises:
            OperationFailure: The operation failed.
            NotEnoughParams: No any parameters to change

        Note:
            kvargs used for arguments splatting from argparse
        """
        # server can change only one parameter by one request :(.
        if email:
            try:
                self.set_user_parameter(user_id, "email", email)
            except OperationFailure as e:
                Ocs.logger.error(
                    "Can't set parameter 'email': {e}".format(e=e.value)
                )

        if quota:
            try:
                self.set_user_parameter(user_id, "quota", quota)
            except OperationFailure as e:
                Ocs.logger.error(
                    "Can't set parameter 'quota': {e}".format(e=e.value)
                )

        if displayname:
            try:
                self.set_user_parameter(user_id, "displayname", displayname)
            except OperationFailure as e:
                Ocs.logger.error(
                    "Can't set parameter 'displayname': {e}".format(e=e.value)
                )

        if phone:
            try:
                self.set_user_parameter(user_id, "phone", phone)
            except OperationFailure as e:
                Ocs.logger.error(
                    "Can't set parameter 'phone': {e}".format(e=e.value)
                )

        if address:
            try:
                self.set_user_parameter(user_id, "address", address)
            except OperationFailure as e:
                Ocs.logger.error(
                    "Can't set parameter 'address': {e}".format(e=e.value)
                )

        if website:
            try:
                self.set_user_parameter(user_id, "website", website)
            except OperationFailure as e:
                Ocs.logger.error(
                    "Can't set parameter 'website': {e}".format(e=e.value)
                )

        if twitter:
            try:
                self.set_user_parameter(user_id, "twitter", twitter)
            except OperationFailure as e:
                Ocs.logger.error(
                    "Can't set parameter 'twitter': {e}".format(e=e.value)
                )

        if password:
            try:
                self.set_user_parameter(user_id, "password", password)
            except OperationFailure as e:
                Ocs.logger.error(
                    "Can't set parameter 'password': {e}".format(e=e.value)
                )

    def get_group_subadmins(self, group_id):
        """Subadmins.

        Get subadmins of a group.

        Args:
            group_id (str): Group ID (group name).

        Returns:
            (list of User id): List of subadmins.

        Raises:
            OperationFailure: The operation failed.
        """
        resp = self.get_data(
            self.URL_GROUPS + "/{groupid}/subadmins".format(groupid=group_id)
        )
        x = OcsXmlResponse(resp, "Subadmins")
        if x.statuscode != "100":
            Ocs.logger.exception(
                "An exception was caught in Ocs.get_group_subadmins"
                + " due to negative server response code: {q}".format(
                    q=x.get_status()
                )
            )
            raise OperationFailure(
                "Ocs.get_group_subadmins response:{e}".format(e=x.get_status())
            )
        return x.data

    def set_group_subadmins(self, group_id, user_id):
        """Set user as subadmin of the group.

        Sets the specified user as subadmin of the group.

        Args:
            group_id (str): Group ID (group name).
            user_id (str): User ID (login).

        Raises:
            OperationFailure: The operation failed.
        """
        resp = self.post_data(
            self.URL_USERS + "/{user_id}/subadmins".format(user_id=user_id),
            {"groupid": group_id},
        )
        x = OcsXmlResponse(resp)
        if x.statuscode != "100":
            Ocs.logger.exception(
                "An exception was caught in Ocs.set_group_subadmins due to "
                + "negative server response code: {q}".format(q=x.get_status())
            )
            raise OperationFailure(
                "Ocs.set_group_subadmins response:{e}".format(e=x.get_status())
            )

    def del_group_subadmins(self, group_id, user_id):
        """Revoke user as subadmin of the group.

        Revoke user as subadmin of the group.

        Args:
            group_id (str): Group ID (group name).
            user_id (str): User ID (login).

        Raises:
            OperationFailure: The operation failed.
        """
        resp = self.delete_data(
            self.URL_USERS + "/{user_id}/subadmins".format(user_id=user_id),
            {"groupid": group_id},
        )
        x = OcsXmlResponse(resp)
        if x.statuscode != "100":
            Ocs.logger.exception(
                "An exception was caught in Ocs.del_group_subadmins due to "
                + "negative server response code: {q}".format(q=x.get_status())
            )
            raise OperationFailure(
                "Ocs.del_group_subadmins response:{e}".format(e=x.get_status())
            )

    def remove_group(self, group_id):
        """Delete group.

        Removes a group from the cloud with the name from group_name.
        Group members are not affected.

        Args:
            group_name (str): Group ID (group name).

        Raises:
            OperationFailure: The operation failed.
        """
        resp = self.delete_data(
            self.URL_GROUPS + "/{group_id}".format(group_id=group_id), {}
        )
        x = OcsXmlResponse(resp)
        if x.statuscode != "100":
            Ocs.logger.exception(
                "An exception was caught in Ocs.remove_group due to "
                + "negative server response code: {q}".format(q=x.get_status())
            )
            raise OperationFailure(
                "Ocs.remove_group response:{e}".format(e=x.get_status())
            )

    def remove_user(self, userid):
        """Delete user.

        Removes a user from the cloud with the name from userid.

        Args:
            userid (str): User ID (user name).

        Raises:
            OperationFailure: The operation failed.
        """
        resp = self.delete_data(
            self.URL_USERS + "/{user_id}".format(user_id=userid), {}
        )
        x = OcsXmlResponse(resp)
        if x.statuscode != "100":
            Ocs.logger.exception(
                "An exception was caught in Ocs.remove_user due to "
                + "negative server response code: {q}".format(q=x.get_status())
            )
            raise OperationFailure(
                "Ocs.remove_user response:{e}".format(e=x.get_status())
            )

    def disable_user(self, userid):
        """Disable user.

        Disables the user on the cloud with the name from userid.

        Args:
            userid (str): User ID (user name).

        Raises:
            OperationFailure: The operation failed.
        """
        resp = self.put_data(
            self.URL_USERS + "/{user_id}/disable".format(user_id=userid), {}
        )
        cloud_answer = OcsXmlResponse(resp)
        fail_reason = ''
        if cloud_answer.statuscode == "100":
            return  # successful
        elif cloud_answer.statuscode == "101":
            fail_reason = 'failure'
        else:
            fail_reason = 'unknown error'
        Ocs.logger.error(
            "An exception was caught in Ocs.disable_user due to "
            + "negative server response code: {code} - {reason}".format(
                code=cloud_answer.statuscode,
                reason=fail_reason
            )
        )
        raise OperationFailure(
            "Ocs.disable_user error: {code} - {reason}".format(code=cloud_answer.statuscode, reason=fail_reason)
        )

    def enable_user(self, userid):
        """Enable user.

        Enables the user on the cloud with the name from userid.

        Args:
            userid (str): User ID (user name).

        Raises:
            OperationFailure: The operation failed.
        """
        resp = self.put_data(
            self.URL_USERS + "/{user_id}/enable".format(user_id=userid), {}
        )
        cloud_answer = OcsXmlResponse(resp)
        fail_reason = ''
        if cloud_answer.statuscode == "100":
            return  # successful
        elif cloud_answer.statuscode == "101":
            fail_reason = 'failure'
        else:
            fail_reason = 'unknown error'
        Ocs.logger.error(
            "An exception was caught in Ocs.enable_user due to "
            + "negative server response code: {code} - {reason}".format(
                code=cloud_answer.statuscode,
                reason=fail_reason
            )
        )
        raise OperationFailure(
            "Ocs.enable_user error: {code} - {reason}".format(code=cloud_answer.statuscode, reason=fail_reason)
        )

    def enable_app(self, appid):
        """Enable application.

        Enables the application on the cloud with the ID from appid.

        Args:
            appid (str): Application ID.

        Raises:
            OperationFailure: The operation failed.
        """
        resp = self.post_data(
            self.URL_APPS + "/{app_id}".format(app_id=appid), {}
        )
        x = OcsXmlResponse(resp)
        if x.statuscode != "100":
            Ocs.logger.exception(
                "An exception was caught in Ocs.enable_app due to "
                + "negative server response code: {q}".format(q=x.get_status())
            )
            raise OperationFailure(
                "Ocs.enable_app response:{e}".format(e=x.get_status())
            )

    def disable_app(self, appid):
        """Disable application.

        Disables the application on the cloud with the ID from appid.

        Args:
            appid (str): Application ID.

        Raises:
            OperationFailure: The operation failed.
        """
        resp = self.delete_data(
            self.URL_APPS + "/{app_id}".format(app_id=appid), {}
        )
        x = OcsXmlResponse(resp)
        if x.statuscode != "100":
            Ocs.logger.exception(
                "An exception was caught in Ocs.disable_app due to "
                + "negative server response code: {q}".format(q=x.get_status())
            )
            raise OperationFailure(
                "Ocs.disable_app response:{e}".format(e=x.get_status())
            )
