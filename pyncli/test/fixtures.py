# -*- coding: UTF-8 -*-
# -------------------------------------------------------------------------------
# Name:        fixtures
# Purpose:     fixtures for testing
#
# Author:      Evgeniy Semenov
#
# Created:     25.03.2019
# Copyright:   (c) evgeniy.semenov 2019
# Licence:     MIT
# -------------------------------------------------------------------------------

TEST_XML_RESPONSE_APP_LDAP = """<ocs>
 <meta>
  <status>ok</status>
  <statuscode>100</statuscode>
  <message>OK</message>
  <totalitems></totalitems>
  <itemsperpage></itemsperpage>
 </meta>
 <data>
  <apps>
   <element>encryption</element>
   <element>theming</element>
   <element>nextcloud_announcements</element>
   <element>files_trashbin</element>
   <element>files_pdfviewer</element>
   <element>files_texteditor</element>
   <element>notifications</element>
   <element>comments</element>
   <element>files_external</element>
   <element>activity</element>
   <element>survey_client</element>
   <element>systemtags</element>
   <element>accessibility</element>
   <element>updatenotification</element>
   <element>serverinfo</element>
   <element>admin_audit</element>
   <element>files_sharing</element>
   <element>password_policy</element>
   <element>federation</element>
   <element>gallery</element>
   <element>user_ldap</element>
   <element>sharebymail</element>
   <element>files_versions</element>
   <element>logreader</element>
   <element>firstrunwizard</element>
   <element>support</element>
   <element>files_videoplayer</element>
   <element>bruteforcesettings</element>
   <element>calendar</element>
   <element>user_saml</element>
   <element>user_external</element>
   <element>tasks</element>
   <element>notes</element>
   <element>groupfolders</element>
   <element>contacts</element>
  </apps>
 </data>
</ocs>"""

TEST_XML_RESPONSE_OK = """<ocs>
 <meta>
  <status>ok</status>
  <statuscode>100</statuscode>
  <message>OK</message>
  <totalitems></totalitems>
  <itemsperpage></itemsperpage>
 </meta>
 <data/>
</ocs>
"""

TEST_XML_RESPONSE_FAILURE = """<ocs>
 <meta>
  <status>failure</status>
  <statuscode>997</statuscode>
  <message>Current user is not logged in</message>
  <totalitems></totalitems>
  <itemsperpage></itemsperpage>
 </meta>
 <data/>
</ocs>
"""

TEST_XML_RESPONSE_GROUPFOLDERS = """<ocs>
 <meta>
  <status>ok</status>
  <statuscode>100</statuscode>
  <message>OK</message>
  <totalitems></totalitems>
  <itemsperpage></itemsperpage>
 </meta>
 <data>
  <element>
   <id>1</id>
   <mount_point>{IT}</mount_point>
   <groups>
    <element group_id="IT" permissions="31"/>
   </groups>
   <quota>-3</quota>
   <size>39136618129</size>
  </element>
  <element>
   <id>2</id>
   <mount_point>{FIS}</mount_point>
   <groups>
    <element group_id="FIS" permissions="31"/>
   </groups>
   <quota>32212254720</quota>
   <size>11052652856</size>
  </element>
  <element>
   <id>19</id>
   <mount_point>{SECURITY}</mount_point>
   <groups>
    <element group_id="SECURITY" permissions="31"/>
   </groups>
   <quota>21474836480</quota>
   <size>6834174935</size>
  </element>
  <element>
   <id>22</id>
   <mount_point>{TEST_NC1}</mount_point>
   <groups>
    <element group_id="TEST_NC1" permissions="31"/>
   </groups>
   <quota>8589934592</quota>
   <size>113153</size>
  </element>
 </data>
</ocs>
"""

TEST_XML_RESPONSE_GROUPS = """<ocs>
 <meta>
  <status>ok</status>
  <statuscode>100</statuscode>
  <message>OK</message>
  <totalitems></totalitems>
  <itemsperpage></itemsperpage>
 </meta>
 <data>
  <groups>
   <element>FIS</element>
   <element>IT</element>
   <element>PHD</element>
   <element>SECURITY</element>
   <element>TEST_NC1</element>
  </groups>
 </data>
</ocs>
"""

TEST_XML_RESPONSE_CTEATE_GROUPFOLDER = """<ocs>
 <meta>
  <status>ok</status>
  <statuscode>100</statuscode>
  <message>OK</message>
  <totalitems></totalitems>
  <itemsperpage></itemsperpage>
 </meta>
 <data>
  <id>13</id>
  <groups/>
 </data>
</ocs>
"""

TEST_XML_RESPONSE_GROUP_MEMBERS = """<ocs>
 <meta>
  <status>ok</status>
  <statuscode>100</statuscode>
  <message>OK</message>
  <totalitems></totalitems>
  <itemsperpage></itemsperpage>
 </meta>
 <data>
  <users>
   <element>tester1@example.com</element>
   <element>tester2@example.com</element>
   <element>tester3@example.com</element>
   <element>tester4@example.com</element>
   <element>tester5@example.com</element>
  </users>
 </data>
</ocs>
"""

TEST_XML_RESPONSE_USER = """<ocs>
 <meta>
  <status>ok</status>
  <statuscode>100</statuscode>
  <message>OK</message>
  <totalitems></totalitems>
  <itemsperpage></itemsperpage>
 </meta>
 <data>
  <enabled>1</enabled>
  <id>tester1@example.com</id>
  <storageLocation>/home/nextcloud/tester1@example.com</storageLocation>
  <lastLogin>1544530113000</lastLogin>
  <backend>LDAP</backend>
  <subadmin>
    <element>testers</element>
  </subadmin>
  <quota>
   <free>8305925677</free>
   <used>2431492563</used>
   <total>10737418240</total>
   <relative>22.65</relative>
   <quota>10737418240</quota>
  </quota>
  <email/>
  <displayname>Пупкин Василий Алибабаевич</displayname>
  <phone>+3333333333</phone>
  <address>Russia, St. Petersburg</address>
  <website>https://www.example.com</website>
  <twitter>@_twitt_me_</twitter>
  <groups>
   <element>testers</element>
   <element>staff</element>
  </groups>
  <language>ru</language>
  <locale></locale>
  <backendCapabilities>
   <setDisplayName></setDisplayName>
   <setPassword></setPassword>
  </backendCapabilities>
 </data>
</ocs>
"""

TEST_XML_RESPONSE_SUBADMINS = """<ocs>
 <meta>
  <status>ok</status>
  <statuscode>100</statuscode>
  <message>OK</message>
  <totalitems></totalitems>
  <itemsperpage></itemsperpage>
 </meta>
 <data>
  <element>admin@example.com</element>
  <element>admin2@example.com</element>
 </data>
</ocs>
"""

TEST_STR_GROUPFOLDER = """<GroupFolder> (10) "share" quota: -3, size: 52.02m
  IT
  Admins"""

TEST_STR_USER = """<User> (user) "Pupkin Vasiliy" enabled: True, e-mail: user@example.com
	backend: LDAP, storage location: /home/nextcloud/user@example.com, last logon: 2018-12-11T15:08:33
	quota: None	phone: +79010010101, twitter: @new_account, website: https://www.leningrad.spb.ru
	address: Russia, Sochi
	language: ru, locale: ru
	<Group> "IT"
	<Group> "tester"
	None"""

TEST_STR_USER_2 = """<User> (alex) "Ivanov Alex" enabled: True, e-mail: alex_hr@example.com
	backend: Database, storage location: /home/nextcloud/alex@example.com, last logon: 1970-01-01T00:00:00
	quota: Quota: 10.00g, used: 2.26g, free: 7.74g, total: 10.00g, relative: 22.65
	phone: +79010010102, twitter: @alex_hr, website: https://www.example.ru
	address: Russia, Surgut
	language: en, locale: en
	<Group> "HR"
	<Group> "staff"
	<BackendCapabilities> setDisplayName: True,  setPassword: True"""

TEST_STR_USER_3_FULL = """<User> (alex) "Ivanov Alex" enabled: True, e-mail: alex_hr@example.com
	backend: Database, storage location: /home/nextcloud/alex@example.com, last logon: 1970-01-01T00:00:00
	quota: Quota: 10.00g, used: 2.26g, free: 7.74g, total: 10.00g, relative: 22.65
	phone: +79010010102, twitter: @alex_hr, website: https://www.example.ru
	address: Russia, Surgut
	language: en, locale: en
	<Group> "HR" [Subadmin]
	<Group> "staff"
	<BackendCapabilities> setDisplayName: True,  setPassword: True"""

TEST_STR_QUOTA = """Quota: 10.00g, used: 2.26g, free: 7.74g, total: 10.00g, relative: 22.65\n"""

TEST_STR_QUOTA_2 = """Quota: 5.00g, used: 0, free: 5.00g, total: 5.00g\n"""

TEST_STR_BACKENDCAPABILITIES = (
    """<BackendCapabilities> setDisplayName: True,  setPassword: True"""
)

TEST_STR_BACKENDCAPABILITIES_2 = (
    """<BackendCapabilities> setDisplayName: False,  setPassword: False"""
)

TEST_STR_GROUPFOLDERS = """<OcsXmlResponse> ok (100): OK
<GroupFolder> (1) "{IT}" quota: -3, size: 36.45g
  <Group> "IT" [cruds]
<GroupFolder> (2) "{FIS}" quota: 30.00g, size: 10.29g
  <Group> "FIS" [cruds]
<GroupFolder> (19) "{SECURITY}" quota: 20.00g, size: 6.36g
  <Group> "SECURITY" [cruds]
<GroupFolder> (22) "{TEST_NC1}" quota: 8.00g, size: 110.50k
  <Group> "TEST_NC1" [cruds]\n"""

TEST_STR_GROUPS = """<OcsXmlResponse> ok (100): OK
<Group> "FIS" [None]
<Group> "IT" [None]
<Group> "PHD" [None]
<Group> "SECURITY" [None]
<Group> "TEST_NC1" [None]\n"""

TEST_STR_CREATE_GROUPFOLDER = """<OcsXmlResponse> ok (100): OK
<CreateGroupFolder> id: 13\n"""

TEST_STR_GROUP_MEMBERS = """<OcsXmlResponse> ok (100): OK
user_id: tester1@example.com
user_id: tester2@example.com
user_id: tester3@example.com
user_id: tester4@example.com
user_id: tester5@example.com\n"""

TEST_STR_GROUPFOLDER_2 = """<OcsXmlResponse> ok (100): OK
<GroupFolder> (13) "None" quota: None, size: None\n"""

TEST_STR_USER_DETAILS = """<OcsXmlResponse> ok (100): OK
<User> (tester1@example.com) "Пупкин Василий Алибабаевич" enabled: True, e-mail: None
	backend: LDAP, storage location: /home/nextcloud/tester1@example.com, last logon: 2018-12-11T15:08:33
	quota: Quota: 10.00g, used: 2.26g, free: 7.74g, total: 10.00g, relative: 22.65
	phone: +3333333333, twitter: @_twitt_me_, website: https://www.example.com
	address: Russia, St. Petersburg
	language: ru, locale: None
	<Group> "testers" [Subadmin]
	<Group> "staff"
	<BackendCapabilities> setDisplayName: False,  setPassword: False\n"""

TEST_LIST_APPS = [
    "encryption",
    "theming",
    "nextcloud_announcements",
    "files_trashbin",
    "files_pdfviewer",
    "files_texteditor",
    "notifications",
    "comments",
    "files_external",
    "activity",
    "survey_client",
    "systemtags",
    "accessibility",
    "updatenotification",
    "serverinfo",
    "admin_audit",
    "files_sharing",
    "password_policy",
    "federation",
    "gallery",
    "user_ldap",
    "sharebymail",
    "files_versions",
    "logreader",
    "firstrunwizard",
    "support",
    "files_videoplayer",
    "bruteforcesettings",
    "calendar",
    "user_saml",
    "user_external",
    "tasks",
    "notes",
    "groupfolders",
    "contacts",
]

TEST_LIST_APPS_OCS = [
    "encryption",
    "theming",
    "nextcloud_announcements",
    "files_trashbin",
    "files_pdfviewer",
    "files_texteditor",
    "notifications",
    "comments",
    "files_external",
    "activity",
    "survey_client",
    "systemtags",
    "accessibility",
    "updatenotification",
    "serverinfo",
    "admin_audit",
    "files_sharing",
    "password_policy",
    "federation",
    "gallery",
    "user_ldap",
    "sharebymail",
    "files_versions",
    "logreader",
    "firstrunwizard",
    "support",
    "files_videoplayer",
    "bruteforcesettings",
    "calendar",
    "user_saml",
    "user_external",
    "tasks",
    "notes",
    "groupfolders",
    "contacts",
    "ocs"
]

TEST_STR_APPS = """<OcsXmlResponse> ok (100): OK
encryption
theming
nextcloud_announcements
files_trashbin
files_pdfviewer
files_texteditor
notifications
comments
files_external
activity
survey_client
systemtags
accessibility
updatenotification
serverinfo
admin_audit
files_sharing
password_policy
federation
gallery
user_ldap
sharebymail
files_versions
logreader
firstrunwizard
support
files_videoplayer
bruteforcesettings
calendar
user_saml
user_external
tasks
notes
groupfolders
contacts\n"""

TEST_STR_SUBADMINS = """<OcsXmlResponse> ok (100): OK
admin@example.com
admin2@example.com\n"""

TEST_XML_RESPONSE_APP_INFO = """<ocs>
  <meta>
    <statuscode>100</statuscode>
    <status>ok</status>
  </meta>
  <data>
    <info/>
    <remote>
      <files>appinfo/remote.php</files>
      <webdav>appinfo/remote.php</webdav>
      <filesync>appinfo/filesync.php</filesync>
    </remote>
    <public/>
    <id>files</id>
    <name>Files</name>
    <description>File Management</description>
    <licence>AGPL</licence>
    <author>Robin Appelman</author>
    <require>4.9</require>
    <shipped>true</shipped>
    <standalone></standalone>
    <default_enable></default_enable>
    <types>
      <element>filesystem</element>
    </types>
  </data>
</ocs>
"""

TEST_STR_APPS_INFO = """<OcsXmlResponse> ok (100): unknown
<AppInfo> (files) "Files" author: Robin Appelman, licence: AGPL
  description: File Management
  require: 4.9, shipped: true, standalone: None
  default_enable: None, public: None, remote: (files: "appinfo/remote.php", webdav: "appinfo/remote.php", filesync: "appinfo/filesync.php")
  types: filesystem, info: None
"""