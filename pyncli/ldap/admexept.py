# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        admexept
# Purpose:
#
# Author:      Evgeniy Semenov
#
# Created:     14.03.2017
# Copyright:   (c) Evgeniy Semenov 2017
# Licence:     MIT
# -------------------------------------------------------------------------------


class AdminException(Exception):
    """ Root package exception class.

    Args:
        value (str): Description of the exception.

    """

    def __init__(self, value, code=None ):
        self.value = value

    def __str__(self):
        return self.value


class NotEnoughParams(AdminException):
    """ Exception class called in case of lack of necessary parameters in the
    constructor or method call.

    Args:
        value (str): Description of the exception.

    """


class EmptyParam(AdminException):
    """ Exception class called when a method is called with an empty parameter.

    Args:
        value (str): Description of the exception.

    """


class WrongParam(AdminException):
    """ The exception class that is called when the method is called as a
    parameter of an invalid type or value.

    Args:
        value (str): Description of the exception.

    """


class TooLong(AdminException):
    """ Exception class called when the method is called with an invalid length
    parameter.

    Args:
        value (str): Description of the exception.

    """


class ConnectionFailure(AdminException):
    """ Exception class called when it is impossible to connect to the specified
    server.

    Args:
        value (str): Description of the exception.

    """


class OperationFailure(AdminException):
    """ Exception class called when it is impossible to perform the specified
    operation.

    Args:
        value (str): Description of the exception.

    """


class NotFound(AdminException):
    """ Exception class called in case of problems with the search.

    Called when the desired object was not found.

    Args:
        value (str): Description of the exception.

    """


##def main():
##    import sys
##    import inspect
##    print( [x[0] for x in inspect.getmembers(sys.modules[__name__], inspect.isclass) ])
##
##if __name__ == '__main__':
##    main()
