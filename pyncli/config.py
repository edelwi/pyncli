# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        Config
# Purpose:
#
# Author:      Evgeniy Semenov
#
# Created:     10.12.2018
# Copyright:   (c) Evgeniy Semenov 2018-2019
# Licence:     MIT
#-------------------------------------------------------------------------------

import os
from dotenv import load_dotenv

#basedir = os.path.abspath(os.path.dirname(__file__))
basedir = os.path.expanduser('~')
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):

    LOG_FILE = os.environ.get('LOG_FILE') or 'pyncli.log'
    LOG_MAX_BYTES = int(os.environ.get('LOG_MAX_BYTES')) if \
         (type(os.environ.get('LOG_MAX_BYTES'))==str and \
        len(os.environ.get('LOG_MAX_BYTES'))>0) else 24*1024*1024
    LOG_BACKUP_COUNT = int(os.environ.get('LOG_BACKUP_COUNT')) if \
         (type(os.environ.get('LOG_BACKUP_COUNT'))==str and \
        len(os.environ.get('LOG_BACKUP_COUNT'))>0) else 12

    CLOUD_USER = os.environ.get('CLOUD_USER') or 'NextCloud'
    CLOUD_USER_PWD = os.environ.get('CLOUD_USER_PWD') or None
    CLOUD_BASE_URL= os.environ.get('CLOUD_BASE_URL') or 'https://nc.example.com'

    USER_DEFAULT_QUOTA = int(os.environ.get('USER_DEFAULT_QUOTA')) if \
         (type(os.environ.get('USER_DEFAULT_QUOTA'))==str and \
        len(os.environ.get('USER_DEFAULT_QUOTA'))>0) else 5*1024*1024*1024

    GF_NAME_PREFIX = os.environ.get('GF_NAME_PREFIX') or '{'
    GF_NAME_SUFFIX = os.environ.get('GF_NAME_SUFFIX') or '}'
    GF_PERMISSION_DEFAULT_STR = os.environ.get('GF_PERMISSION_DEFAULT_STR') or 'r'

    LDAP_USER = os.environ.get('LDAP_USER') or 'nobody'
    LDAP_USER_PWD = os.environ.get('LDAP_USER_PWD') or 'secret'

    LDAP_HOST =  os.environ.get('LDAP_HOST') or None
    LDAP_BASE_DN = os.environ.get('LDAP_BASE_DN') or 'dc=example,dc=com'
##    LDAP_PORT = int(os.environ.get('LDAP_PORT')) if \
##        (type(os.environ.get('LDAP_PORT'))==str and \
##        len(os.environ.get('LDAP_PORT'))>0) else 389
##
##
##    LDAP_USER_RDN_ATTR = os.environ.get('LDAP_USER_RDN_ATTR') or 'cn'
##    LDAP_USER_LOGIN_ATTR = os.environ.get('LDAP_USER_LOGIN_ATTR') or \
##        'samaccountname'
##    LDAP_USE_SSL = os.environ.get('LDAP_USE_SSL') or False
    LDAP_ADD_SERVER = os.environ.get('LDAP_ADD_SERVER') or False
    LDAP_SEARCH_FOR_GROUPS = os.environ.get('LDAP_SEARCH_FOR_GROUPS') or \
        'dc=example,dc=com'
##    LDAP_GROUP_MEMBERS_ATTR = os.environ.get('LDAP_GROUP_MEMBERS_ATTR') or \
##        'member:1.2.840.113556.1.4.1941:'
##    LDAP_USER_SEARCH_SCOPE = os.environ.get('LDAP_USER_SEARCH_SCOPE') or \
##        'SUBTREE'
    LDAP_NEW_GROUP_DESCRIPTION = os.environ.get('LDAP_NEW_GROUP_DESCRIPTION') or \
        'Access group to cloud group'

    LDAP_GRP_NAME_PREFIX = os.environ.get('LDAP_GRP_NAME_PREFIX') or 'Cloud_'   #
    LDAP_GRP_NAME_SUFFIX = os.environ.get('LDAP_GRP_NAME_SUFFIX') or ''         #
    LDAP_PARENT_GRP_NAME = os.environ.get('LDAP_PARENT_GRP_NAME') or None       #

    LOG_TO_STDOUT =  os.environ.get('LOG_TO_STDOUT') or True

