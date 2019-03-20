# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
# Name:        nc
# Purpose:     Python NextCloud Command Line Interface
#
# Author:      Evgeniy Semenov
#
# Created:     27.12.2018
# Copyright:   (c) Evgeniy Semenov 2018-2019
# Licence:     MIT
#-------------------------------------------------------------------------------
import argparse
import os
import textwrap

from pyncli import name as prog_name
from pyncli import __version__ as prog_ver
from pyncli.config import Config
from pyncli.ocs import ocs
from pyncli.ocs.ocs import (PERMISSION_CREATE, PERMISSION_READ,
    PERMISSION_UPDATE, PERMISSION_DELETE, PERMISSION_SHARE, PERMISSION_ALL)
from pyncli.ocs import exceptions
from pyncli.ldap import operate2
from pyncli.ldap import group
import logging
from logging.handlers import RotatingFileHandler
from pyncli.ldap.admexept import AdminException, OperationFailure, WrongParam
import re

PERMISSION_DEFAULT_STR = Config.GF_PERMISSION_DEFAULT_STR #'r'
PATTERN_LOGIN_1 = re.compile(r'^[a-zA-Z]+\w*$',re.IGNORECASE)
PATTERN_LOGIN_2 = re.compile(
    r'^[a-zA-Z]+[a-zA-Z0-9-\.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',re.IGNORECASE)
PATTERN_QUOTA_1 = re.compile(
    r'(?P<value>\d+\.?\d*)(?P<multiplier>[kmgt]?)',re.IGNORECASE)
DEFAULT_QUOTA = Config.USER_DEFAULT_QUOTA
PREF = Config.GF_NAME_PREFIX
SUF = Config.GF_NAME_SUFFIX
LPR = Config.LDAP_GRP_NAME_PREFIX
LSU = Config.LDAP_GRP_NAME_SUFFIX
LPARENT = Config.LDAP_PARENT_GRP_NAME

def str_to_permissions(str_code):
    """Convert character permissions representation to digital.

        Convert character permissions representation to digital. If conversion
        fails it returns default quota.

        Args:
            str_code (unicode): Сharacter permissions representation (rcudsa).
                r - read
                c - create
                u - update
                d - delete
                s - share
                a - all of the above

        Returns:
            int: permissions.
    """
    #'r','c','u','d','s','a'
    if not isinstance(str_code, str) or str_code=='':
        return str_to_permissions(PERMISSION_DEFAULT_STR)
    else:
        permissions=0
        for it in str_code.lower():
            if it=='r':
                permissions+=PERMISSION_READ
            elif it=='c':
                permissions+=PERMISSION_CREATE
            elif it=='u':
                permissions+=PERMISSION_UPDATE
            elif it=='d':
                permissions+=PERMISSION_DELETE
            elif it=='s':
                permissions+=PERMISSION_SHARE
            elif it=='a':
                permissions+=PERMISSION_ALL
        if permissions>PERMISSION_ALL:
            permissions=PERMISSION_ALL
    return permissions

def check(pattern,check_str):
    match = re.search(pattern,check_str)
    if match:
        return match

def is_ascii(text):
    if isinstance(text,str):
        return all(ord(x) < 128 for x in text)

def get_quote_bytes(quote_str):
    match=re.search(PATTERN_QUOTA_1,quote_str)
    if match:
        val=float(match.groupdict()['value'])
        mul=match.groupdict()['multiplier'].lower() if \
            'multiplier' in match.groupdict() else ''
        m=0
        if mul=='g':
            m=1073741824
        elif mul=='m':
            m=1048576
        elif mul=='':
           m=1
        elif mul=='k':
            m=1024
        elif mul=='t':
            m=1099511627776
        return round(val*m)
    else:
        return DEFAULT_QUOTA


def is_fullname(name):
    if len(name.split(' '))>=2:
        return True
    else:
        return False

def is_login(name):
    for ptr in (PATTERN_LOGIN_1,PATTERN_LOGIN_2):
        login=check(ptr,name)
        if login:
            return True
    else: #for-else
        return False

def new_groupfolder(args):
    """Create new GroupFolder
    """
    if ch and not args.debug:
        ch.setLevel(logging.INFO)
    else:
        ch.setLevel(logging.DEBUG)

    user_list=[]
    for line in args.usersfile:
        ln=line.strip()
        print(ln)
        if is_fullname(ln):
            user_list.append({'fullname':ln})
        elif is_login(ln):
            user_list.append({'login':ln})
        else:
            continue
    user_obj_list=[]

    share_name=args.name.lstrip(PREF).rstrip(SUF)
    permissions= sum( str_to_permissions(x) for x in args.permissions )
    quota= get_quote_bytes(args.quota)

    try:
        cloud=ocs.Ocs(Config.CLOUD_USER, Config.CLOUD_USER_PWD,
            Config.CLOUD_BASE_URL)
    except (OperationFailure, WrongParam) as e:
        logger.error('Could not connect to the cloud: {e}'.format(e=e.value))
        exit(1)

    if 'groupfolders' not in cloud._apps:
        logger.warning('Your server does not support group folder functionality.')
        return
    ncgroup=ocs.Group(share_name,permissions)
    gf=ocs.GroupFolder(id=0,mount_point='{pref}{gr}{suf}'.format(
            pref=PREF,
            suf=SUF,
            gr=share_name),
            groups=[ncgroup],quota=quota)
    cloud.batch_new_group_folder(gf)

    if 'user_ldap' in cloud._apps and  Config.LDAP_USER:
        try:
            adm=operate2.admin(Config.LDAP_USER, Config.LDAP_USER_PWD,
                [Config.LDAP_HOST, Config.LDAP_ADD_SERVER])
            ldap_ok=True
        except OperationFailure as e:
            logger.exeption('Could not connect to the ldap backend: {e}. Directory operations will be skipped.'.format(e=e.value))
            ldap_ok=False
    else:
        ldap_ok=False

    if ldap_ok:
        for usr in user_list:
            if 'fullname' in usr:
                u=adm.search_users_p("(&(objectClass=user)(displayname={fullname})(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))".format(
                    fullname=usr['fullname']),
                    base=Config.LDAP_BASE_DN, user_class_name='user')
                if len(u)==1:
                    user_obj_list.append(u[0])
                elif len(u)==0:
                    logger.warning('User "{u}" not found. Skip it.'.format(
                        u=usr['fullname']))
                else:
                    logger.warning('Searching for user "{u}" returned an ambiguous result: {r}. Set the user by login.'.format(
                        u=usr['fullname'], r=', '.join(x.brief for x in u) ))
            elif 'login' in usr:
                if '@' in usr['login']:
                    u=adm.search_users_p("(&(objectClass=user)(userPrincipalName={login})(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))".format(
                        login=usr['login']),
                        base=Config.LDAP_BASE_DN, user_class_name='user')
                else:
                    u=adm.search_users_p("(&(objectClass=user)(sAMAccountName={login})(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))".format(
                        login=usr['login']),
                        base=Config.LDAP_BASE_DN, user_class_name='user')
                if len(u)==1:
                    user_obj_list.append(u[0])
                elif len(u)==0:
                    logger.warning('User "{u}" not found. Skip it.'.format(
                        u=usr['login']))
                else:
                    logger.warning('Searching for user "{u}" returned an ambiguous result: {r}. This should not be!'.format(
                        u=usr['login'], r=', '.join(x.brief for x in u) ))

    if ldap_ok:
        for usr in user_obj_list:
            cloud.add_user_to_group(usr.principal_name ,ncgroup.group_id)
    else:
        for usr in user_list:
            if 'fullname' in usr:
                logger.warning('The directory is not available. I can not add a user by their full name. Skipping user {u}.'.format(
                        u=usr['fullname'] ))
            elif 'login' in usr:
                # TODO: may by check is the login with suffix
                cloud.add_user_to_group(usr['login'] ,ncgroup.group_id)
    if ldap_ok:
        ldap_grp=group.group(
            '{lpr}{gr}{lsu}'.format(
                lpr=LPR,
                lsu=LSU,
                gr=share_name),
            org_unit=Config.LDAP_SEARCH_FOR_GROUPS,
            description="{descr} {gr}".format(
                descr=Config.LDAP_NEW_GROUP_DESCRIPTION,
                gr=share_name))
        adm.create_group(ldap_grp)

        share_grp=adm.get_group('{lpr}{gr}{lsu}'.format(
            lpr=LPR,
            lsu=LSU,
            gr=share_name),'group')
        if LPARENT:
            # Добавим группу шары в группу всех шар
            all_shares_ldap_grp=adm.get_group(LPARENT,'group')
            adm.add_users_to_groups([share_grp],[all_shares_ldap_grp])

        adm.add_users_to_groups(user_obj_list,[share_grp])

def new_group(args):
    """Create new Group
    """
    if ch and not args.debug:
        ch.setLevel(logging.INFO)
    else:
        ch.setLevel(logging.DEBUG)

    user_list=[]
    for line in args.usersfile:
        ln=line.strip()
        print(ln)
        if is_fullname(ln):
            user_list.append({'fullname':ln})
        elif is_login(ln):
            user_list.append({'login':ln})
        else:
            continue
    user_obj_list=[]

    group_name=args.name

    try:
        cloud=ocs.Ocs(Config.CLOUD_USER, Config.CLOUD_USER_PWD,
            Config.CLOUD_BASE_URL)
    except (OperationFailure, WrongParam) as e:
        logger.error('Could not connect to the cloud: {e}'.format(e=e.value))
        exit(1)
    cloud.new_group(group_name)
    ncgroup=ocs.Group(group_name)
    if 'user_ldap' in cloud._apps and  Config.LDAP_USER:
        try:
            adm=operate2.admin(Config.LDAP_USER, Config.LDAP_USER_PWD,
                [Config.LDAP_HOST, Config.LDAP_ADD_SERVER])
            ldap_ok=True
        except OperationFailure as e:
            logger.exeption('Could not connect to the ldap backend: {e}. Directory operations will be skipped.'.format(e=e.value))
            ldap_ok=False
    else:
        ldap_ok=False

    if ldap_ok:
        for usr in user_list:
            if 'fullname' in usr:
                u=adm.search_users_p("(&(objectClass=user)(displayname={fullname})(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))".format(
                    fullname=usr['fullname']),
                    base=Config.LDAP_BASE_DN, user_class_name='user')
                if len(u)==1:
                    user_obj_list.append(u[0])
                elif len(u)==0:
                    logger.warning("User \"{u}\" not found. Skip it.".format(
                        u=usr['fullname']))
                else:
                    logger.warning('Searching for user \"{u}\" returned an ambiguous result: {r}. Set the user by login.'.format(
                        u=usr['fullname'], r=', '.join(x.brief for x in u) ))
            elif 'login' in usr:
                if '@' in usr['login']:
                    u=adm.search_users_p("(&(objectClass=user)(userPrincipalName={login})(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))".format(
                        login=usr['login']),
                        base=Config.LDAP_BASE_DN, user_class_name='user')
                else:
                    u=adm.search_users_p("(&(objectClass=user)(sAMAccountName={login})(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))".format(
                        login=usr['login']),
                        base=Config.LDAP_BASE_DN, user_class_name='user')
                if len(u)==1:
                    user_obj_list.append(u[0])
                elif len(u)==0:
                    logger.warning("User \"{u}\" not found. Skip it.".format(
                        u=usr['login']))
                else:
                    logger.warning('Searching for user \"{u}\" returned an ambiguous result: {r}. This should not be!'.format(
                        u=usr['fullname'], r=', '.join(x.brief for x in u) ))

    if ldap_ok:
        for usr in user_obj_list:
            cloud.add_user_to_group(usr.principal_name ,ncgroup.group_id)
    else:
        for usr in user_list:
            if 'fullname' in usr:
                logger.warning('The directory is not available. I can not add a user by their full name. Skipping user {u}.'.format(
                        u=usr['fullname'] ))
            elif 'login' in usr:
                # TODO: may by check is the login with suffix
                cloud.add_user_to_group(usr['login'] ,ncgroup.group_id)
    if ldap_ok:
        ldap_grp=group.group(
            '{lpr}{gr}{lsu}'.format(
                lpr=LPR,
                lsu=LSU,
                gr=group_name),
            org_unit=Config.LDAP_SEARCH_FOR_GROUPS,
            description="{descr} {gr}".format(
                descr=Config.LDAP_NEW_GROUP_DESCRIPTION,
                gr=group_name))
        adm.create_group(ldap_grp)

        if LPARENT:
            # Добавим группу шары в группу всех шар
            all_shares_ldap_grp=adm.get_group(LPARENT,'group')
            adm.add_users_to_groups([share_grp],[all_shares_ldap_grp])

        share_grp=adm.get_group('{lpr}{gr}{lsu}'.format(
            lpr=LPR,
            lsu=LSU,
            gr=group_name),'group')
        adm.add_users_to_groups(user_obj_list,[share_grp])

def new_user(args):
    """Create new user
    """
    if ch and not args.debug:
        ch.setLevel(logging.INFO)
    else:
        ch.setLevel(logging.DEBUG)
    if is_login(args.login):
        login = args.login
    else:
        logger.warning('It does not look like it is {l} login.'.format(l=args.login))
        return
    try:
        cloud=ocs.Ocs(Config.CLOUD_USER, Config.CLOUD_USER_PWD,
            Config.CLOUD_BASE_URL)
    except (OperationFailure, WrongParam) as e:
        logger.error('Could not connect to the cloud: {e}'.format(e=e.value))
        exit(1)
    try:
        cloud.new_user(userid=login, password=args.password, groups=args.group )
    except OperationFailure as e:
        logger.error('Can not create user {u}: {err}'.format(
            u=login,err=e.value))
        return
    params=vars(args)
    params.pop('password',None)
    cloud.set_user(user_id=login,**params)

def del_group_member(args):
    """Delete member from the group.
    """
    if ch and not args.debug:
        ch.setLevel(logging.INFO)
    else:
        ch.setLevel(logging.DEBUG)

    if args.fullname:
        fullname=args.fullname if is_fullname(args.fullname) else ''
    else:
        fullname=''
    if args.login:
        login=args.login if is_login(args.login) else ''
    else:
        login=''
    group_name=args.name
    user_obj_list=[]

    try:
        cloud=ocs.Ocs(Config.CLOUD_USER, Config.CLOUD_USER_PWD,
            Config.CLOUD_BASE_URL)
    except (OperationFailure, WrongParam) as e:
        logger.error('Could not connect to the cloud: {e}'.format(e=e.value))
        exit(1)

    if 'user_ldap' in cloud._apps and  Config.LDAP_USER:
        try:
            adm=operate2.admin(Config.LDAP_USER, Config.LDAP_USER_PWD,
                [Config.LDAP_HOST, Config.LDAP_ADD_SERVER])
            ldap_ok=True
        except OperationFailure as e:
            logger.exeption('Could not connect to the ldap backend: {e}. Directory operations will be skipped.'.format(e=e.value))
            ldap_ok=False
    else:
        ldap_ok=False

    if login and ldap_ok:
        if '@' in login:
            u=adm.search_users_p("(&(objectClass=user)(userPrincipalName={login})(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))".format(
                login=login),
                base=Config.LDAP_BASE_DN, user_class_name='user')
        else:
            u=adm.search_users_p("(&(objectClass=user)(sAMAccountName={login})(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))".format(
                login=login),
                base=Config.LDAP_BASE_DN, user_class_name='user')
        if len(u)==1:
            user_obj_list.append(u[0])
        elif len(u)==0:
            logger.warning("User \"{u}\" not found. Skip it.".format(
                u=login))
        else:
            logger.warning('Searching for user \"{u}\" returned an ambiguous result: {r}. This should not be!'.format(
                u=login, r=', '.join(x.brief for x in u) ))

        cloud_group=cloud.remove_user_from_group(
            user_id=user_obj_list[0].principal_name,group_id=group_name)
        ldap_grp=adm.get_group('{lpr}{gr}{lsu}'.format(
            lpr=LPR,
            lsu=LSU,
            gr=group_name),'group')
        adm.remove_users_from_groups(user_obj_list,[ldap_grp])
        return
    elif login and  not ldap_ok:
        cloud_group=cloud.remove_user_from_group(
            user_id=login,group_id=group_name)
        return
    elif not login and fullname and ldap_ok:
        u=adm.search_users_p("(&(objectClass=user)(displayname={fullname})(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))".format(
            fullname=fullname),
            base=Config.LDAP_BASE_DN, user_class_name='user')
        if len(u)==1:
            user_obj_list.append(u[0])
        elif len(u)==0:
            logger.warning("User \"{u}\" not found.".format(
                u=fullname))
            return
        else:
            logger.warning('Searching for user \"{u}\" returned an ambiguous result: {r}. Set the user by login.'.format(
                u=fullname, r=', '.join(x.brief for x in u) ))
            return
        cloud.remove_user_from_group(user_id=user_obj_list[0].principal_name,
            group_id=group_name)
        ldap_grp=adm.get_group('{lpr}{gr}{lsu}'.format(
            lpr=LPR,
            lsu=LSU,
            gr=group_name),'group')
        adm.remove_users_from_groups(user_obj_list,[ldap_grp])
        return
    elif not login and fullname and not ldap_ok:
        logger.warning('The directory is not available. I can not remove a user by their full name. Skipping user {u}.'.format(
            u=fullname))
        return
    else:
        logger.warning('User is not defined. Login: "{l}", Fullname: "{f}"'.format(
            l=login, f=fullname))
        return

def del_group(args):
    """Delete Group
    """
    if ch and not args.debug:
        ch.setLevel(logging.INFO)
    else:
        ch.setLevel(logging.DEBUG)

    group_name=args.name

    try:
        cloud=ocs.Ocs(Config.CLOUD_USER, Config.CLOUD_USER_PWD,
            Config.CLOUD_BASE_URL)
    except (OperationFailure, WrongParam) as e:
        logger.error('Could not connect to the cloud: {e}'.format(e=e.value))
        exit(1)

    if 'user_ldap' in cloud._apps and  Config.LDAP_USER:
        try:
            adm=operate2.admin(Config.LDAP_USER, Config.LDAP_USER_PWD,
                [Config.LDAP_HOST, Config.LDAP_ADD_SERVER])
            ldap_ok=True
        except OperationFailure as e:
            logger.exeption('Could not connect to the ldap backend: {e}. Directory operations will be skipped.'.format(e=e.value))
            ldap_ok=False
    else:
        ldap_ok=False

    cloud.remove_group(group_id=group_name)
    if ldap_ok:
        ldap_grp=group.group(
            '{lpr}{gr}{lsu}'.format(lpr=LPR,
                lsu=LSU,gr=group_name),
            org_unit=Config.LDAP_SEARCH_FOR_GROUPS,
            description="{descr} {gr}".format(
                descr=Config.LDAP_NEW_GROUP_DESCRIPTION,
                gr=group_name))
        try:
            adm.delete_group(ldap_grp)
        except (NotFound, OperationFailure) as e:
            logger.error('Could not delete ldapgroup {g}. Error: {e}'.format(
                g=ldap_grp.brief,
                e=e.value))

def del_group_link(args):
    """Unlink group from the groupfolder
    """
    if ch and not args.debug:
        ch.setLevel(logging.INFO)
    else:
        ch.setLevel(logging.DEBUG)

    group_name=args.name
    groupfolder_name=args.groupfolder.lstrip(PREF).rstrip(SUF)
    try:
        cloud=ocs.Ocs(Config.CLOUD_USER, Config.CLOUD_USER_PWD,
            Config.CLOUD_BASE_URL)
    except (OperationFailure, WrongParam) as e:
        logger.error('Could not connect to the cloud: {e}'.format(e=e.value))
        exit(1)
    if 'groupfolders' not in cloud._apps:
        logger.warning('Your server does not support group folder functionality.')
        return
    group_folders=cloud.get_group_folders()
    for gf in group_folders:
        if gf.mount_point==PREF+groupfolder_name+SUF:
            for grp in gf.groups:
                if grp.group_id==group_name:
                    cloud.revoke_access_to_group_folder(
                        gfolder_id=gf.id,
                        group_id=group_name)
                    return
    else:
        logger.warning('Group folder {gp} with group {grp} not found.'.format(
            gp=groupfolder_name, grp=group_name))


def del_groupfolder(args):
    """Delete Groupfolder
    """
    if ch and not args.debug:
        ch.setLevel(logging.INFO)
    else:
        ch.setLevel(logging.DEBUG)
    groupfolder_name=args.name.lstrip(PREF).rstrip(SUF)

    try:
        cloud=ocs.Ocs(Config.CLOUD_USER, Config.CLOUD_USER_PWD,
            Config.CLOUD_BASE_URL)
    except (OperationFailure, WrongParam) as e:
        logger.error('Could not connect to the cloud: {e}'.format(e=e.value))
        exit(1)

    if 'user_ldap' in cloud._apps and  Config.LDAP_USER:
        try:
            adm=operate2.admin(Config.LDAP_USER, Config.LDAP_USER_PWD,
                [Config.LDAP_HOST, Config.LDAP_ADD_SERVER])
            ldap_ok=True
        except OperationFailure as e:
            logger.exeption('Could not connect to the ldap backend: {e}. Directory operations will be skipped.'.format(e=e.value))
            ldap_ok=False
    else:
        ldap_ok=False

    if 'groupfolders' not in cloud._apps:
        logger.warning('Your server does not support group folder functionality.')
        return
    group_folders=cloud.get_group_folders()
    for gf in group_folders:
        if gf.mount_point==PREF+groupfolder_name+SUF:
            cloud.remove_group_folder(gfolder_id=gf.id)
            for grp in gf.groups:
                cloud.remove_group(group_id=grp.group_id)
                if ldap_ok:
                    ldap_grp='{lpr}{gr}{lsu}'.format(lpr=LPR,
                        lsu=LSU,gr=grp.group_id)
                    logger.debug('Trying to delete group: {gp}.'.format(
                        gp=ldap_grp))
                    try:
                        adm.delete_group(ldap_grp)
                    except (OperationFailure, NotFound) as e:
                        logger.exeption(
                            'Could not delete group: {g}. Error: {e}.'.format(
                            e=e.value,g=ldap_grp))
            return
    else:
        logger.warning('Group folder {gp} not found.'.format(
            gp=groupfolder_name))

def del_group_subadmins(args):
    """Demote user as group subadmin
    """
    if ch and not args.debug:
        ch.setLevel(logging.INFO)
    else:
        ch.setLevel(logging.DEBUG)
    group_name = args.name
    if is_login(args.login):
        login = args.login
    else:
        logger.warning('It does not look like it is {l} login.'.format(l=args.login))
        return
    try:
        cloud=ocs.Ocs(Config.CLOUD_USER, Config.CLOUD_USER_PWD,
            Config.CLOUD_BASE_URL)
    except (OperationFailure, WrongParam) as e:
        logger.error('Could not connect to the cloud: {e}'.format(e=e.value))
        exit(1)

    cloud.del_group_subadmins(group_name,login)

def del_user(args):
    """Delete user
    """
    if ch and not args.debug:
        ch.setLevel(logging.INFO)
    else:
        ch.setLevel(logging.DEBUG)

    if is_login(args.login):
        login = args.login
    else:
        logger.warning('It does not look like it is {l} login.'.format(l=args.login))
        return
    try:
        cloud=ocs.Ocs(Config.CLOUD_USER, Config.CLOUD_USER_PWD,
            Config.CLOUD_BASE_URL)
    except (OperationFailure, WrongParam) as e:
        logger.error('Could not connect to the cloud: {e}'.format(e=e.value))
        exit(1)

    cloud.remove_user(login)

def add_group(args):
    """Add Group to the group folder
    """
    if ch and not args.debug:
        ch.setLevel(logging.INFO)
    else:
        ch.setLevel(logging.DEBUG)

    group_name=args.name
    group_folder=args.groupfolder.lstrip(PREF).rstrip(SUF)
    permissions=sum( str_to_permissions(x) for x in args.permissions )

    try:
        cloud=ocs.Ocs(Config.CLOUD_USER, Config.CLOUD_USER_PWD,
            Config.CLOUD_BASE_URL)
    except (OperationFailure, WrongParam) as e:
        logger.error('Could not connect to the cloud: {e}'.format(e=e.value))
        exit(1)

    if 'groupfolders' not in cloud._apps:
        logger.warning('Your server does not support group folder functionality.')
        return
    group_folders=cloud.get_group_folders()
    gf=None
    for itm in group_folders:
        if itm.mount_point==PREF+group_folder+SUF:
            gf=itm
    if not gf:
        logger.error('The specified group folder {gp} is not found!'.format(
            gp=group_folder))
        exit(0)
    cloud.grant_access_to_group_folder(gfolder_id=gf.id,
        group_id=group_name)
    cloud.set_group_folder_group_permissions(gfolder_id=gf.id,
        group_id=group_name,permissions=permissions)

def add_user(args):
    """Add User to the Group
    """
    if ch and not args.debug:
        ch.setLevel(logging.INFO)
    else:
        ch.setLevel(logging.DEBUG)

    if args.name:
        fullname=args.name if is_fullname(args.name) else ''
    else:
        fullname=''
    if args.login:
        login=args.login if is_login(args.login) else ''
    else:
        login=''
    group_name=args.group
    user_obj_list=[]

    try:
        cloud=ocs.Ocs(Config.CLOUD_USER, Config.CLOUD_USER_PWD,
            Config.CLOUD_BASE_URL)
    except (OperationFailure, WrongParam) as e:
        logger.error('Could not connect to the cloud: {e}'.format(e=e.value))
        exit(1)

    if 'user_ldap' in cloud._apps and  Config.LDAP_USER:
        try:
            adm=operate2.admin(Config.LDAP_USER, Config.LDAP_USER_PWD,
                [Config.LDAP_HOST, Config.LDAP_ADD_SERVER])
            ldap_ok=True
        except OperationFailure as e:
            logger.exeption('Could not connect to the ldap backend: {e}. Directory operations will be skipped.'.format(e=e.value))
            ldap_ok=False
    else:
        ldap_ok=False

    if login and ldap_ok:
        if '@' in login:
            u=adm.search_users_p("(&(objectClass=user)(userPrincipalName={login})(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))".format(
                login=login),
                base=Config.LDAP_BASE_DN, user_class_name='user')
        else:
            u=adm.search_users_p("(&(objectClass=user)(sAMAccountName={login})(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))".format(
                login=login),
                base=Config.LDAP_BASE_DN, user_class_name='user')
        if len(u)==1:
            user_obj_list.append(u[0])
        elif len(u)==0:
            logger.warning("User \"{u}\" not found. Skip it.".format(
                u=login))
        else:
            logger.warning('Searching for user \"{u}\" returned an ambiguous result: {r}. This should not be!'.format(
                u=login, r=', '.join(x.brief for x in u) ))

        cloud_group=cloud.add_user_to_group(
            user_id=user_obj_list[0].principal_name,group_id=group_name)
        ldap_grp=adm.get_group('{lpr}{gr}{lsu}'.format(lpr=LPR,
            lsu=LSU,gr=group_name),'group')
        adm.add_users_to_groups(user_obj_list,[ldap_grp])
        return
    elif login and not ldap_ok:
        cloud_group=cloud.add_user_to_group(
            user_id=login,group_id=group_name)
        return
    elif not login and fullname and ldap_ok:
        u=adm.search_users_p("(&(objectClass=user)(displayname={fullname})(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))".format(
            fullname=fullname),
            base=Config.LDAP_BASE_DN, user_class_name='user')
        if len(u)==1:
            user_obj_list.append(u[0])
        elif len(u)==0:
            logger.warning("User \"{u}\" not found.".format(
                u=fullname))
            return
        else:
            logger.warning('Searching for user \"{u}\" returned an ambiguous result: {r}. Set the user by login.'.format(
                u=fullname, r=', '.join(x.brief for x in u) ))
            return
        cloud.add_user_to_group(user_id=user_obj_list[0].principal_name,
            group_id=group_name)
        ldap_grp=adm.get_group('{lpr}{gr}{lsu}'.format(lpr=LPR,
            lsu=LSU,gr=group_name),'group')
        adm.add_users_to_groups(user_obj_list,[ldap_grp])
        return
    elif not login and fullname and not ldap_ok:
        logger.warning('The directory is not available. I can not add a user by their full name. Skipping user {u}.'.format(
            u=fullname))
        return
    else:
        logger.warning('User is not defined. Login: {l}, Fullname: {f}'.format(
            l=login, f=fullname))
        return

def add_users(args):
    """Add Users to the Group
    """
    if ch and not args.debug:
        ch.setLevel(logging.INFO)
    else:
        ch.setLevel(logging.DEBUG)

    user_list=[]
    for line in args.usersfile:
        ln=line.strip()
        print(ln)
        if is_fullname(ln):
            user_list.append({'fullname':ln})
        elif is_login(ln):
            user_list.append({'login':ln})
        else:
            continue
    user_obj_list=[]
    group_name=args.group
    ncgroup=ocs.Group(group_name)

    try:
        cloud=ocs.Ocs(Config.CLOUD_USER, Config.CLOUD_USER_PWD,
            Config.CLOUD_BASE_URL)
    except (OperationFailure, WrongParam) as e:
        logger.error('Could not connect to the cloud: {e}'.format(e=e.value))
        exit(1)

    if 'user_ldap' in cloud._apps and  Config.LDAP_USER:
        try:
            adm=operate2.admin(Config.LDAP_USER, Config.LDAP_USER_PWD,
                [Config.LDAP_HOST, Config.LDAP_ADD_SERVER])
            ldap_ok=True
        except OperationFailure as e:
            logger.exeption('Could not connect to the ldap backend: {e}. Directory operations will be skipped.'.format(e=e.value))
            ldap_ok=False
    else:
        ldap_ok=False

    for usr in user_list:
        if 'fullname' in usr and ldap_ok:
            u=adm.search_users_p("(&(objectClass=user)(displayname={fullname})(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))".format(
                fullname=usr['fullname']),
                base=Config.LDAP_BASE_DN, user_class_name='user')
            if len(u)==1:
                user_obj_list.append(u[0])
            elif len(u)==0:
                logger.warning("User \"{u}\" not found. Skip it.".format(
                    u=usr['fullname']))
            else:
                logger.warning('Searching for user \"{u}\" returned an ambiguous result: {r}. Set the user by login.'.format(
                    u=usr['fullname'], r=', '.join(x.brief for x in u) ))
        elif 'fullname' in usr and not ldap_ok:
            logger.warning('The directory is not available. I can not add a user by their full name. Skipping user {u}.'.format(
                u=usr['fullname']))
        elif 'login' in usr and ldap_ok:
            if '@' in usr['login']:
                u=adm.search_users_p("(&(objectClass=user)(userPrincipalName={login})(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))".format(
                    login=usr['login']),
                    base=Config.LDAP_BASE_DN, user_class_name='user')
            else:
                u=adm.search_users_p("(&(objectClass=user)(sAMAccountName={login})(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))".format(
                    login=usr['login']),
                    base=Config.LDAP_BASE_DN, user_class_name='user')
            if len(u)==1:
                user_obj_list.append(u[0])
            elif len(u)==0:
                logger.warning("User \"{u}\" not found. Skip it.".format(
                    u=usr['login']))
            else:
                logger.warning('Searching for user \"{u}\" returned an ambiguous result: {r}. This should not be!'.format(
                    u=usr['login'], r=', '.join(x.brief for x in u) ))
        elif 'login' in usr and not ldap_ok:
            user_obj_list.append( usr )
    if ldap_ok:
        for usr in user_obj_list:
            cloud.add_user_to_group(usr.principal_name ,ncgroup.group_id)
        ldap_grp=adm.get_group('{lpr}{gr}{lsu}'.format(lpr=LPR,
                lsu=LSU,gr=group_name),'group')
        adm.add_users_to_groups(user_obj_list,[ldap_grp])
    else:
        for usr in user_obj_list:
            cloud.add_user_to_group(usr['login'] ,ncgroup.group_id)

def get_apps(args):
    """Get all installed apps
    """
    if ch and not args.debug:
        ch.setLevel(logging.INFO)
    else:
        ch.setLevel(logging.DEBUG)

    try:
        cloud=ocs.Ocs(Config.CLOUD_USER, Config.CLOUD_USER_PWD,
            Config.CLOUD_BASE_URL)
    except (OperationFailure, WrongParam) as e:
        logger.error('Could not connect to the cloud: {e}'.format(e=e.value))
        exit(1)

    apps=cloud._apps   # cloud.get_apps()
    for itm in apps:
        print(itm)

def get_groupfolders(args):
    """Get all Groupfolders
    """
    if ch and not args.debug:
        ch.setLevel(logging.INFO)
    else:
        ch.setLevel(logging.DEBUG)
    try:
        cloud=ocs.Ocs(Config.CLOUD_USER, Config.CLOUD_USER_PWD,
            Config.CLOUD_BASE_URL)
    except (OperationFailure, WrongParam) as e:
        logger.error('Could not connect to the cloud: {e}'.format(e=e.value))
        exit(1)

    if 'groupfolders' not in cloud._apps:
        logger.warning('Your server does not support group folder functionality.')
        return
    group_folders=cloud.get_group_folders()
    for itm in group_folders:
        print(itm)

def get_groups(args):
    """Get all cloud groups
    """
    if ch and not args.debug:
        ch.setLevel(logging.INFO)
    else:
        ch.setLevel(logging.DEBUG)
    try:
        cloud=ocs.Ocs(Config.CLOUD_USER, Config.CLOUD_USER_PWD,
            Config.CLOUD_BASE_URL)
    except (OperationFailure, WrongParam) as e:
        logger.error('Could not connect to the cloud: {e}'.format(e=e.value))
        exit(1)
    groups=cloud.get_groups()
    for itm in groups:
        print(itm.info)

def get_group_members(args):
    """Get members of the group
    """
    if ch and not args.debug:
        ch.setLevel(logging.INFO)
    else:
        ch.setLevel(logging.DEBUG)
    group_name=args.name
    try:
        cloud=ocs.Ocs(Config.CLOUD_USER, Config.CLOUD_USER_PWD,
            Config.CLOUD_BASE_URL)
    except (OperationFailure, WrongParam) as e:
        logger.error('Could not connect to the cloud: {e}'.format(e=e.value))
        exit(1)
    members=cloud.get_group_members(group_name)
    for itm in members:
        print(itm)

def get_group_permissions(args):
    """Get permissions of the group
    """
    if ch and not args.debug:
        ch.setLevel(logging.INFO)
    else:
        ch.setLevel(logging.DEBUG)
    group_name=args.name
    group_folder_name=args.groupfolder.lstrip(PREF).rstrip(SUF)
    try:
        cloud=ocs.Ocs(Config.CLOUD_USER, Config.CLOUD_USER_PWD,
            Config.CLOUD_BASE_URL)
    except (OperationFailure, WrongParam) as e:
        logger.error('Could not connect to the cloud: {e}'.format(e=e.value))
        exit(1)

    if 'groupfolders' not in cloud._apps:
        logger.warning('Your server does not support group folder functionality.')
        return
    group_folders=cloud.get_group_folders()
    for gf in group_folders:
        if gf.mount_point==PREF+group_folder_name+SUF:
            for grp in gf.groups:
                if grp.group_id==group_name:
                    print(grp)
                    return
    else:
        logger.warning('Group folder {gp} with group {grp} not found.'.format(
            gp=group_folder_name, grp=group_name))

def get_group_subadmins(args):
    """Get subadmins of the group
    """
    if ch and not args.debug:
        ch.setLevel(logging.INFO)
    else:
        ch.setLevel(logging.DEBUG)
    group_name=args.name
    try:
        cloud=ocs.Ocs(Config.CLOUD_USER, Config.CLOUD_USER_PWD,
            Config.CLOUD_BASE_URL)
    except (OperationFailure, WrongParam) as e:
        logger.error('Could not connect to the cloud: {e}'.format(e=e.value))
        exit(1)

    resp=cloud.get_group_subadmins(group_id=group_name)
    for itm in resp:
        print(itm)

def get_groupfolder(args):
    """Get Groupfoldet info
    """
    if ch and not args.debug:
        ch.setLevel(logging.INFO)
    else:
        ch.setLevel(logging.DEBUG)
    group_folder_name=args.name.lstrip(PREF).rstrip(SUF)
    try:
        cloud=ocs.Ocs(Config.CLOUD_USER, Config.CLOUD_USER_PWD,
            Config.CLOUD_BASE_URL)
    except (OperationFailure, WrongParam) as e:
        logger.error('Could not connect to the cloud: {e}'.format(e=e.value))
        exit(1)

    if 'groupfolders' not in cloud._apps:
        logger.warning('Your server does not support group folder functionality.')
        return
    group_folders=cloud.get_group_folders()
    for gf in group_folders:
        if gf.mount_point==PREF+group_folder_name+SUF:
            print(gf)
            return
    else:
        logger.warning('Group folder {gp} not found.'.format(
            gp=group_folder_name))

def get_users(args):
    """Search/Get users
    """
    if ch and not args.debug:
        ch.setLevel(logging.INFO)
    else:
        ch.setLevel(logging.DEBUG)
    try:
        cloud=ocs.Ocs(Config.CLOUD_USER, Config.CLOUD_USER_PWD,
            Config.CLOUD_BASE_URL)
    except (OperationFailure, WrongParam) as e:
        logger.error('Could not connect to the cloud: {e}'.format(e=e.value))
        exit(1)

    answer=cloud.search_user(search=args.search, limit=args.limit,
        offset=args.offset)
    for itm in answer:
        print(itm)

def get_user(args):
    """Get user details
    """
    if ch and not args.debug:
        ch.setLevel(logging.INFO)
    else:
        ch.setLevel(logging.DEBUG)

    try:
        cloud=ocs.Ocs(Config.CLOUD_USER, Config.CLOUD_USER_PWD,
            Config.CLOUD_BASE_URL)
    except (OperationFailure, WrongParam) as e:
        logger.error('Could not connect to the cloud: {e}'.format(e=e.value))
        exit(1)

    try:
        answer=cloud.get_user(user_id=args.login)
    except OperationFailure as e:
        logger.error('Error: {v}'.format(v=e.value))
        return
    for itm in answer:
        print(itm)

def get_groupfolder_members(args):
    """All users of all group folder groups.
    """
    if ch and not args.debug:
        ch.setLevel(logging.INFO)
    else:
        ch.setLevel(logging.DEBUG)
    group_folder_name=args.name.lstrip(PREF).rstrip(SUF)
    try:
        cloud=ocs.Ocs(Config.CLOUD_USER, Config.CLOUD_USER_PWD,
            Config.CLOUD_BASE_URL)
    except (OperationFailure, WrongParam) as e:
        logger.error('Could not connect to the cloud: {e}'.format(e=e.value))
        exit(1)

    if 'groupfolders' not in cloud._apps:
        logger.warning('Your server does not support group folder functionality.')
        return
    group_folders=cloud.get_group_folders()
    for gf in group_folders:
        if gf.mount_point==PREF+group_folder_name+SUF:
            for grp in gf.groups:
                print(grp)
                members=cloud.get_group_members(grp.group_id)
                for itm in members:
                    print(itm)
            return
    else:
        logger.warning('Group folder {gp} not found.'.format(
            gp=group_folder_name))

def set_groupfolder_quota(args):
    """Set new quota for Groupfolder
    """
    if ch and not args.debug:
        ch.setLevel(logging.INFO)
    else:
        ch.setLevel(logging.DEBUG)
    quota=get_quote_bytes(args.quota)
    group_folder_name=args.name.lstrip(PREF).rstrip(SUF)
    try:
        cloud=ocs.Ocs(Config.CLOUD_USER, Config.CLOUD_USER_PWD,
            Config.CLOUD_BASE_URL)
    except (OperationFailure, WrongParam) as e:
        logger.error('Could not connect to the cloud: {e}'.format(e=e.value))
        exit(1)

    if 'groupfolders' not in cloud._apps:
        logger.warning('Your server does not support group folder functionality.')
        return
    group_folders=cloud.get_group_folders()
    for gf in group_folders:
        if gf.mount_point==PREF+group_folder_name+SUF:
            cloud.set_group_folder_quota(gf.id,quota)
            return
    else:
        logger.warning('Group folder {gp} not found.'.format(
            gp=group_folder_name))

def set_groupfolder_name(args):
    """Set new name for groupfolder (rename).
    """
    if ch and not args.debug:
        ch.setLevel(logging.INFO)
    else:
        ch.setLevel(logging.DEBUG)
    group_folder_name=args.name.lstrip(PREF).rstrip(SUF)
    new_group_folder_name=args.newname.lstrip(PREF).rstrip(SUF)
    try:
        cloud=ocs.Ocs(Config.CLOUD_USER, Config.CLOUD_USER_PWD,
            Config.CLOUD_BASE_URL)
    except (OperationFailure, WrongParam) as e:
        logger.error('Could not connect to the cloud: {e}'.format(e=e.value))
        exit(1)

    if 'groupfolders' not in cloud._apps:
        logger.warning('Your server does not support group folder functionality.')
        return
    group_folders=cloud.get_group_folders()
    for gf in group_folders:
        if gf.mount_point==PREF+group_folder_name+SUF:
            cloud.rename_group_folder(gf.id,PREF+new_group_folder_name+SUF)
            return
    else:
        logger.warning('Group folder {gp} not found.'.format(
            gp=group_folder_name))

def set_group_permissions(args):
    """Set permissions for group on groupfolder
    """
    if ch and not args.debug:
        ch.setLevel(logging.INFO)
    else:
        ch.setLevel(logging.DEBUG)
    group_name=args.name
    group_folder_name=args.groupfolder.lstrip(PREF).rstrip(SUF)
    permissions=sum( str_to_permissions(x) for x in args.permissions )
    try:
        cloud=ocs.Ocs(Config.CLOUD_USER, Config.CLOUD_USER_PWD,
            Config.CLOUD_BASE_URL)
    except (OperationFailure, WrongParam) as e:
        logger.error('Could not connect to the cloud: {e}'.format(e=e.value))
        exit(1)

    if 'groupfolders' not in cloud._apps:
        logger.warning('Your server does not support group folder functionality.')
        return
    group_folders=cloud.get_group_folders()
    for gf in group_folders:
        if gf.mount_point==PREF+group_folder_name+SUF:
            cloud.set_group_folder_group_permissions(gfolder_id=gf.id,
                group_id=group_name, permissions=permissions)
            return
    else:
        logger.warning('Group folder {gp} not found.'.format(
            gp=group_folder_name))

def set_group_subadmins(args):
    """Set user as group subadmin
    """
    if ch and not args.debug:
        ch.setLevel(logging.INFO)
    else:
        ch.setLevel(logging.DEBUG)
    group_name = args.name
    if is_login(args.login):
        login = args.login
    else:
        logger.warning('It does not look like it is {l} login.'.format(l=args.login))
        return
    try:
        cloud=ocs.Ocs(Config.CLOUD_USER, Config.CLOUD_USER_PWD,
            Config.CLOUD_BASE_URL)
    except (OperationFailure, WrongParam) as e:
        logger.error('Could not connect to the cloud: {e}'.format(e=e.value))
        exit(1)

    cloud.set_group_subadmins(group_name,login)

def set_user(args):
    """Set/change user parameters
    """
    if ch and not args.debug:
        ch.setLevel(logging.INFO)
    else:
        ch.setLevel(logging.DEBUG)
    if is_login(args.login):
        login = args.login
    else:
        logger.warning('It does not look like it is {l} login.'.format(l=args.login))
        return
    try:
        cloud=ocs.Ocs(Config.CLOUD_USER, Config.CLOUD_USER_PWD,
            Config.CLOUD_BASE_URL)
    except (OperationFailure, WrongParam) as e:
        logger.error('Could not connect to the cloud: {e}'.format(e=e.value))
        exit(1)
    cloud.set_user(user_id=login,**vars(args))

def set_user_enable(args):
    """Enable user
    """
    if ch and not args.debug:
        ch.setLevel(logging.INFO)
    else:
        ch.setLevel(logging.DEBUG)
    if is_login(args.login):
        login = args.login
    else:
        logger.warning('It does not look like it is {l} login.'.format(l=args.login))
        return
    try:
        cloud=ocs.Ocs(Config.CLOUD_USER, Config.CLOUD_USER_PWD,
            Config.CLOUD_BASE_URL)
    except (OperationFailure, WrongParam) as e:
        logger.error('Could not connect to the cloud: {e}'.format(e=e.value))
        exit(1)
    cloud.enable_user(login)

def set_user_disable(args):
    """Disable user
    """
    if ch and not args.debug:
        ch.setLevel(logging.INFO)
    else:
        ch.setLevel(logging.DEBUG)
    if is_login(args.login):
        login = args.login
    else:
        logger.warning('It does not look like it is {l} login.'.format(l=args.login))
        return
    try:
        cloud=ocs.Ocs(Config.CLOUD_USER, Config.CLOUD_USER_PWD,
            Config.CLOUD_BASE_URL)
    except (OperationFailure, WrongParam) as e:
        logger.error('Could not connect to the cloud: {e}'.format(e=e.value))
        exit(1)
    cloud.disable_user(login)

def command_line():
    """CLI parser
    """
    debug_help_message= 'Enable debugging.'
    quota_help_message = 'Sets a quota for a group. '+\
        'You can use the modifiers k, m, g, t. For example 5g.'
    user_quota_help_message = 'Sets a quota for a user. '+\
        'You can use the modifiers k, m, g, t. For example 5g.'
    usersfile_help_message = 'The path to the file with users (by full name or login in the line).'
    groupfolder_help_message = 'The name of the group folder.'
    groupname_help_message = 'The name of the group in the cloud (without prefix and suffix).'
    groupname2_help_message = 'The name of the group in the cloud.'
    fullname_help_message = 'Full username.'
    login_help_message = 'User login.'
    newfoldername_help_message = 'New group folder name.'
#    human_help_message = 'Вывести данные в человекочитаемом формате'
    usrs_search_help_message = 'Search string by full username.'
    usrs_limit_help_message = 'Limit the output to the specified number of records.'
    usrs_offset_help_message = 'Offset output on a given number of records.'
    password_help_message = 'User password.'
    email_help_message = 'User email.'
    phone_help_message = 'User phone.'
    address_help_message = 'User address.'
    website_help_message = 'User website.'
    twitter_help_message = "Twitter user."
    displayname_help_message = 'User display name.'
    permissions_help_message = \
'''Permissions can be set to the following values:
        r - read permission
        c - permission to create files and folders
        u - permission to modify
        d - permission to delete
        s - permission to share
        a - permission to full access'''
    permissions_choice = ['r','c','u','d','s','a']
    """list of str: permissions choice list:
        r - read permission
        c - create permission
        u - update permission
        d - delete permission
        s - share permission
        a - all above permissions
    """
    #: str: default permissions if parameter is not set
    permissions_default = PERMISSION_DEFAULT_STR
    quota_default = str(ocs.human_size(DEFAULT_QUOTA)) #'5g'
    parser = argparse.ArgumentParser(
            #prog=os.path.basename(__file__),
            prog='pnc',
            description=textwrap.dedent(
'''Python NextCloud Command Line Interface:

list of commands menu:

 new     create menu
 del     delete menu
 get     get menu
 add     add menu
 set     change menu
'''), formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--version', action='version',
        version='{pr} {ver}'.format(
        pr=prog_name,
        ver=prog_ver))

    subparsers = parser.add_subparsers(dest="top")

    new__group = subparsers.add_parser('new',description=textwrap.dedent(
'''create:

 groupfolder  cloud Group Folder
 group        cloud Group
 user         cloud User (local cloud user)
'''), formatter_class=argparse.RawDescriptionHelpFormatter)

    del__group = subparsers.add_parser('del',description=textwrap.dedent(
'''delete:

 group-member     cloud user from Group
 group            cloud Group
 group-link       unlink cloud Group from GroupFolder
 groupfolder      cloud Group Folder
 group-subadmin   subadmin of the cloud Group
 user             delete user
'''), formatter_class=argparse.RawDescriptionHelpFormatter)

    get__group = subparsers.add_parser('get',description=textwrap.dedent(
'''get:

 apps                 installed cloud applications
 groups               all cloud Groups,
 groupfolders         all cloud GroupFolders
 group-members        Group members
 group-permissions    permissions for the Group on GroupFolder
 group-subadmins      all subadmins of the group
 groupfolder          GroupFolder details
 groupfolder-members  members all Groups for the GroupFolder
 users                (search) Users by name (Launched without keys gives a list of all users)
 user                 User details
'''), formatter_class=argparse.RawDescriptionHelpFormatter)

    add__group = subparsers.add_parser('add',description=textwrap.dedent(
'''add:

 group     Group to the GroupFolder
 user      User to the Group
 users     Users from file to the Group
'''), formatter_class=argparse.RawDescriptionHelpFormatter)

    set__group = subparsers.add_parser('set',description=textwrap.dedent(
'''set:

 groupfolder-quota   GroupFoldet quota
 groupfolder-name    rename GroupFolder
 group-permissions   permissions for the Group
 group-subadmin      subadmins for the Group
 user                change user parameters
 user-disable        disable user
 user-enable         enable user
'''), formatter_class=argparse.RawDescriptionHelpFormatter)

    # new
    #===============================================
    subparsers = new__group.add_subparsers(dest="new")

    gf_new = subparsers.add_parser('groupfolder')

    gf_new.add_argument('-n','--name', action='store',
        required=True,
        help=groupfolder_help_message)
    gf_new.add_argument('-p','--permissions',
        action='store',
                choices=permissions_choice,
        default=[permissions_default],
        type=str,
        nargs='*',
        help=permissions_help_message)
    gf_new.add_argument('-q','--quota', action='store',
        default=quota_default,
        type=str,
        help=quota_help_message)
    gf_new.add_argument('-u','--usersfile', action='store',
        required=True,
        type=argparse.FileType('r',encoding='utf8'),
        help=usersfile_help_message)
    gf_new.add_argument('-d','--debug',  help=debug_help_message)
    gf_new.set_defaults(func=new_groupfolder)

    #-------------------------------------------------
    grp_new = subparsers.add_parser('group')
    grp_new.add_argument('-n','--name', action='store',
        type=str,
        required=True,
        help=groupname_help_message)
    grp_new.add_argument('-u','--usersfile', action='store',
        required=True,
        type=argparse.FileType('r',encoding='utf8'),
        help=usersfile_help_message)
    grp_new.add_argument('-d','--debug', help=debug_help_message)
    grp_new.set_defaults(func=new_group)
    #-------------------------------------------------------------
    usr_new = subparsers.add_parser('user')
    usr_new.add_argument('-l','--login', action='store',
        type=str,
        required=True,
        help=login_help_message)
    usr_new.add_argument('-p','--password', action='store',
        type=str,
        required=True,
        help=password_help_message)
    usr_new.add_argument('-e','--email', action='store',
        type=str,
        help=email_help_message)
    usr_new.add_argument('-i','--displayname', action='store',
        type=str,
        help=displayname_help_message)
    usr_new.add_argument('-q','--quota', action='store',
        type=str,
        help=user_quota_help_message)
    usr_new.add_argument('-m','--phone', action='store',
        type=str,
        help=phone_help_message)
    usr_new.add_argument('-a','--address', action='store',
        type=str,
        help=address_help_message)
    usr_new.add_argument('-w','--website', action='store',
        type=str,
        help=website_help_message)
    usr_new.add_argument('-t','--twitter', action='store',
        type=str,
        help=twitter_help_message)
    usr_new.add_argument('-g','--group', action='append',
        type=str,
        #nargs='*',
        #default=[],
        help=groupname2_help_message)
    usr_new.add_argument('-d','--debug',  help=debug_help_message)
    usr_new.set_defaults(func=new_user)
    # del
    #===============================================
    subparsers = del__group.add_subparsers(dest='del')
    grp_mem_del = subparsers.add_parser('group-member')
    grp_mem_del.add_argument('-n','--name', action='store',
        type=str,
        required=True,
        help=groupname_help_message)
    grp_mem_del.add_argument('-f','--fullname', action='store',
        type=str,
        help=fullname_help_message)
    grp_mem_del.add_argument('-l','--login', action='store',
        type=str,
        help=login_help_message)
    grp_mem_del.add_argument('-d','--debug',  help=debug_help_message)
    grp_mem_del.set_defaults(func=del_group_member)
    #-------------------------------------------------------------
    grp_del = subparsers.add_parser('group')
    grp_del.add_argument('-n','--name', action='store',
        type=str,
        required=True,
        help=groupname_help_message)
    grp_del.add_argument('-d','--debug',  help=debug_help_message)
    grp_del.set_defaults(func=del_group)
    #-------------------------------------------------------------
    grp_link_del = subparsers.add_parser('group-link')
    grp_link_del.add_argument('-n','--name', action='store',
        type=str,
        required=True,
        help=groupname_help_message)
    grp_link_del.add_argument('-f','--groupfolder', action='store',
        type=str,
        required=True,
        help=groupfolder_help_message)
    grp_link_del.add_argument('-d','--debug',  help=debug_help_message)
    grp_link_del.set_defaults(func=del_group_link)
    #-------------------------------------------------------------
    gf_del = subparsers.add_parser('groupfolder')
    gf_del.add_argument('-n','--name', action='store',
        type=str,
        required=True,
        help=groupfolder_help_message)
    gf_del.add_argument('-d','--debug',  help=debug_help_message)
    gf_del.set_defaults(func=del_groupfolder)
    #-------------------------------------------------------------
    grp_sub_del = subparsers.add_parser('group-subadmin')
    grp_sub_del.add_argument('-n','--name', action='store',
        type=str,
        required=True,
        help=groupname_help_message)
    grp_sub_del.add_argument('-l','--login', action='store',
        type=str,
        required=True,
        help=login_help_message)
    grp_sub_del.add_argument('-d','--debug',  help=debug_help_message)
    grp_sub_del.set_defaults(func=del_group_subadmins)
    #-------------------------------------------------------------
    usr_del = subparsers.add_parser('user')
    usr_del.add_argument('-l','--login', action='store',
        type=str,
        required=True,
        help=login_help_message)
    usr_del.add_argument('-d','--debug',  help=debug_help_message)
    usr_del.set_defaults(func=del_user)
    # get
    #===============================================
    subparsers = get__group.add_subparsers(dest='get')
    apps_get = subparsers.add_parser('apps')
    apps_get.add_argument('-d','--debug',  help=debug_help_message)
    apps_get.set_defaults(func=get_apps)
    #-------------------------------------------------------------
    grps_get = subparsers.add_parser('groups')
    grps_get.add_argument('-d','--debug',  help=debug_help_message)
    grps_get.set_defaults(func=get_groups)
    #-------------------------------------------------------------
    gfs_get = subparsers.add_parser('groupfolders')
    gfs_get.add_argument('-d','--debug',  help=debug_help_message)
    gfs_get.set_defaults(func=get_groupfolders)
    #-------------------------------------------------------------
    grp_mem_get = subparsers.add_parser('group-members')
    grp_mem_get.add_argument('-n','--name', action='store',
        type=str,
        required=True,
        help=groupname_help_message)
    grp_mem_get.add_argument('-d','--debug',  help=debug_help_message)
    grp_mem_get.set_defaults(func=get_group_members)
    #-------------------------------------------------------------

    grper_get = subparsers.add_parser('group-permissions')
    grper_get.add_argument('-n','--name', action='store',
        type=str,
        required=True,
        help=groupname_help_message)
    grper_get.add_argument('-f','--groupfolder', action='store',
        type=str,
        required=True,
        help=groupfolder_help_message)
    grper_get.add_argument('-d','--debug', help=debug_help_message)
    grper_get.set_defaults(func=get_group_permissions)
    #-------------------------------------------------------------
    grsub_get = subparsers.add_parser('group-subadmins')
    grsub_get.add_argument('-n','--name', action='store',
        type=str,
        required=True,
        help=groupname_help_message)
    grsub_get.add_argument('-d','--debug', help=debug_help_message)
    grsub_get.set_defaults(func=get_group_subadmins)
    #-------------------------------------------------------------

    gf_get = subparsers.add_parser('groupfolder')
    gf_get.add_argument('-n','--name', action='store',
        type=str,
        required=True,
        help=groupfolder_help_message)
    gf_get.add_argument('-d','--debug',  help=debug_help_message)
    gf_get.set_defaults(func=get_groupfolder)
    #-------------------------------------------------------------
    gfm_get = subparsers.add_parser('groupfolder-members')
    gfm_get.add_argument('-n','--name', action='store',
        type=str,
        required=True,
        help=groupfolder_help_message)
    gfm_get.add_argument('-d','--debug',  help=debug_help_message)
    gfm_get.set_defaults(func=get_groupfolder_members)
    #-------------------------------------------------------------
    usr_get = subparsers.add_parser('user')
    usr_get.add_argument('-l','--login', action='store',
        type=str,
        required=True,
        help=login_help_message)
    usr_get.add_argument('-d','--debug',  help=debug_help_message)
    usr_get.set_defaults(func=get_user)
    #-------------------------------------------------------------
    usrs_get = subparsers.add_parser('users')
    usrs_get.add_argument('-s','--search', action='store',
        type=str,
        help=usrs_search_help_message)
    usrs_get.add_argument('-l','--limit', action='store',
        type=int,
        help=usrs_limit_help_message)
    usrs_get.add_argument('-o','--offset', action='store',
        type=int,
        help=usrs_offset_help_message)
    usrs_get.add_argument('-d','--debug',  help=debug_help_message)
    usrs_get.set_defaults(func=get_users)

    # add
    #===========================================================
    subparsers = add__group.add_subparsers(dest='add')
    grp_add = subparsers.add_parser('group')
    grp_add.add_argument('-n','--name', action='store',
        type=str,
        required=True,
        help=groupname_help_message)
    grp_add.add_argument('-f','--groupfolder', action='store',
        type=str,
        required=True,
        help=groupfolder_help_message)
    grp_add.add_argument('-p','--permissions', action='store',
        choices=permissions_choice,
        default=[permissions_default],
        type=str,
        nargs='*',
        help=permissions_help_message)
    grp_add.add_argument('-d','--debug',  help=debug_help_message)
    grp_add.set_defaults(func=add_group)
    #-------------------------------------------------------------
    usr_add = subparsers.add_parser('user')
    usr_add.add_argument('-n','--name', action='store',
        type=str,
        help=fullname_help_message)
    usr_add.add_argument('-g','--group', action='store',
        type=str,
        required=True,
        help=groupname_help_message)
    usr_add.add_argument('-l','--login', action='store',
        type=str,
        help=login_help_message)
    usr_add.add_argument('-d','--debug',  help=debug_help_message)
    usr_add.set_defaults(func=add_user)
    #-------------------------------------------------------------
    usrs_add = subparsers.add_parser('users')
    usrs_add.add_argument('-u','--usersfile', action='store',
        required=True,
        type=argparse.FileType('r',encoding='utf8'),
        help=usersfile_help_message)
    usrs_add.add_argument('-g','--group', action='store',
        type=str,
        required=True,
        help=groupname_help_message)
    usrs_add.add_argument('-d','--debug',  help=debug_help_message)
    usrs_add.set_defaults(func=add_users)
    # set
    #===========================================================
    subparsers = set__group.add_subparsers(dest='set')
    gfq_set = subparsers.add_parser('groupfolder-quota')
    gfq_set.add_argument('-n','--name', action='store',
        type=str,
        required=True,
        help=groupfolder_help_message)
    gfq_set.add_argument('-q','--quota', action='store',
        type=str,
        required=True,
        help=quota_help_message)
    gfq_set.add_argument('-d','--debug',  help=debug_help_message)
    gfq_set.set_defaults(func=set_groupfolder_quota)
    #-------------------------------------------------------------

    gf_nm_set = subparsers.add_parser('groupfolder-name')
    gf_nm_set.add_argument('-n','--name', action='store',
        type=str,
        required=True,
        help=groupfolder_help_message)
    gf_nm_set.add_argument('-w','--newname', action='store',
        type=str,
        required=True,
        help=newfoldername_help_message)
    gf_nm_set.add_argument('-d','--debug',  help=debug_help_message)
    gf_nm_set.set_defaults(func=set_groupfolder_name)
    #-------------------------------------------------------------
    grp_per_set = subparsers.add_parser('group-permissions')
    grp_per_set.add_argument('-n','--name', action='store',
        type=str,
        required=True,
        help=groupname_help_message)
    grp_per_set.add_argument('-f','--groupfolder', action='store',
        type=str,
        required=True,
        help=groupfolder_help_message)
    grp_per_set.add_argument('-p','--permissions',
        choices=permissions_choice,
        default=[permissions_default],
        type=str,
        nargs='*',
        help=permissions_help_message)
    grp_per_set.add_argument('-d','--debug',  help=debug_help_message)
    grp_per_set.set_defaults(func=set_group_permissions)
    #-------------------------------------------------------------
    grp_sub_set = subparsers.add_parser('group-subadmin')
    grp_sub_set.add_argument('-n','--name', action='store',
        type=str,
        required=True,
        help=groupname_help_message)
    grp_sub_set.add_argument('-l','--login', action='store',
        type=str,
        required=True,
        help=login_help_message)
    grp_sub_set.add_argument('-d','--debug',  help=debug_help_message)
    grp_sub_set.set_defaults(func=set_group_subadmins)
    #-------------------------------------------------------------
    usr_set = subparsers.add_parser('user')
    usr_set.add_argument('-l','--login', action='store',
        type=str,
        required=True,
        help=login_help_message)
    usr_set.add_argument('-p','--password', action='store',
        type=str,
        #required=True,
        help=password_help_message)
    usr_set.add_argument('-e','--email', action='store',
        type=str,
        help=email_help_message)
    usr_set.add_argument('-i','--displayname', action='store',
        type=str,
        help=displayname_help_message)
    usr_set.add_argument('-q','--quota', action='store',
        type=str,
        help=user_quota_help_message)
    usr_set.add_argument('-m','--phone', action='store',
        type=str,
        help=phone_help_message)
    usr_set.add_argument('-a','--address', action='store',
        type=str,
        help=address_help_message)
    usr_set.add_argument('-w','--website', action='store',
        type=str,
        help=website_help_message)
    usr_set.add_argument('-t','--twitter', action='store',
        type=str,
        help=twitter_help_message)
    usr_set.add_argument('-d','--debug',  help=debug_help_message)
    usr_set.set_defaults(func=set_user)
    #-------------------------------------------------------------
    usr_en_set = subparsers.add_parser('user-enable')
    usr_en_set.add_argument('-l','--login', action='store',
        type=str,
        required=True,
        help=login_help_message)
    usr_en_set.add_argument('-d','--debug',  help=debug_help_message)
    usr_en_set.set_defaults(func=set_user_enable)
    #-------------------------------------------------------------
    usr_di_set = subparsers.add_parser('user-disable')
    usr_di_set.add_argument('-l','--login', action='store',
        type=str,
        required=True,
        help=login_help_message)
    usr_di_set.add_argument('-d','--debug',  help=debug_help_message)
    usr_di_set.set_defaults(func=set_user_disable)

    args = parser.parse_args()

    try:
        args.func(args)
    except AttributeError as e: # closed bug: https://github.com/datalad/datalad/issues/848
        logger
        args = parser.parse_args([args.top,'-h'])
        args.func(args)

def main():
    global logger
    logger = logging.getLogger('ocs')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]')
    formatter_console = logging.Formatter('%(message)s')

    if bool(Config.LOG_TO_STDOUT):
        global ch
        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        # add formatter to ch
        ch.setFormatter(formatter_console)
        # add ch to logger
        logger.addHandler(ch)

    file_handler = RotatingFileHandler(Config.LOG_FILE,
                                       maxBytes=Config.LOG_MAX_BYTES,
                                       backupCount=Config.LOG_BACKUP_COUNT,
                                       encoding='utf-8')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

    logger.debug(">>>>>>>>>>")
    command_line()
    logger.debug("<<<<<<<<<<")


if __name__ == '__main__':
    ch=None
    logger = logging.getLogger('ocs')
    main()
