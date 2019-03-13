# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
# Name:        exceptions
# Purpose:
#
# Author:      Evgeniy Semenov
#
# Created:     21.05.2018
# Copyright:   (c) Evgeniy Semenov 2018
# Licence:     MIT
#-------------------------------------------------------------------------------

class AdminException(Exception):
    """ Корневой класс исключений для работы пакета.

    Args:
        value (str): Человекочитаемое строковое описание исключения.

    Attributes:
        value (str): Человекочитаемое строковое описание исключения.
    """

    def __init__(self, value):
        self.value = value
##    def __str__(self):
##        #return self.value
##        return unicode(self.value).encode('utf-8')

class OperationFailure(AdminException):
    """ Класс исключения вызываемый в случае невозможности выполнения
    указанной операции.

    Args:
        value (str): Человекочитаемое строковое описание исключения.

    Attributes:
        value (str): Человекочитаемое строковое описание исключения.
    """