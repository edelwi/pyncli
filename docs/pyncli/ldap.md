<h1 id="pyncli.ldap">pyncli.ldap</h1>


<h2 id="pyncli.ldap.admexept">pyncli.ldap.admexept</h2>


<h3 id="pyncli.ldap.admexept.AdminException">AdminException</h3>

```python
AdminException(self, value)
```
Root package exception class.

Args:
    value (str): Description of the exception.


<h3 id="pyncli.ldap.admexept.NotEnoughParams">NotEnoughParams</h3>

```python
NotEnoughParams(self, value)
```
Exception class called in case of lack of necessary parameters in the
constructor or method call.

Args:
    value (str): Description of the exception.


<h3 id="pyncli.ldap.admexept.EmptyParam">EmptyParam</h3>

```python
EmptyParam(self, value)
```
Exception class called when a method is called with an empty parameter.

Args:
    value (str): Description of the exception.


<h3 id="pyncli.ldap.admexept.WrongParam">WrongParam</h3>

```python
WrongParam(self, value)
```
The exception class that is called when the method is called as a
parameter of an invalid type or value.

Args:
    value (str): Description of the exception.


<h3 id="pyncli.ldap.admexept.TooLong">TooLong</h3>

```python
TooLong(self, value)
```
Exception class called when the method is called with an invalid length
parameter.

Args:
    value (str): Description of the exception.


<h3 id="pyncli.ldap.admexept.ConnectionFailure">ConnectionFailure</h3>

```python
ConnectionFailure(self, value)
```
Exception class called when it is impossible to connect to the specified
server.

Args:
    value (str): Description of the exception.


<h3 id="pyncli.ldap.admexept.OperationFailure">OperationFailure</h3>

```python
OperationFailure(self, value)
```
Exception class called when it is impossible to perform the specified
operation.

Args:
    value (str): Description of the exception.


<h3 id="pyncli.ldap.admexept.NotFound">NotFound</h3>

```python
NotFound(self, value)
```
Exception class called in case of problems with the search.

Called when the desired object was not found.

Args:
    value (str): Description of the exception.


<h2 id="pyncli.ldap.operate2">pyncli.ldap.operate2</h2>

A module that implements the admin class for working with LDAP.

<h3 id="pyncli.ldap.operate2.admin">admin</h3>

```python
admin(self, ldap_admin, admin_pwd, ldap_server_list)
```

Class for administrative operations

<h2 id="pyncli.ldap.protogroup">pyncli.ldap.protogroup</h2>


<h3 id="pyncli.ldap.protogroup.protogroup">protogroup</h3>

```python
protogroup(self, name, org_unit, **kwargs)
```

base group class

<h2 id="pyncli.ldap.group">pyncli.ldap.group</h2>


<h3 id="pyncli.ldap.group.CleanSetAttrMeta">CleanSetAttrMeta</h3>

```python
CleanSetAttrMeta(self, /, *args, **kwargs)
```
Metaclass to change setattr method

<h3 id="pyncli.ldap.group.group">group</h3>

```python
group(self, name, org_unit='ou=test_ou,dc=example,dc=com', description='', **kwargs)
```

common group class

<h2 id="pyncli.ldap.protoou">pyncli.ldap.protoou</h2>


<h3 id="pyncli.ldap.protoou.CleanSetAttrMeta">CleanSetAttrMeta</h3>

```python
CleanSetAttrMeta(self, /, *args, **kwargs)
```
Metaclass to change setattr method

<h3 id="pyncli.ldap.protoou.protoou">protoou</h3>

```python
protoou(self, name, org_unit, **kwargs)
```

base Organisational Unit class

<h2 id="pyncli.ldap.ou">pyncli.ldap.ou</h2>


<h3 id="pyncli.ldap.ou.ou">ou</h3>

```python
ou(self, name, org_unit='ou=test_ou,dc=example,dc=com', description='', **kwargs)
```

Common Organizational Utit class

<h2 id="pyncli.ldap.protouser">pyncli.ldap.protouser</h2>


<h3 id="pyncli.ldap.protouser.protouser">protouser</h3>

```python
protouser(self, login, **kwargs)
```

Base user class

<h2 id="pyncli.ldap.user">pyncli.ldap.user</h2>


<h3 id="pyncli.ldap.user.CleanSetAttrMeta">CleanSetAttrMeta</h3>

```python
CleanSetAttrMeta(self, /, *args, **kwargs)
```
Metaclass to change setattr method

<h3 id="pyncli.ldap.user.user">user</h3>

```python
user(self, login, uid='', org_unit='OU=test,DC=example,DC=com', surname='', first_name='', middle_name='', company='', department='', division='', position='', mail='', mobile='', other_mailbox='0', other_mobile='0', comment='', employee_type='', acc_control=[<uac.NORMAL_ACCOUNT: 512>, <uac.ACCOUNTDISABLE: 2>], description='', **kwargs)
```

Common user class

<h2 id="pyncli.ldap.uac.uac">uac</h2>

```python
uac(self, /, *args, **kwargs)
```

userAccountControl Enumerator class

<h3 id="pyncli.ldap.uac.uac.ACCOUNTDISABLE">ACCOUNTDISABLE</h3>


userAccountControl Enumerator class

<h3 id="pyncli.ldap.uac.uac.DONT_EXPIRE_PASSWORD">DONT_EXPIRE_PASSWORD</h3>


userAccountControl Enumerator class

<h3 id="pyncli.ldap.uac.uac.DONT_REQ_PREAUTH">DONT_REQ_PREAUTH</h3>


userAccountControl Enumerator class

<h3 id="pyncli.ldap.uac.uac.ENCRYPTED_TEXT_PWD_ALLOWED">ENCRYPTED_TEXT_PWD_ALLOWED</h3>


userAccountControl Enumerator class

<h3 id="pyncli.ldap.uac.uac.hex">hex</h3>

Get hex representation of uac instance

Returns:
    (str): hex representation of uac instance

<h3 id="pyncli.ldap.uac.uac.HOMEDIR_REQUIRED">HOMEDIR_REQUIRED</h3>


userAccountControl Enumerator class

<h3 id="pyncli.ldap.uac.uac.INTERDOMAIN_TRUST_ACCOUNT">INTERDOMAIN_TRUST_ACCOUNT</h3>


userAccountControl Enumerator class

<h3 id="pyncli.ldap.uac.uac.LOCKOUT">LOCKOUT</h3>


userAccountControl Enumerator class

<h3 id="pyncli.ldap.uac.uac.MNS_LOGON_ACCOUNT">MNS_LOGON_ACCOUNT</h3>


userAccountControl Enumerator class

<h3 id="pyncli.ldap.uac.uac.NORMAL_ACCOUNT">NORMAL_ACCOUNT</h3>


userAccountControl Enumerator class

<h3 id="pyncli.ldap.uac.uac.NOT_DELEGATED">NOT_DELEGATED</h3>


userAccountControl Enumerator class

<h3 id="pyncli.ldap.uac.uac.PASSWD_CANT_CHANGE">PASSWD_CANT_CHANGE</h3>


userAccountControl Enumerator class

<h3 id="pyncli.ldap.uac.uac.PASSWD_NOTREQD">PASSWD_NOTREQD</h3>


userAccountControl Enumerator class

<h3 id="pyncli.ldap.uac.uac.PASSWORD_EXPIRED">PASSWORD_EXPIRED</h3>


userAccountControl Enumerator class

<h3 id="pyncli.ldap.uac.uac.SCRIPT">SCRIPT</h3>


userAccountControl Enumerator class

<h3 id="pyncli.ldap.uac.uac.SERVER_TRUST_ACCOUNT">SERVER_TRUST_ACCOUNT</h3>


userAccountControl Enumerator class

<h3 id="pyncli.ldap.uac.uac.SMARTCARD_REQUIRED">SMARTCARD_REQUIRED</h3>


userAccountControl Enumerator class

<h3 id="pyncli.ldap.uac.uac.TEMP_DUPLICATE_ACCOUNT">TEMP_DUPLICATE_ACCOUNT</h3>


userAccountControl Enumerator class

<h3 id="pyncli.ldap.uac.uac.TRUSTED_FOR_DELEGATION">TRUSTED_FOR_DELEGATION</h3>


userAccountControl Enumerator class

<h3 id="pyncli.ldap.uac.uac.TRUSTED_TO_AUTH_FOR_DELEGATION">TRUSTED_TO_AUTH_FOR_DELEGATION</h3>


userAccountControl Enumerator class

<h3 id="pyncli.ldap.uac.uac.USE_DES_KEY_ONLY">USE_DES_KEY_ONLY</h3>


userAccountControl Enumerator class

<h3 id="pyncli.ldap.uac.uac.val">val</h3>

Get value of uac instance

Returns:
    (int): value of uac instance

<h3 id="pyncli.ldap.uac.uac.WORKSTATION_TRUST_ACCOUNT">WORKSTATION_TRUST_ACCOUNT</h3>


userAccountControl Enumerator class

<h3 id="pyncli.ldap.uac.uac.get_status">get_status</h3>

```python
uac.get_status(hex_status_code)
```
Get a list of userAccountControl flags names.

Args:
    hex_status_code (str): userAccountControl hex value

Returns:
    (list): userAccountControl flags names.

<h3 id="pyncli.ldap.uac.uac.get_uac">get_uac</h3>

```python
uac.get_uac(hex_status_code)
```
Get a list of userAccountControl flags.

Args:
    hex_status_code (str): userAccountControl hex value

Returns:
    (list): userAccountControl flags.

<h3 id="pyncli.ldap.uac.uac.get_control">get_control</h3>

```python
uac.get_control(flag_list)
```
Get userAccountControl value.

Args:
    flag_list (list): userAccountControl list

Returns:
    (list): userAccountControl hex value or False.

<h2 id="pyncli.ldap.utill">pyncli.ldap.utill</h2>

Module with auxiliary functions.

<h3 id="pyncli.ldap.utill.download_file">download_file</h3>

```python
download_file(url, local_path, user, pwd)
```
Download file

Downloads a file with basic authentication.

Args:
    url (str): URL
    local_path (str): file full name
    user (str): user name
    pwd (str): password

Returns:
    (str): file full name

Raises:
    ConnectionFailure: connection failure

<h3 id="pyncli.ldap.utill.upload_file">upload_file</h3>

```python
upload_file(url, data, login, pwd)
```
Upload file

Uploads a file with basic authentication.

Args:
    url (str): URL
    data (str): string or buffer to load
    login (str): user name
    pwd (str): password

Returns:
    (str): file full name

Raises:
    OperationFailure: operation failure

<h3 id="pyncli.ldap.utill.mailto">mailto</h3>

```python
mailto(msg_from, msg_to_list, smpt, subject, text)
```
Simple mailto function

Sends a message to one or a group of recipients.

Args:
    msg_from (str): From whom
    msg_to_list (list): List of email recipients.
    smpt (str): SMTP server name or IP
    subject (str): subject of the message
    text (str): text of the message

Raises:
    ConnectionFailure: connection failure

<h3 id="pyncli.ldap.utill.trim">trim</h3>

```python
trim(text)
```
Removes extra spaces from text.

Args:
    text (str): text

Returns:
    (str): processed text

<h3 id="pyncli.ldap.utill.trim_low">trim_low</h3>

```python
trim_low(text)
```
Removes extra spaces from text and set it to lower case.

Args:
    text (str): text

Returns:
    (str): processed text

<h3 id="pyncli.ldap.utill.split_names">split_names</h3>

```python
split_names(fullname)
```
Splits user fullname by surname, first name and middle name.

Args:
    fullname (str): full name (The first word is considered the surname,
        the second first name, all the rest go to the middle name. This
        is the Russian name record format.)

Returns:
    (dict): Dictionary with surname, first name and middle name as
        values.

<h3 id="pyncli.ldap.utill.date_str_to_generalize_time">date_str_to_generalize_time</h3>

```python
date_str_to_generalize_time(date_str)
```
Converts date in string format to date in generalized time format.

Args:
    date_str (str): Date string in formats %Y-%m-%d, %Y/%m/%d or %d.%m.%Y

Returns:
    (str): Date in generalized time format.

Note:
    Time zone information is not supported.

<h3 id="pyncli.ldap.utill.is_generalized_time">is_generalized_time</h3>

```python
is_generalized_time(date_str)
```
Checks is this string look like generalized time.

Args:
    date_str (str): Date string

Returns:
    (bool): True if input string is generalized time.

Note:
    Time zone information is not supported.

<h3 id="pyncli.ldap.utill.generalized_time_to_datetime">generalized_time_to_datetime</h3>

```python
generalized_time_to_datetime(gen_time)
```
Converts date in generalized time format to datetime

Args:
    gen_time (str): Date string in generalized time format

Returns:
    (datetime): datetime object

Note:
    Time zone information is not supported.

<h3 id="pyncli.ldap.utill.datetime_to_generalized_time">datetime_to_generalized_time</h3>

```python
datetime_to_generalized_time(date_time)
```
Converts datetime to generalized time format.

Args:
    date_time (datetime): datetime object

Returns:
    (str): Date in generalized time format.

Note:
    Time zone information is not supported.

