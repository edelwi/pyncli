# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
# Name:        exceptions
# Purpose:
#
# Author:      Evgeniy Semenov
#
# Created:     21.05.2018
# Copyright:   (c) Evgeniy Semenov 2018-2019
# Licence:     MIT
#-------------------------------------------------------------------------------

class AdminException(Exception):
    """Root package exception class.

    Args:
        value (str): Description of the exception.

    Attributes:
        value (str): Description of the exception.
    """

    def __init__(self, value):
        self.value = value


class OperationFailure(AdminException):
    """ Exception class called when it is impossible to perform the specified
    operation.

    Args:
        value (str): Description of the exception.

    Attributes:
        value (str): Description of the exception.
    """