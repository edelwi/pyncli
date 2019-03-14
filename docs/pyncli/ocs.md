<h1 id="pyncli.ocs">pyncli.ocs</h1>


<h2 id="pyncli.ocs.ocs">pyncli.ocs.ocs</h2>

This module implements little part of the web API for the NextCloud server.

<h3 id="pyncli.ocs.ocs.human_size">human_size</h3>

```python
human_size(size_in_bytes)
```
Get size in kilo,Mega,Giga... bytes.

<h3 id="pyncli.ocs.ocs.human_permissions">human_permissions</h3>

```python
human_permissions(permissions, short=False)
```
Get permissions in readable form.

<h3 id="pyncli.ocs.ocs.GroupMembers">GroupMembers</h3>

```python
GroupMembers(self, user_id)
```

GroupMembers class

<h3 id="pyncli.ocs.ocs.CreateGroupFolder">CreateGroupFolder</h3>

```python
CreateGroupFolder(self, id)
```

CreateGroupFolder class

<h3 id="pyncli.ocs.ocs.Group">Group</h3>

```python
Group(self, group_id=0, permissions=1)
```

Group class

<h3 id="pyncli.ocs.ocs.GroupFolder">GroupFolder</h3>

```python
GroupFolder(self, id=0, mount_point='nothing', groups=[], quota=-3, size=0)
```

GroupFolder class

<h3 id="pyncli.ocs.ocs.User">User</h3>

```python
User(self, id=0, enabled=True, storageLocation='', lastLogin=0, backend='', subadmin=[], quota=None, email='', displayname='', phone='', address='', website='', twitter='', groups=[], language='ru', locale='ru', backendCapabilities=None)
```

NextCloud User

<h3 id="pyncli.ocs.ocs.UserQuota">UserQuota</h3>

```python
UserQuota(self, quota, used=0, free=None, total=None, relative=None)
```

NextCloud user quota class

<h3 id="pyncli.ocs.ocs.BackendCapabilities">BackendCapabilities</h3>

```python
BackendCapabilities(self, setDisplayName=0, setPassword=0)
```

NectCloud BackendCapabilities class

<h3 id="pyncli.ocs.ocs.Ocs_xml">Ocs_xml</h3>

```python
Ocs_xml(self, xml_text, data_class_name='')
```

NextCloud answer parser class.

<h3 id="pyncli.ocs.ocs.GroupFolderMixin">GroupFolderMixin</h3>

```python
GroupFolderMixin(self, /, *args, **kwargs)
```

GroupFolder Mixin for Ocs class

<h3 id="pyncli.ocs.ocs.Ocs">Ocs</h3>

```python
Ocs(self, cloud_user, cloud_user_pwd, cloud_URL)
```

Class wrapper over ocs.
Dynamically expandable class.

