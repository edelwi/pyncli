# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        utill
# Purpose:     some functions
#
# Author:      Evgeniy Semenov
#
# Created:     14.03.2017
# Copyright:   (c) Evgeniy Semenov 2017-2019
# Licence:     MIT
# -------------------------------------------------------------------------------
"""Module with auxiliary functions.
"""
import requests
from pyncli.ldap import admexept
import string
import re

# import urllib2
import socket
import requests
from base64 import b64encode
import datetime

EMAIL_PATTERN = re.compile(
    r"^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$", re.IGNORECASE
)
DATE_STR_PATTERN = re.compile(
    r"^(?P<year>\d{4})[-/](?P<month>\d{2})[-/](?P<day>\d{2})$", re.IGNORECASE
)
DATE_STR_PATTERN2 = re.compile(
    r"^(?P<day>\d{1,2})\.(?P<month>\d{1,2})\.(?P<year>\d{4})$", re.IGNORECASE
)

GENERALIZED_TIME_PATTERN = re.compile(
    r"^(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})(?P<hour>\d{2})(?P<minute>\d{2})(?P<second>\d{2}).0Z$",
    re.IGNORECASE,
)


def download_file(url, local_path, user, pwd):
    """Download file

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
    """
    local_filename = local_path  # os.path.join(local_path,local_filename)
    r = requests.get(url, auth=(user, pwd), stream=True)
    if r.status_code != 200:
        raise admexept.ConnectionFailure(
            "File Download Error, status code: %s" % r.status_code
        )
    with open(local_filename, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
    return local_filename


def upload_file(url, data, login, pwd):
    """Upload file

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
    """
    pair = "{user}:{pwd}".format(user=login, pwd=pwd)
    userAndPass = b64encode(pair).decode("ascii")
    headers = {
        "Content-type": "text/xml",
        "Authorization": "Basic %s" % userAndPass,
    }

    r = requests.post(url, data=data, headers=headers)
    if r.status_code != 200:
        raise admexept.OperationFailure(
            "The server cannot complete the request. Code: %s <%s>"
            % (r.status_code, r.text)
        )


def mailto(msg_from, msg_to_list, smpt, subject, text):
    """Simple mailto function

        Sends a message to one or a group of recipients.

        Args:
            msg_from (str): From whom
            msg_to_list (list): List of email recipients.
            smpt (str): SMTP server name or IP
            subject (str): subject of the message
            text (str): text of the message

        Raises:
            ConnectionFailure: connection failure
    """
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    COMMASPACE = ", "
    part = MIMEText(text, "plain", "utf-8")
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = msg_from
    msg["To"] = COMMASPACE.join(msg_to_list)
    msg.attach(part)
    try:
        s = smtplib.SMTP(smpt)
    except socket.gaierror:
        raise admexept.ConnectionFailure("SMTP server is unavailable.")
    s.sendmail(msg_from, [COMMASPACE.join(msg_to_list)], msg.as_string())
    s.quit()


##def emailWalidator(email_str):
##    """
##    """
##    if email_str=='':
##        return ''
##    else:
##        email=email_str.lower()
##        email=email.strip()
##        email=email.replace(","," ")
##        emails=email.split()
##        newemaillist=[]
##        for mail in emails:
##            if len(mail)>=7:
##                rez=EMAIL_PATTERN.findall(mail)
##                if len(rez)>0:
##                    newemaillist.append(rez[0])
##        if len(newemaillist)>0:
##            return newemaillist[0]
##        else:
##            return ''


def trim(text):
    """Removes extra spaces from text.

        Args:
            text (str): text

        Returns:
            (str): processed text
    """
    return " ".join(string.split(string.strip(text)))


def trim_low(text):
    """Removes extra spaces from text and set it to lower case.

        Args:
            text (str): text

        Returns:
            (str): processed text
    """
    return string.lower(trim(text))


def split_names(fullname):
    """Splits user fullname by surname, first name and middle name.

        Args:
            fullname (str): full name (The first word is considered the surname,
                the second first name, all the rest go to the middle name. This
                is the Russian name record format.)

        Returns:
            (dict): Dictionary with surname, first name and middle name as
                values.
    """
    fullname = trim(fullname)
    names = string.split(fullname, sep=" ")
    rez = {"surname": "", "first_name": "", "middle_name": ""}
    try:
        rez["surname"] = names[0]
    except IndexError:
        pass

    try:
        rez["first_name"] = names[1]
    except IndexError:
        pass

    if len(names) >= 3:
        mn = " ".join(names[2:])
        rez["middle_name"] = mn
    return rez


def sqllite_quote_ap(strvalue):
    if isinstance(strvalue, str):
        return strvalue.replace("'", "''")
    else:
        return strvalue


def check(pattern, check_str):
    match = re.search(pattern, check_str)
    if match:
        return match


def date_str_to_generalize_time(date_str):
    """Converts date in string format to date in generalized time format.

        Args:
            date_str (str): Date string in formats %Y-%m-%d, %Y/%m/%d or %d.%m.%Y

        Returns:
            (str): Date in generalized time format.

        Note:
            Time zone information is not supported.
    """
    if isinstance(date_str, str):
        if len(date_str) == 0:
            return ""
        if is_generalized_time(date_str):
            return date_str

        for ptr in (DATE_STR_PATTERN, DATE_STR_PATTERN2):
            date_time = check(ptr, date_str)
            if date_time:
                date_time = {
                    k: int(v) for k, v in (date_time.groupdict()).items()
                }
                try:
                    py_time = datetime.datetime(**date_time)
                except:
                    raise admexept.WrongParam(
                        "Invalid date format ({date}).".format(date=date_str)
                    )
                return "{year}{month:02d}{day:02d}000000.0Z".format(
                    year=py_time.year, month=py_time.month, day=py_time.day
                )

        else:  # its for-else
            raise admexept.WrongParam(
                "Invalid date format ({date}).".format(date=date_str)
            )
    else:
        raise admexept.WrongParam(
            "Invalid date format ({date}).".format(date=date_str)
        )


def is_generalized_time(date_str):
    """Checks is this string look like generalized time.

        Args:
            date_str (str): Date string

        Returns:
            (bool): True if input string is generalized time.

        Note:
            Time zone information is not supported.
    """
    if isinstance(date_str, str) or isinstance(date_str, str):
        if len(date_str) == 0:
            return True
        date_time = re.search(GENERALIZED_TIME_PATTERN, date_str)
        if date_time:
            date_time = {k: int(v) for k, v in date_time.groupdict().items()}
            try:
                py_time = datetime.datetime(**date_time)
            except:
                return False
            return True
    else:
        return False


def generalized_time_to_datetime(gen_time):
    """Converts date in generalized time format to datetime

        Args:
            gen_time (str): Date string in generalized time format

        Returns:
            (datetime): datetime object

        Note:
            Time zone information is not supported.
    """
    if is_generalized_time(gen_time):
        if len(gen_time) > 0:
            date_time = re.search(GENERALIZED_TIME_PATTERN, gen_time)
            date_time = {k: int(v) for k, v in date_time.groupdict().items()}
            return datetime.datetime(**date_time)
        else:
            raise admexept.EmptyParam("Value not set.")
    else:
        raise admexept.WrongParam("Wrong Generalize Time format")


def datetime_to_generalized_time(date_time):
    """Converts datetime to generalized time format.

        Args:
            date_time (datetime): datetime object

        Returns:
            (str): Date in generalized time format.

        Note:
            Time zone information is not supported.
    """
    if isinstance(date_time, datetime.datetime):
        return date_time.strftime("%Y%m%d%H%M%S.0Z")
    else:
        raise admexept.WrongParam("Invalid DateTime variable.")
