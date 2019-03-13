# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        protouser
# Purpose:     To implement base protouser class.
#
# Author:      Evgeniy Semenov
#
# Created:     06.02.2017
# Copyright:   (c) Evgeniy Semenov 2017-2019
# Licence:     MIT
#-------------------------------------------------------------------------------

import sys

from .admexept import NotEnoughParams, EmptyParam, WrongParam, TooLong

class protouser(object):
    """
        Base user class
    """
    _FIELD_MAP={
                #u'uid':u'uid',
                'login':'sAMAccountName',
    }

    #Ключи берём по классу, ограничения из ЛДАП
    _LDAP_LIMITS = {
                #u'uid':{u'min':0,u'max':255,u'fail_min':True,u'fail_max':True},
                'login':{'min':1,'max':64,'fail_min':True,'fail_max':True}, # login==CN
    }
    _DEFAULT_SORT_ORDER=['login']

    @classmethod
    def check_length(cls,field_name, field_value):
        """A class method that checks and adjusts a long transmitted setting.

        Args:
            field_name (str): attribute name.
            field_value (str): attribute value.

        Returns:
            (str): attribute value.
        """
        if field_name in list(cls._LDAP_LIMITS.keys()):
            if len(field_value) < cls._LDAP_LIMITS[field_name]['min'] and  cls._LDAP_LIMITS[field_name]['fail_min']:
                raise EmptyParam('{field} must not be blank.'.format(field=field_name))
            elif len(field_value) > cls._LDAP_LIMITS[field_name]['max'] and  cls._LDAP_LIMITS[field_name]['fail_max']:
                raise TooLong('{field} too long.'.format(field=field_name))
            else:
                return field_value[:cls._LDAP_LIMITS[field_name]['max']]
        else:
            return field_value

    def __init__(self,login,**kwargs): #uid,
        """constructor

            Args:
                login (str): user name

            Raises:
                WrongParam: The Organisational Unit parameter is not of the correct
                type.
        """
        if isinstance(login, str):
            self.login=protouser.check_length('login',login)
        else:
            try:
                self.login=str(login,'utf-8')
            except:
                raise WrongParam('Unicode string expected (login), conversion fails.')
            self.login=protouser.check_length('login',self.login)


    def __getitem__(self,name):
        if name in self.__dict__:
            return self.__dict__[name]
        else:
            return False
            # may be raise EmptyParam('Value %s not found!' % name)
    def __eq__(self, instance):
        if type(instance) is not self.__class__:
            raise WrongParam("%s is not %s instance!" % (instance, self.__class__.__name__))
        for (key, value) in list(self.__dict__.items()):
            if self.__getitem__(key)!=instance.__getitem__(key):
                return False
        return True

    def __ne__(self,instance):
        return not self.__eq__(instance)

    def diff(self, instance):
        """Get instances difference

            The method returns a dictionary with attributes and their values
            that do not match in two instances of the class (self and passed
            to the instance parameter)

            Args:
                instance (:obj: 'protouser' or inheritor ): instance for
                    comparison

            Returns:
                (dict): dictionary with attributes and their values
                    that do not match in two instances of the class

        """
        if type(instance) is not self.__class__:
            raise WrongParam("%s is not %s instance!" % (instance, self.__class__.__name__))
        ret = {}
        if self == instance:
            return ret
        else:
            for (key, value) in list(self.__dict__.items()):
                if self.__getitem__(key)!=instance.__getitem__(key):
                    ret[key]=instance.__getitem__(key)
            return ret

    def diff_ldap_attrs(self, instance):
        """Get instances difference (in ldap attributes)

            the method returns a dictionary with ldap attributes and their
            values that do not match in two instances of the class (self and
            passed to the instance parameter)

            Args:
                instance (:obj: 'protouser' or inheritor ): instance for
                    comparison

            Returns:
                (dict): dictionary with ldap attributes and their values
                    that do not match in two instances of the class
        """
        if type(instance) is not self.__class__:
            raise WrongParam("%s is not %s instance!" % (instance, self.__class__.__name__))
        ret = {}
        if self == instance:
            return ret
        else:
            for (key, value) in list(self.__dict__.items()):
                if self.__getitem__(key)!=instance.__getitem__(key):
                    if key in list(self._FIELD_MAP.keys()):
                        ret[self._FIELD_MAP[key]]=instance.__getitem__(key)
            return ret

    def diff_ldap_attrs_by_categories(self, instance):
        """Get instances difference (in ldap attributes with categories)

            the method returns a dictionary with ldap attributes and their
            values that do not match in two instances of the class (self and
            passed to the instance parameter). For the "modify" method from the
            library ldap 3.

            Args:
                instance (:obj: 'protouser' or inheritor ): instance for
                    comparison

            Returns:
                (dict): dictionary with ldap attributes and their values
                    that do not match in two instances of the class
            Raises:
                WrongParam: The instance parameter is not of the correct
                type.

            Note:
                Does not detect container shifts.
        """
        if type(instance) is not self.__class__:
            raise WrongParam("%s is not %s instance!" % (instance, self.__class__.__name__))
        if self.login!=instance.login:
            raise WrongParam("Wrong method call! Logins must be equal (%s!=%s). \
                To rename RDN use special method." % (self.login, instance.login))
        ret = {}
        if self == instance:
            return ret
        else:
            for (key, value) in list(self.diff(instance).items()):
                if self.__getitem__(key)!=instance.__getitem__(key):
                    if key in list(self._FIELD_MAP.keys()):
                        VL=[]
                        if self.__getitem__(key)=='':
                            OP='MODIFY_ADD'
                            VL.append(instance.__getitem__(key))
                        elif instance.__getitem__(key)=='':
                            OP='MODIFY_DELETE'
                        else:
                            OP='MODIFY_REPLACE'
                            VL.append(instance.__getitem__(key))
                        ret[self._FIELD_MAP[key]]=[(OP,VL)]
            return ret

    def get_ldap_attrs(self):
        """Get ldap attributes

            Returns:
                (dict): LDAP attributes dictionary of instance.
        """
        attrs={}
        for atr in list(self._FIELD_MAP.keys()):
            attrs[self._FIELD_MAP[atr]]=self.__getitem__(atr)
        return attrs

    def get_ldap_attr(self, ldap_attr):
        """Get instance attribute name by its ldap attribute name

            Args:
                ldap_attr (str): Ldap attibute name.

            Returns:
                (str): attribute name.
        """
        attr=[ atr for atr, ld_atr in list(self._FIELD_MAP.items()) if ld_atr == ldap_attr][0]
        return attr

    def get_ldap_val(self, ldap_attr):
        """Get instance attribute value by its ldap attribute name

            Args:
                ldap_attr (str): Ldap attibute name.

            Returns:
                attribute value.
        """
        attr=self.get_ldap_attr(ldap_attr)
        return getattr(self,attr)

    def show_diff(self,instance, field_order=[], by_ldap_attf=False, print_out=False, only_diff=False, diff_all_field=True):
        """Display information on differences in instances.

            Args:
                instance (:obj: 'protouser' or inheritor ): instance for
                    comparison
                field_order (list): A list with the instance attribute names to
                    display in the specified order. (default: self._DEFAULT_SORT_ORDER)
                by_ldap_attf (bool): Print differences by ldap attributes or by
                    instance attributes.
                print_out (bool): Print on the console.
                only_diff (bool): Display only distinguished attributes.
                diff_all_field (bool): Display different attributes even
                    forbidden to be displayed in descendants.

            Returns:
                (list): List of formated strings with difference in instances.
        """
        if type(instance) is not self.__class__:
            raise WrongParam("%s is not %s instance!" % (instance, self.__class__.__name__))
        if field_order==[] and by_ldap_attf==False:
            field_order=self._DEFAULT_SORT_ORDER
        elif field_order==[] and by_ldap_attf==True:
            for dso in self._DEFAULT_SORT_ORDER:
                field_order.append(self._FIELD_MAP[dso])
        ret=[]
        if by_ldap_attf:
            max_descr_len=len(max( list(self._FIELD_MAP.values()), key=len))
            if only_diff:
                if diff_all_field:
                    # в df значения из instance
                    # т.к. во всех потомках diff_ldap_attrs перегружен вызываем метод класса protouser чтобы засечь все изменения для отображения
                    # тут явный вязов метода из класса protouser с явной передачей ему экземпляра.
                    df=protouser.diff_ldap_attrs(self,instance)
                else:
                    df=self.diff_ldap_attrs(instance)
            else:
                df=instance.get_ldap_attrs()
            if len(df)>0:
                out_line='='*80
                if print_out:
                    print( out_line)
                else:
                    ret.append(out_line)

                out_line= "Changes for: {short}".format(short=self.brief)
                if print_out:
                    print( out_line)
                else:
                    ret.append(out_line)

                for sortedKey in field_order:
                    if sortedKey in list(df.keys()):
                        itm_k=sortedKey
                        itm_v=df[sortedKey]
                        if self.get_ldap_val(itm_k) != itm_v:
                            from_sign='<'
                            to_sign='>'
                        else:
                            from_sign=' '
                            to_sign=' '

                        out_line= "{item_name:<{width}}:{mark}{orig}".format(item_name=itm_k,
                                                            orig=self.get_ldap_val(itm_k),
                                                            width=max_descr_len,
                                                            mark=from_sign)
                        if print_out:
                            print( out_line)
                        else:
                            ret.append(out_line)

                        out_line= "{item_name:<{width}}:{mark}{orig}".format(item_name='',
                                                            orig=itm_v,
                                                            width=max_descr_len,
                                                            mark=to_sign)
                        if print_out:
                            print( out_line)
                        else:
                            ret.append(out_line)
        else:
            max_descr_len=len(max( list(self._FIELD_MAP.keys()), key=len))
            if only_diff:
                df=self.diff(instance)
            else:
                df={key:value for (key, value) in list(instance.__dict__.items())}

            if len(df)>0:
                out_line= '='*80
                if print_out:
                    print( out_line)
                else:
                    ret.append(out_line)
                out_line= "Changes for: {short}".format(short=self.brief)
                if print_out:
                    print( out_line)
                else:
                    ret.append(out_line)

                for sortedKey in field_order:
                    if sortedKey in list(df.keys()):
                        itm_k=sortedKey
                        itm_v=df[sortedKey]
                        if getattr( self, itm_k) != itm_v:
                            from_sign='<'
                            to_sign='>'
                        else:
                            from_sign=' '
                            to_sign=' '
                        out_line= "{item_name:<{width}}:{mark}{orig}".format(item_name=itm_k,
                                                            orig=getattr( self,itm_k),
                                                            width=max_descr_len,
                                                            mark=from_sign)
                        if print_out:
                            print( out_line)
                        else:
                            ret.append(out_line)
                        out_line= "{item_name:<{width}}:{mark}{orig}".format(item_name='',
                                                            orig=itm_v,
                                                            width=max_descr_len,
                                                            mark=to_sign)
                        if print_out:
                            print( out_line)
                        else:
                            ret.append(out_line)
        if not print_out:
            return ret

    def show(self, field_order=[], by_ldap_attf=False, print_out=False):
        """Display information instances.

            Args:
                field_order (list): A list with the instance attribute names to
                    display in the specified order. (default: self._DEFAULT_SORT_ORDER)
                by_ldap_attf (bool): Print by ldap attributes or by
                    instance attributes.
                print_out (bool): Print on the console.

            Returns:
                (list): List of formated strings with instance information.
        """
        if field_order==[] and by_ldap_attf==False:
            field_order=self._DEFAULT_SORT_ORDER
        elif field_order==[] and by_ldap_attf==True:
            for dso in self._DEFAULT_SORT_ORDER:
                field_order.append(self._FIELD_MAP[dso])
        ret=[]
        if by_ldap_attf:
            max_descr_len=len(max( list(self._FIELD_MAP.values()), key=len))
            df={self._FIELD_MAP[key]:getattr(self,key) for key in list(self._FIELD_MAP.keys())}
            if len(df)>0:
                out_line='='*80
                if print_out:
                    print( out_line)
                else:
                    ret.append(out_line)

                out_line= "Instance: {short}".format(short=self.brief)
                if print_out:
                    print( out_line)
                else:
                    ret.append(out_line)

                for sortedKey in field_order:
                    if sortedKey in list(df.keys()):
                        itm_k=sortedKey
                        itm_v=df[sortedKey]
                        if self.get_ldap_val(itm_k) != itm_v:
                            from_sign='<'
                            to_sign='>'
                        else:
                            from_sign=' '
                            to_sign=' '

                        out_line= "{item_name:<{width}}:{mark}{orig}".format(item_name=itm_k,
                                                            orig=self.get_ldap_val(itm_k),
                                                            width=max_descr_len,
                                                            mark=from_sign)
                        if print_out:
                            print( out_line)
                        else:
                            ret.append(out_line)

        else:
            max_descr_len=len(max( list(self._FIELD_MAP.keys()), key=len))

            df={key:value for (key, value) in list(self.__dict__.items())}

            if len(df)>0:
                out_line= '='*80
                if print_out:
                    print( out_line)
                else:
                    ret.append(out_line)
                out_line= "Instance: {short}".format(short=self.brief)
                if print_out:
                    print( out_line)
                else:
                    ret.append(out_line)

                for sortedKey in field_order:
                    if sortedKey in list(df.keys()):
                        itm_k=sortedKey
                        itm_v=df[sortedKey]
                        if getattr( self, itm_k) != itm_v:
                            from_sign='<'
                            to_sign='>'
                        else:
                            from_sign=' '
                            to_sign=' '
                        out_line= "{item_name:<{width}}:{mark}{orig}".format(item_name=itm_k,
                                                            orig=getattr( self,itm_k),
                                                            width=max_descr_len,
                                                            mark=from_sign)
                        if print_out:
                            print( out_line)
                        else:
                            ret.append(out_line)
        if not print_out:
            return ret

    @property
    def brief(self):
        """Gets brief user information.

        Returns:
            (str): brief user information
        """
        return "login :{login}".format(login=self.login)

    @classmethod
    def get_sql_create_table(cls,table_name):
        """A class method that creates a database table definition suitable for
        uploading instances of a given class.

        Args:
            table_name (str): SQL database table name.

        Note:
            Suitable for SQLite.
        """
        crr="CREATE TABLE \'{table}\'(".format(table=table_name)
        names=getattr(cls,'_LDAP_LIMITS')
        count=len(names)
        i=1
        for itm in list(names.keys()):
            if i==count:
                if itm=='login':
                    crr+=" \'{field}\' TEXT PRIMARY KEY".format(field=itm)
                else:
                    crr+=" \'{field}\' TEXT".format(field=itm)

            else:
                if itm=='login':
                    crr+=" \'{field}\' TEXT PRIMARY KEY,".format(field=itm)
                else:
                    crr+=" \'{field}\' TEXT,".format(field=itm)
            i+=1
        crr+=");"
        return crr

    def get_sql_insert(self, table_name):
        """A method that creates an instruction to insert a row into a database,
        suitable for loading instances of a given class.

        Args:
            table_name (str): SQL database table name.

        Note:
            Suitable for SQLite.
        """
        ins="INSERT INTO \'{table}\'(".format(table=table_name)
        vals=" VALUES ("
        count=len(self._LDAP_LIMITS)
        i=1
        for itm in list(self._LDAP_LIMITS.keys()):
            if i==count:
                ins+="\'{itm}\' ".format(itm=itm)
                vals+="\'{val}\' ".format(val=getattr( self, itm ))
            else:
                ins+="\'{itm}\', ".format(itm=itm)
                vals+="\'{val}\', ".format(val=getattr( self, itm ))
            i+=1
        ins+=") "
        vals+=");"
        return ins+vals

    def __unicode__(self):
        out='class {0} instance:\n'.format(self.__class__.__name__)
        for (key, value) in list(self.__dict__.items()):
            out+='{key}: {value}\n'.format(key=key,value=value)
        return out

    def __str__(self):
        out=u'class {0} instance:\n'.format(self.__class__.__name__)
        for (key, value) in list(self.__dict__.items()):
            out+=u'{key}: {value}\n'.format(key=key,value=value)

        return out
