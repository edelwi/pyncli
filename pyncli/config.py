# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        Config
# Purpose:     application settings
#
# Author:      Evgeniy Semenov
#
# Created:     10.12.2018
# Copyright:   (c) Evgeniy Semenov 2018-2019
# Licence:     MIT
# -------------------------------------------------------------------------------

import os
from dotenv import load_dotenv

# basedir = os.path.abspath(os.path.dirname(__file__))
basedir = os.path.expanduser("~")
load_dotenv(os.path.join(basedir, ".env"))


class Config(object):
    """Class with application settings.

        Settings are loaded from environment variables or from the .env file
        located in the root of the user's home directory or are initiated
        by default values.
    """

    CLOUD_USER = os.environ.get("CLOUD_USER") or "admin"
    """The user of the cloud from which requests will be made."""

    CLOUD_USER_PWD = os.environ.get("CLOUD_USER_PWD") or "admin"
    """Cloud users password."""

    CLOUD_BASE_URL = (
        os.environ.get("CLOUD_BASE_URL") or "https://nc.example.com"
    )
    """Your NextCloud server URL. Or you can try a demo server, first create it
        at https://demo.nextcloud.com."""

    LOG_TO_STDOUT = os.environ.get("LOG_TO_STDOUT") or True
    """Print log on console."""

    LOG_FILE = os.environ.get("LOG_FILE") or "pyncli.log"
    """Log file name."""

    LOG_MAX_BYTES = (
        int(os.environ.get("LOG_MAX_BYTES"))
        if (
            type(os.environ.get("LOG_MAX_BYTES")) == str
            and len(os.environ.get("LOG_MAX_BYTES")) > 0
        )
        else 24 * 1024 * 1024
    )
    """The maximum size of the log file."""

    LOG_BACKUP_COUNT = (
        int(os.environ.get("LOG_BACKUP_COUNT"))
        if (
            type(os.environ.get("LOG_BACKUP_COUNT")) == str
            and len(os.environ.get("LOG_BACKUP_COUNT")) > 0
        )
        else 12
    )
    """Backups log files count."""

    LDAP_USER = os.environ.get("LDAP_USER") or "nobody"
    """User in your LDAP who can create groups in LDAP_SEARCH_FOR_GROUPS
        location. If you are not using an LDAP server, leave this variable
        empty and ignore all other variables whose names begin with LDAP_."""

    LDAP_USER_PWD = os.environ.get("LDAP_USER_PWD") or "secret"
    """LDAP users password."""

    LDAP_HOST = os.environ.get("LDAP_HOST") or None
    """Primary LDAP server. Used ldaps bind on port 636 by default."""

    LDAP_ADD_SERVER = os.environ.get("LDAP_ADD_SERVER") or False
    """Additional server, if specified, uses round-robin binding."""

    LDAP_BASE_DN = os.environ.get("LDAP_BASE_DN") or "dc=example,dc=com"
    """Base distinctive names, which is used when searching for users."""

    LDAP_SEARCH_FOR_GROUPS = (
        os.environ.get("LDAP_SEARCH_FOR_GROUPS") or "dc=example,dc=com"
    )
    """Distinguished name of the group organizational unit used to work with
        ldap groups."""

    LDAP_NEW_GROUP_DESCRIPTION = (
        os.environ.get("LDAP_NEW_GROUP_DESCRIPTION")
        or "Access group to cloud group"
    )
    """Description for created groups."""

    LDAP_GRP_NAME_PREFIX = os.environ.get("LDAP_GRP_NAME_PREFIX") or "Cloud_"
    """The prefix for the name of the ldap group to the corresponding cloud
        group."""

    LDAP_GRP_NAME_SUFFIX = os.environ.get("LDAP_GRP_NAME_SUFFIX") or ""
    """The suffix for the name of the ldap group to the corresponding cloud
        group."""

    LDAP_PARENT_GRP_NAME = os.environ.get("LDAP_PARENT_GRP_NAME") or None
    """Parent group in which all newly created LDAP groups will be placed."""

    USER_DEFAULT_QUOTA = (
        int(os.environ.get("USER_DEFAULT_QUOTA"))
        if (
            type(os.environ.get("USER_DEFAULT_QUOTA")) == str
            and len(os.environ.get("USER_DEFAULT_QUOTA")) > 0
        )
        else 5 * 1024 * 1024 * 1024
    )
    """The quota value that will be applied by default unless explicitly
        specified. Default 5Gb. Set -3 to unlimited."""

    GF_NAME_PREFIX = os.environ.get("GF_NAME_PREFIX") or "{"
    """The prefix for the group folder name. So you can help the user to
        distinguish personal folders from group folders. I use surrounding
        curly braces."""

    GF_NAME_SUFFIX = os.environ.get("GF_NAME_SUFFIX") or "}"
    """The suffix for the group folder name. So you can help the user to
        distinguish personal folders from group folders."""

    GF_PERMISSION_DEFAULT_STR = (
        os.environ.get("GF_PERMISSION_DEFAULT_STR") or "r"
    )
    """The permissions value that will be applied by default unless explicitly
        specified."""
