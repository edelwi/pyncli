# pyncli - Python NextCloud Command Line Interface

[![Build Status](https://travis-ci.org/edelwi/pyncli.svg?branch=master)](https://travis-ci.org/edelwi/pyncli) [![Documentation Status](https://readthedocs.org/projects/pyncli/badge/?version=latest)](https://pyncli.readthedocs.io/en/latest/?badge=latest) [![Coverage Status][coverage-image]][coverage-url]

Main goal of this project is to create command line interface to work with NextCloud Group Folders.


## Installing


```
pip install -i https://test.pypi.org/simple/ pyncli
```

## Configurration

You should set evironment variables like belowe or create .env file in your users home directory to store your credentials and configuration parameters.
Like this:

```sh
# The user of the cloud from which requests will be made.
CLOUD_USER=admin

# Cloud users password.
CLOUD_USER_PWD=admin

# Your NextCloud server URL. Or you can try a demo server, first create it at https://demo.nextcloud.com.
CLOUD_BASE_URL=https://demo.nextcloud.com/random_/

# Print log on console.
LOG_TO_STDOUT=True
# Log file name.
LOG_FILE=pyncli.log

# The maximum size of the log file.
LOG_MAX_BYTES=10240000

# Backups log files count.
LOG_BACKUP_COUNT=12

# User in your LDAP who can create groups in LDAP_SEARCH_FOR_GROUPS location. 
# If you are not using an LDAP server, leave this variable empty and ignore all other variables whose names begin with LDAP_.
LDAP_USER=ad_admin@example.com

# LDAP users password.
LDAP_USER_PWD=very_secret_pass

# Primary LDAP server. Used ldaps bind on port 636 by default.
LDAP_HOST=dc1.example.com

# Additional server, if specified, uses round-robin binding.
LDAP_ADD_SERVER=dc2.example.com

# Base distinctive names, which is used when searching for users.
LDAP_BASE_DN=dc=example,dc=com

# Distinguished name of the group organizational unit used to work with ldap groups.
LDAP_SEARCH_FOR_GROUPS=OU=special_groups,OU=groups,dc=example,dc=com

# Description for created groups.
LDAP_NEW_GROUP_DESCRIPTION="Access group to cloud group"

# The prefix for the name of the ldap group to the corresponding cloud group.
LDAP_GRP_NAME_PREFIX="Cloud_"

# The suffix for the name of the ldap group to the corresponding cloud group.
LDAP_GRP_NAME_SUFFIX=""

# Parent group in which all newly created LDAP groups will be placed.
LDAP_PARENT_GRP_NAME="My_cloud_shares"

# The quota value that will be applied by default unless explicitly specified. Default 5Gb. Set -3 to unlimited.
USER_DEFAULT_QUOTA="5368709120"

# The prefix for the group folder name. So you can help the user to distinguish personal folders from group folders. I use surrounding curly braces.
GF_NAME_PREFIX="{"

# The suffix for the group folder name. So you can help the user to distinguish personal folders from group folders.
GF_NAME_SUFFIX="}"

# The permissions value that will be applied by default unless explicitly specified.
GF_PERMISSION_DEFAULT_STR="r"
  
 
```


## CLI

Command Line menu map

* Create new GroupFolder
```sh
pnc new groupfolder --name (-n) GroupfolderName [--permissions (-p)] rcudsa (default r) [--quota (-q)] (default 5g) --usersfile (-u) filename.txt in utf-8 [--debug (-d)]
```
* Create new Group
```sh
pnc new group --name (-n) GroupName --usersfile (-u) filename.txt in utf-8 [--debug (-d)]
```
* Create new user
```sh
pnc new user --login (-l) UserLogin --password (-p) new password [--email (-e)] email [--displayname (-i)] display name [--quota (-q)] quota [--phone (-m)] phone [--address (-a)] address [--website (-w)] website [--twitter (-t)] twitter [--group (-g)] Group name [--debug (-d)]
```

* Delete member from the group
```sh
pnc del group-member --name (-n) GroupName [--fullname (-f)] UserFullName [--login] UserLogin [--debug (-d)]
```
* Delete Group
```sh
pnc del group --name (-n) GroupName [--debug (-d)]
```
* Unlink group from the groupfolder
```sh
pnc del group-link --name (-n) GroupName --groupfolder (-f) GroupfolderName [--debug (-d)]
```
* Delete Groupfolder
```sh
pnc del groupfolder --name (-n) GroupfolderName [--debug (-d)]
```
* Demote user as group subadmin
```sh
pnc del group-subadmin --name (-n) GroupName --login UserLogin [--debug (-d)]
```
* Delete user
```sh
pnc del user --login (-l) UserLogin [--debug (-d)]
```

* Get all installed apps
```sh
pnc get apps [--debug (-d)]
```
* Get all cloud groups
```sh
pnc get groups [--debug (-d)]
```
* Get all Groupfolders
```sh
pnc get groupfolders [--debug (-d)]
```
* Get members of the group
```sh
pnc get group-members --name (-n) GroupName [--debug (-d)]
```
* Get permissions of the group
```sh
pnc get group-permissions --name (-n) GroupName --groupfolder (-f) GroupfolderName [--debug (-d)]
```
* Get subadmins of the group
```sh
pnc get group-subadmins --name (-n) GroupName [--debug (-d)]
```
* Get Groupfoldet info
```sh
pnc get groupfolder --name (-n) GroupfolderName [--debug (-d)]
```
* All users of all group folder groups
```sh
pnc get groupfolder-members --name (-n) GroupfolderName [--debug (-d)]
```
* Get user details
```sh
pnc get user --login userLogin [--debug (-d)]
```
* Search/Get users
```sh
pnc get users [--search (-s)] UserFullName search string [--limit (-l)] rows count [--offset (-o)] offset from begin [--debug (-d)]
```

* Add Group to the group  folder
```sh
pnc add group --name (-n) GroupNeme --groupfolder (-f) GroupfolderName [--permissions (-p)] rcudsa (default r)   [--debug (-d)]
```
* Add User to the Group
```sh
pnc add user --name (-n) UserFullName --group (-g) GroupeName --login userLogin   [--debug (-d)]
```
* Add Users to the Group
```sh
pnc add users --usersfile (-u) filename.txt in utf-8 --group (-g) GroupeName     [--debug (-d)]
```

* Set new quota for Groupfolder
```sh
pnc set groupfolder-quota --name (-n) GroupfolderName --quota (-q) quota in bytes  [--debug (-d)]
```
* Set new name for groupfolder (rename)
```sh
pnc set groupfolder-name --name (-n) GroupfolderName --newname (-w) NewFolderName  [--debug (-d)]
```
* Set permissions for group on groupfolder
```sh
pnc set group-permissions --name (-n) GroupNeme --groupfolder (-f) GroupfolderName [--permissions (-p)] rcudsa (default r)   [--debug (-d)]
```
* Set user as group subadmin
```sh
pnc set group-subadmin --name (-n) GroupNeme --login UserLogin [--debug (-d)]
```
* Change user parameters
```sh
pnc set user --login (-l) UserLogin [--password (-p)] new password [--email (-e)] email [--displayname (-i)] display name [--quota (-q)] quota [--phone (-m)] phone [--address (-a)] address [--website (-w)] website [--twitter (-t)] twitter [--debug (-d)]
```
* Enable user
```sh
pnc set user-enable --login (-l) UserLogin [--debug (-d)]
```
* Disable user
```sh
pnc set user-disable --login (-l) UserLogin [--debug (-d)]
```

## API
You can use the API in the package to automate administrative tasks associated with the creation and maintenance of group folders, groups and users of the NextClood server.
There are two different API, for work with NextCloud and for ldap.
### NextCloud API
It is python class uses osc web API to NextCloud server.
```python
>>> import pyncli.config
>>> import pyncli.ocs
>>> cloud=ocs.Ocs(Config.CLOUD_USER, Config.CLOUD_USER_PWD, Config.CLOUD_BASE_URL)
>>> cloud.get_apps()
['encryption',
 'theming',
 'serverinfo',
 'admin_audit',
 'files_sharing',
 ...
 'password_policy',
 'federation',
 'gallery',
 'user_ldap',
 'groupfolders', 
 'contacts']
>>> cloud.get_groups()
[<pyncli.ocs.ocs.Group object at 0x04782310>,
 <pyncli.ocs.ocs.Group object at 0x04782190>,
 ...
 
>>> gr=cloud.get_groups()
>>> for g in gr: 
...     print(g.info)
...     
<Group> "IT"
<Group> "PHD"
<Group> "SECURITY"
<Group> "admin"
 ...
 
print(cloud.get_group_folder(1))
<GroupFolder> (1) "{IT}" quota: -3, size: 36.45g
  <Group> "IT" [cruds] 
```

### ldap API (litle wrapper around fine [ldap3](https://pypi.org/project/ldap3/) library)
If you use ldap backend to NextCloud, it may be useful.


## Documentation

Documentation is available at - [pyncli documentation](https://pyncli.readthedocs.io "see on readthedocs")


## Authors

* **Evgeniy Semenov** - *Initial work* - [edelwi](https://github.com/edelwi/)


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Copyright

Copyright © 2019. Evgeniy Semenov.

[coverage-image]: https://codecov.io/gh/edelwi/pyncli/branch/master/graph/badge.svg
[coverage-url]: https://codecov.io/gh/edelwi/pyncli