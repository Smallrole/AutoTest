# coding=utf-8
import sys,json,re
from robot.api import logger
reload(sys)
sys.setdefaultencoding("utf-8")   # 把 str 编码由 ascii 改为 utf8


class JsonDataHandle(object):
    # 处理长度类型  返回 状态 信息1 信息2
    def __JsonLen(self, DataA, DataB):
        logger.debug('调用JsonLen函数 开始判断长度，响应返回数据:%s  预期数据:%s' % (DataA, DataB))
        if 'len' not in DataB or len(DataB.keys()) >1:
            return '0', 'Expectation and return are not equal! Please check!' + ''  # 失败
        for k, v in DataB.items():
            ReverseLen = len(str(DataA))       # 返回数据的长度
            RefrenceLen = int(DataB[k])        # 参考数据的长度
            logger.debug('实返回数据长度：%s  预期数据长度：%s' % (ReverseLen, RefrenceLen))
            if ReverseLen != RefrenceLen:
                logger.debug('实返回数据长度：%s  预期数据长度：%s' % (ReverseLen, RefrenceLen))
                return '0', 'The length is not equal! RealLen:' + str(ReverseLen) + '  ExpectLen:'+ str(RefrenceLen)  # 失败
            return '1', None                   # 成功


    # 处理列表-列表类型数据 返回参数a 参考参数 b 日志  返回状态1或0 信息1 信息2
    def __JsonList(self, Real_data,  Expect_data):
        try:
            logger.debug('调用JsonList函数 实响应数据: %s 预期数据:%s' % (Real_data, Expect_data))
            if len(Real_data) < len(Expect_data):
                return '0', 'List Values are not equal! ' + 'Real_data: ' + str(Real_data) + '  Expect_data: ' + str(Expect_data)
            for single_Real_data in Real_data:
                single_Real_data_index = Real_data.index(single_Real_data)
                if single_Real_data_index > len(Expect_data) -1:
                    return '0', str(single_Real_data) + ' in Expect_data not found!'
                single_Expect_data = Expect_data[single_Real_data_index]  # 期望返回的数据
                logger.debug('实响应数据 %s' % single_Real_data)
                logger.debug('预期数据 %s' % single_Expect_data)
                if single_Expect_data != single_Real_data:       # 如果列表的中字典不相同,则判断具体那里不同
                    if isinstance(single_Expect_data, dict) and isinstance(single_Real_data, dict):   # 字典类型
                        State, Info= self.__JsonDict(single_Real_data, single_Expect_data)
                        if State == '0':
                            logger.info('数据匹配失败.详情：%s' %Info)
                            return State, Info
                        continue
                    elif isinstance(single_Expect_data, list) and isinstance(single_Real_data, list):   # 字典类型
                        State, Info= self.__JsonList(single_Real_data, single_Expect_data)
                        if State == '0':
                            logger.info('数据匹配失败.详情：%s' %Info)
                            return State, Info
                        continue
                    else:                                                           # 判断普通类型
                        return '0', 'Values are not equal! Real: ' + str(single_Real_data) + '  Expect: ' + str(single_Expect_data)
                elif single_Expect_data == single_Real_data:
                    logger.debug('匹对成功退出当次循环')
                    continue
                else:
                    return '0', 'unknown error'
            return '1', None # 数据正确
        except KeyError, e:
            logger.error('发生异常！！！错误信息%s' % e)
            return '0', 'KeyError:' + e


    # 处理字典类型数据  字典1，字典2 返回状态1或0 信息1 信息2
    def __JsonDict(self, Real_dict, Reference_dict):
        try:
            check_state, Real_key, Reference_key = self.__check_dit_key(Real_dict, Reference_dict)   # 检查同级的key是否相等
            if check_state == '0':
                return '0', 'The key is not equal! Real_key: ' + str(Real_key) + '  Reference_key: ' + str(Reference_key)
            for kb, vb in Real_dict.items():  # 取响应数据中的一组
                if kb not in Reference_dict:
                    logger.debug('在期望数据中找不到key: %s ' % kb)
                    return '0', 'Reference data NoFound Key :  ' + str(kb)
                elif isinstance(vb, dict) and isinstance(Reference_dict[kb], dict):   # 如果参考数据是字典类型
                    State, Info= self.__JsonDict(vb, Reference_dict[kb])
                    if State == '0':
                         logger.debug('数据匹配失败。详情：%s' %Info)
                         return '0', Info
                elif isinstance(vb, list) and isinstance(Reference_dict[kb], list):       # 调用列表匹配
                    State, Info= self.__JsonList(vb, Reference_dict[kb])
                    if State == '0':
                         logger.debug('数据匹配失败。详情：%s' %Info)
                         return '0', Info
                elif isinstance(Reference_dict[kb], dict) and not isinstance(vb, dict) and 'len' in Reference_dict[kb] and len(Reference_dict[kb].keys()) ==1:   # 动态数据对比数据长度
                    State, Info = self.__JsonLen(vb, Reference_dict[kb])
                    if State == '0':
                        logger.debug('数据匹配失败。详情：%s' %Info)
                        return '0', Info
                    break
                elif kb in Reference_dict and Reference_dict[kb] != vb:
                    logger.debug('匹对失败。返回key: %s 值:%s  参考Key：%s  值：%s' % (kb, vb, kb ,Reference_dict[kb]))
                    return '0', 'Values are not equal! Real Key: ' + str(kb) + ' Value: ' + str(vb) + '  Expect Key: ' + str(kb) + ' Value: ' + str(Reference_dict[kb])    # 返回失败状态0 返回参数 参考数
                else:
                    return '0', 'unknown error'
            return '1', None   # 返回成功
        except KeyError, e:
            logger.error('错误信息%s' % e)
            return '0', 'KeyError:' + str(e)

    # 用于检查同一级的json数据的key是否相等
    def __check_dit_key(self,RealData, ReferenceData):
        RealData_all_key = RealData.keys()
        ReferenceData_all_key = ReferenceData.keys()
        RealData_all_key.sort()
        ReferenceData_all_key.sort()
        if RealData_all_key != ReferenceData_all_key:   # 如果不同等刚找出不相等的key
            if len(RealData_all_key) >= len(ReferenceData_all_key):
                for key_name in RealData_all_key:
                    if key_name in ReferenceData_all_key:
                        continue
                    elif RealData_all_key.index(key_name) > (len(ReferenceData_all_key)-1):   # 判断是否超出长度
                         return '0', key_name, 'Not Found'
                    else:
                        return '0', key_name, ReferenceData_all_key[RealData_all_key.index(key_name)]
            else:
                for key_name in ReferenceData_all_key:
                    if key_name in RealData_all_key:
                        continue
                    elif ReferenceData_all_key.index(key_name) > (len(RealData_all_key)-1):   # 判断是否超出长度
                         return '0', 'Not Found', key_name
                    else:
                        return '0', RealData_all_key[ReferenceData_all_key.index(key_name)], key_name
        else:
            return '1', '', ''

    # 对比所有数据（要求返回与预期的数据字段一定要相等）
    def cmp_json(self,RealData,ReferenceData):
        '''json数据对比 RealData 是响应返回的数据  ReferenceData 是期望数据
            |@{result}|cmp_json_all|@{RealData}|@{ReferenceData}|
        '''
        # try:
        if not isinstance(RealData, dict):
            RealData = json.loads(RealData)
        if not isinstance(ReferenceData, dict):
            ReferenceData = json.loads(ReferenceData)
        check_state, Real_key, Reference_key = self.__check_dit_key(RealData, ReferenceData)   # 检查同级的key是否相等
        if check_state == '0':
            return '0', 'The key is not equal! Real_key: ' + str(Real_key) + '  Reference_key: ' + str(Reference_key)
        for key, value in RealData.items():
            if (key in ReferenceData):
                if isinstance(ReferenceData[key], list) and isinstance(value, list):  # 列表类型数据
                    State, Info = self.__JsonList(value, ReferenceData[key])
                    if State == '0':
                        logger.info('数据匹配失败。详情：%s' %Info)
                        return State, Info
                    continue
                elif isinstance(ReferenceData[key], dict) and isinstance(value, dict):   # 字典类型
                    State, Info= self.__JsonDict(value, ReferenceData[key])
                    if State== '0':
                        logger.info('数据匹配失败.详情：%s' %Info)
                        return State, Info
                    continue
                elif isinstance(ReferenceData[key], dict) and not isinstance(value, dict) and 'len' in ReferenceData[key] and len(ReferenceData[key].keys()) ==1: # 只判断长度类型
                    State, Info= self.__JsonLen(value, ReferenceData[key])
                    if State == '0':
                        logger.info('数据匹配失败。详情：%s' %Info)
                        return '0', Info
                    continue
                elif key in RealData and ReferenceData[key] != value:               # 普通数据判断
                    logger.info('实返回数据：%s:%s 期望返回数据：%s:%s' % (key, value, key, ReferenceData[key]))
                    return '0', 'Values are not equal! Real key: ' + str(key) + ' value: '+ str(value) + '   Reference key: ' + str(key) + ' value: ' + str(ReferenceData[key])
                else:
                    return '0', 'unknown error'
            else:                            # key不在返回数据里
                logger.info('在响应数据里找不到该 %s Key' %key)
                return '0', 'Key Name: '+ str(key) + '  in Reference data NoFound '      # 返回失败原因
        return '1', None


    # 处理字典类型  返回状态1表示查询到数据
    def __key_dict_type(self, parameter, target):
        for k, v in parameter.items():
            if k == target:
                return '1', v
            elif isinstance(v, list):
                state, result = self.__key_list_type(v, target)
                if state == '1':
                    return state, result
            elif isinstance(v, dict):
                state, result = self.__key_dict_type(v, target)
                if state == '1':
                    return state, result
        return '0', None


    # 处理列表类型  返回状态1表示查询到数据
    def __key_list_type(self, parameter, target):
        list_len = len(parameter)
        for i in range(list_len):
            read_data = parameter[i]
            if isinstance(read_data, dict):
                state, result = self.__key_dict_type(read_data, target)
                if state == '1':
                    return state, result
        return '0', None


    # 取json数据中的值
    def get_json_value(self, parameter, target):
        '''取json中的值  parameter是json数据  target：json中的Key
            |@{result}|get_json_value|parameter|target|
        '''
        if not isinstance(parameter, dict):
            try:
                parameter = json.loads(parameter)
            except:
                parameter =eval(parameter)
        for k, v in parameter.items():
            if k == target:
                return '1', v
            elif isinstance(v, list):
                state, result = self.__key_list_type(v, target)
                if state == '1':
                    return state, result
            elif isinstance(v, dict):
                state, result = self.__key_dict_type(v, target)
                if state == '1':
                    return state, result
        return '0', None

    # 保存响应的参数，并合到数据中 key_name以；分开
    def save_key_respond_data(self, respond_data, cache_data, key_name=''):
        '''save_key_respond_data 保存关键的参数或合并数据
            | ${result} | save_key_respond_data | ${respond_data} | ${cache_data} |
        '''
        need_save_data = {}
        try:
            if cache_data is not None:
                cache_data = json.loads(cache_data)
            elif cache_data is None:
                cache_data = {}
        except:
            cache_data = eval(cache_data)
        if len(key_name) != 0:
            for name in key_name.split(';'):
                state, result = self.get_json_value(respond_data, name)
                if state == '1':
                    need_save_data[name] = result
            need_save_data = dict(cache_data, **need_save_data)
        else:
            # respond_data = re.sub(r"(,?)(\w+?)\s+?:", r"\1'\2' :", respond_data)
            # respond_data = respond_data.replace("'", "\"")
            logger.debug(respond_data)
            if respond_data is None:
                return str(cache_data)
            if respond_data is not None and len(respond_data) == 0:
                return str(cache_data)
            if not isinstance(respond_data, dict) and respond_data is not None:
                try:
                    respond_data = json.loads(respond_data)
                except:
                    respond_data = eval(respond_data)
            need_save_data = dict(cache_data, **respond_data)
        return str(need_save_data)

    def get_loop_sum_or_loop_value(self, mode, content, loop_num = '1'):
        '''get_loop_sum_or_loop_value 获取循环次数或第几循环的值 mode 有 sum，content 二种模式  N 表示数字
            | ${sum} | get_loop_sum_or_loop_value | sum | ${content}|
            | @{result} | get_loop_sum_or_loop_value | content | ${content}|  N |
        '''
        loop_sum = 0
        loop_num = int(loop_num)
        if not isinstance(content, dict):
            content = json.loads(content)
        for k, v in sorted(content.items()):
            sql_content = v.split(';')
            for sql in sql_content:
                # print sql
                if mode == 'content' and loop_num == loop_sum:
                    return k, sql
                loop_sum += 1
        if mode == 'sum':
            return loop_sum
        return loop_sum, None


    def get_db_configuration(self, mode, config, order_id='0'):
        '''get_db_configuration 获取循环次数或第几循环的值 mode 有 sum，get_values 二种模式  N 表示数字
            返回数据：数据库类型，数据库用户，连接参数
            | ${sum} | get_db_configuration | sum | ${content}|
            | @{result} | get_db_configuration | get_values |${content}|  N |
        '''
        loop_sum = 0
        order_id = int(order_id)
        if not isinstance(config, dict):
            config = json.loads(config)
        if mode == 'sum':
            return len(config.keys())
        elif mode == 'get_values':
            for k, v in sorted(config.items()):
                if loop_sum == order_id:
                    return v['db_type'], k, v['connect']
                loop_sum += 1

    def replace_json_data(self, old_data, new_data):
        '''replace_json_data 替换json数据
            | ${result} | replace_json_data | ${old_data} | ${new_data}|
        '''
        if None == new_data:
            return old_data
        try:
            if not isinstance(new_data, dict):
                new_data = json.loads(new_data)
        except:
                new_data = eval(new_data)
        all_keys_new_data = new_data.keys()
        need_keys = []
        for key_name in  all_keys_new_data:
            result, info = self.get_json_value(old_data, key_name)
            if result == '1':
                need_keys.append(key_name)
        logger.debug('need_keys:%s' %need_keys)
        if len(need_keys) != 0:
            if not isinstance(old_data, dict):
                encoding_old_data = json.loads(old_data)         # 需要先编码，再能编码
                need_return_data = json.dumps(encoding_old_data, sort_keys=True)
            else:
                need_return_data = old_data
            for name in need_keys:
                old_result, old_info = self.get_json_value(need_return_data, name)
                new_result, new_info = self.get_json_value(new_data, name)
                if isinstance(old_info, (dict,list)):
                    new_info= json.dumps(new_info, sort_keys=True)
                    old_info =json.dumps(old_info, sort_keys=True)
                else:
                    old_info = str(old_info)
                    new_info = str(new_info)
                need_return_data = need_return_data.replace(old_info, new_info)
                logger.debug('need_return_data:%s' %need_return_data)
            return need_return_data
        return old_data


                
if __name__ == '__main__':
    pass
