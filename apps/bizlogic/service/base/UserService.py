# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/11 15:01'

from apps.bizlogic.models import Piuser
from apps.bizlogic.models import Piuserrole

from django.db.utils import DatabaseError
from django.db.transaction import TransactionManagementError
from django.db import connection
from django.core.paginator import Paginator

from utilities.publiclibrary.StringHelper import StringHelper
from utilities.message.StatusCode import StatusCode
from utilities.message.FrameworkMessage import FrameworkMessage
from utilities.publiclibrary.DbCommonLibaray import DbCommonLibaray

from apps.bizlogic.service.base.OrganizeService import OrganizeService

class UserSerivce(object):
    """
    用户服务
    """

    def __init__(self):
        object.__init__()

    def Exists(self, fieldNames, fieldValue):
        """
        用户名是否重复
        Args:
            fieldNames (string): 字段名
            fieldValue (string): 字段值
        Returns:
            returnValue(bool): 已存在
        """
        try:
            Piuser.objects.get(**{fieldNames: fieldValue})
            return True
        except Piuser.DoesNotExist:
            return False

    def AddUser(self, userEntity):
        """
        添加用户
        Args:
            userEntity (Piuser): 用户实体
        Returns:
            returnValue: 用户主键
        """
        try:
            userEntity.save()
            returnCode = StatusCode.statusCodeDic['OKAdd']
            returnMessage = FrameworkMessage.MSG0009
            returnValue = userEntity.id
            return returnCode, returnMessage, returnValue
        except DatabaseError as e:
            print(e)
            returnCode = StatusCode.statusCodeDic['DbError']
            returnMessage = FrameworkMessage.MSG0001
            returnValue = None
            return returnCode, returnMessage, returnValue
        except TransactionManagementError as e:
            print(e)
            returnCode = StatusCode.statusCodeDic['DbError']
            returnMessage = FrameworkMessage.MSG0001
            returnValue = None
            return returnCode, returnMessage, returnValue

    def GetEntity(id):
        """
        获取用户实体
        Args:
            id (string): 用户主键
        Returns:
            returnValue (Piuser or None): 用户实体
        """
        try:
            user = Piuser.objects.get(id=id)
            return user
        except Piuser.DoesNotExist:
            return None


    def GetEntityByUserName(self, userName):
        """
        根据用户名获取用户实体
        Args:
            userName (string): 用户名称
        Returns:
            returnValue (Piuser or None): 用户实体
        """
        try:
            user = Piuser.objects.get(username=userName)
            return user
        except Piuser.DoesNotExist:
            return None


    def GetDT(self):
        """
        获取用户列表
        Args:
        Returns:
            returnValue (List): 用户列表
        """
        returnValue = []
        try:
            for user in Piuser.objects.all():
                returnValue.append(user)
            return returnValue
        except DatabaseError as e:
            return returnValue
        except TransactionManagementError as e:
            return returnValue


    def GetDTByPage(self, searchValue, departmentId, roleId, pageSize=50, order=None):
        """
        分页查询
        Args:
            searchValue (string): 查询字段
            departmentId (string): 部门主键
            roleId (string): 角色主键
            pageSize (int): 每页显示
            order (string): 排序
        Returns:
            returnValue (List): 用户分页列表
        """
        countSqlQuery =' SELECT * FROM ' +  Piuser._meta.db_table + ' WHERE '

        whereConditional = Piuser._meta.db_table + '.DELETEMARK' + ' = 0 ' \
            + " AND " + Piuser._meta.db_table + '.ENABLED' + ' = 1 ' \
            + " AND " + Piuser._meta.db_table + '.ISVISIBLE' + ' = 1 '

        if departmentId:
            organizeIds = OrganizeService.GetChildrensById(self, departmentId)
            if len(organizeIds) != 0:
                whereConditional = whereConditional + " AND (" +  Piuser._meta.db_table + '.COMPANYID IN (' + StringHelper.ArrayToList(self,organizeIds,"\'") + ')' \
                    + " OR " + Piuser._meta.db_table + '.SUBCOMPANYID IN (' + StringHelper.ArrayToList(self,organizeIds,"\'") + ')' \
                    + " OR " + Piuser._meta.db_table + '.DEPARTMENTID IN (' + StringHelper.ArrayToList(self,organizeIds,"\'") + ')' \
                    + " OR " + Piuser._meta.db_table + '.SUBDEPARTMENTID IN (' + StringHelper.ArrayToList(self,organizeIds,"\'") + ')' \
                    + " OR " + Piuser._meta.db_table + '.WORKGROUPID IN (' + StringHelper.ArrayToList(self,organizeIds,"\'") + '))'

        # if roleId:
        #     whereConditional = whereConditional + ' AND ( ' + Piuser._meta.db_table + '.ID IN' \
        #         + '    (SELECT USERID FROM ' + Piuserrole._meta.db_table \
        #         + '     WHERE ROLEID = \'' + roleId + '\'' \
        #         + '     AND ENABLED = 1' \
        #         + '     AND DELETEMARK = 0 ))'

        if searchValue:
            whereConditional = whereConditional + " AND (" + searchValue + ')'

        countSqlQuery = countSqlQuery + ' ' + whereConditional

        #print(countSqlQuery)

        userList = DbCommonLibaray.executeQuery(self, countSqlQuery)


        #print(len(userList))
        returnValue = Paginator(userList, pageSize)
        return returnValue

    def GetList(self):
        pass

    def GetDTByIds(self, ids):
        pass

    def GetListByIds(self, ids):
        pass

    def UpdateUser(self, userEntity, statusCode, statusMessage):
        pass

    def Search(self, searchValue, auditStatus, roleIds):
        pass

    def SetUserAuditStates(self, ids, auditStates):
        pass

    def Delete(self, id):
        pass

    def BatchDelete(self, ids):
        pass

    def SetDeleted(self, ids):
        pass

    def BatchSave(self, dataTable):
        pass

    def GetCompanyUser(self):
        pass

    def GetDepartmentUser(self):
        pass

    def GetDepartmentUser(self, departmentId, containChildren):
        pass

    def GetListByDepartment(self, departmentId, containChildren):
        pass