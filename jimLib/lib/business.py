# -*- coding: utf-8 -*-
#!/usr/bin/env python
from jimLib.lib.util import lib_post
import urllib
from jimLib.lib.util import Dict
from jimLib.lib.util import lib_log

class business():
    def __init__(self):
        pass

    #登录
    def login(self,user_name='',passwd=''):
        if ''==user_name or '' == passwd:
            return ('',False,0)

        method = 'Admin.login'
        content = {'admin_name':urllib.quote(user_name.encode('utf-8')),'passwd':urllib.quote(passwd.encode('utf-8'))}
        result  = lib_post(method, content)
        if 500 == result['status_code']:
            return (result['content'],False,0)
        if 200 == result['status_code'] and 0 == result['content']['is_success']:
            admin_id = result['content']['id']
            return (u'成功登录',True,admin_id)

        return (u'用户名或者密码错误!',False,0)

    #查询属于当前用户的bug
    '''
    return status,is_success,message
           500,,参数错误
           200,0,严重错误
           200,1,一般错误
           200,-1,没有错误
           其他查询失败
    '''
    def get_my_bug(self,admin_id=0):
        if 0 == admin_id:
            return (500,None,u'参数不正确')

        method = 'Bug.get_self_bug'
        content = {'admin_id':urllib.quote(admin_id.encode('utf-8'))}
        result = lib_post(method, content)
        if 500 == result['status_code']:
            return (500,None,result['content'])
        elif 200 == result['status_code'] and 0 == result['content']['is_success']:
            return (200,0,u'严重错误')
        elif 200 == result['status_code'] and 1 == result['content']['is_success']:
            return (200,1,u'一般错误')
        elif 200 == result['status_code'] and -1 == result['content']['is_success']:
            return (200,-1,u'没有错误')
        else:
            return (200,None,u'查询失败')

        pass

    #接受消息
    def receive_message(self,messge=''):
        pass

    #查询项目

    #查询bug

    #查询资源
    def get_resource_name(self):
        method = 'Resource.get_list'
        content = {}
        re_list = []

        result = lib_post(method,content)
        if 500 == result['status_code']:
            return (False,result['content'])
        if 200 == result['status_code']:
            if 0< int(str(result['content']['record_count'])):
                rows = int(str(result['content']['record_count']))
                for i in range(0,rows-1):
                    re_list.append(result['content']['list'][i]['source_name'])
            return (True,re_list)
        return (False,'')
        pass
    def get_resource_id_name_map(self):
        pass

    #查询

    #新增

    #修改

    #删除

    #获取编号
    '''
    通过获取当前要求模块的最大的id，在此基础上加一已返回
    '''
    def get_number(self,module_index=0):
        cur_prefix = Dict.prefix_list[module_index]
        number = ''
        max_num = 1

        method = '%s.get_list'%Dict.module_list[module_index]
        content={'page_size':1}
        result = lib_post(method,content)
        if 500 == result['status_code']:
            lib_log(0,result['content'])
            return 'error'
        if 200 == result['status_code']:
            if 0 <> result['content']['record_count']:
                max_num = int(result['content']['list'][0]['id'])
                max_num += 1

        number = '%06d'%max_num
        return '%s%s'%(cur_prefix,number)

    #获取字典
    def get_dict(self):
        method = 'Map.get_map'
        content = {}
        result = lib_post(method,content)
        if 500 == result['status_code']:
            return (False,'参数错误')
        elif 200 == result['status_code']:
            return (True,result['content'])

        return (False,'其他错误')