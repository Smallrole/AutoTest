# coding=utf-8
import os,sys,xlrd,json
from string import Template
#reload(sys)
#sys.setdefaultencoding('utf-8')



start_content = '''*** Settings ***
Resource          AutomaticTestResources.txt

*** Test Cases ***
'''

content = '''${test_case_suite}
    [Documentation]    ${test_case_suite_documentation}
    [Tags]${test_case_tags}
    单接口测试    ${test_case_id}

'''

function_start_content = '''*** Settings ***
Resource          AutomaticTestResources.txt

 '''

function_variables = '''*** Variables ***
@{function_case_id}${function_case_all_id}

*** Test Cases ***
'''

function_case = '''${function_case_name}
    [Tags]${test_case_tags}
    [Timeout]    1 minute
    功能测试    ${test_case_id}    @{function_case_id}

'''

class robot_tool_box():
    # 打开表格
    def __init__(self, current_path = ''):
        self.work_table = None
        self.interface_all_mered_calls = None     # 单接口测试
        self.function_all_mered_calls = None    # 功能测试组
        self.function_data_all_mered_calls = None  # 功能测试用例
        self.default_all_mered_calls = None        # 默认时使用
        self.all_test_case_sum = 0
        if current_path == '':
            self.current_path = os.getcwd()
        else:
            self.current_path = current_path

    def open_table(self, table_path):
        ex = xlrd.open_workbook(table_path)
        self.work_table = ex

    # 获取表中的所有合并单元格位置
    def get_all_mered_calls(self, table_name=''):
        # table = self.work_table.sheet_by_index(0)
        if table_name == 'function':
            table = self.work_table.sheet_by_name(table_name)
            all_merged_cells = table.merged_cells
            self.function_all_mered_calls = all_merged_cells
        elif table_name == 'data':
            table = self.work_table.sheet_by_name(table_name)
            all_merged_cells = table.merged_cells
            self.function_data_all_mered_calls = all_merged_cells
        elif table_name == 'interface':
            table = self.work_table.sheet_by_name(table_name)
            all_merged_cells = table.merged_cells
            self.interface_all_mered_calls = all_merged_cells
        else:
            table = self.work_table.sheet_by_index(0)
            all_merged_cells = table.merged_cells
            self.default_all_mered_calls = all_merged_cells

    # 获取接口测试用例数据
    def get_test_case_data(self, table_name, row):
        try:
            if table_name == 'function':
                merged_info = self.function_all_mered_calls
            elif table_name == 'data':
                merged_info = self.function_data_all_mered_calls
            elif table_name == 'interface':
                merged_info = self.interface_all_mered_calls
            table = self.work_table.sheet_by_name(table_name)
            row = int(row)
            row_date = table.row_values(row)
            for merged in merged_info:
                row_start_num, row_end_num, line_start_num, line_end_num = merged
                if row_date[1] == '':
                    if row >= row_start_num and row < row_end_num and 1 >= line_start_num and 1 < line_end_num:
                        row_date[1] = table.cell(row_start_num, line_end_num - line_start_num).value
                if row_date[2] == '':
                    if row >= row_start_num and row < row_end_num and 2 >= line_start_num and 2 < line_end_num:
                        row_date[2] = table.cell(row_start_num, line_start_num).value
                if row_date[4] == '':
                    if row >= row_start_num and row < row_end_num and 4 >= line_start_num and 4 < line_end_num:
                        row_date[4] = table.cell(row_start_num, line_start_num).value
                if row_date[5] == '':
                    if row >= row_start_num and row < row_end_num and 5 >= line_start_num and 5 < line_end_num:
                        row_date[5] = table.cell(row_start_num, line_start_num).value
            return row_date
        except IndexError:
            pass

    # 获取单条功能
    def get_function_data(self, table_name, row):
        try:
            if table_name == 'function':
                merged_info = self.function_all_mered_calls
            elif table_name == 'data':
                merged_info = self.function_data_all_mered_calls
            elif table_name == 'interface':
                merged_info = self.interface_all_mered_calls
            table = self.work_table.sheet_by_name(table_name)
            row = int(row)
            row_date = table.row_values(row)
            for merged in merged_info:
                row_start_num, row_end_num, line_start_num, line_end_num = merged
                if row_date[1] == '':
                    if row >= row_start_num and row < row_end_num and 1 >= line_start_num and 1 < line_end_num:
                        row_date[1] = table.cell(row_start_num, line_end_num - line_start_num).value
                if row_date[3] == '':
                    if row >= row_start_num and row < row_end_num and 3 >= line_start_num and 3 < line_end_num:
                        row_date[3] = table.cell(row_start_num, line_start_num).value
                if row_date[4] == '':
                    if row >= row_start_num and row < row_end_num and 4 >= line_start_num and 4 < line_end_num:
                        row_date[4] = table.cell(row_start_num, line_start_num).value
                if row_date[5] == '':
                    if row >= row_start_num and row < row_end_num and 5 >= line_start_num and 5 < line_end_num:
                        row_date[5] = table.cell(row_start_num, line_start_num).value
                if row_date[6] == '':
                    if row >= row_start_num and row < row_end_num and 6 >= line_start_num and 6 < line_end_num:
                        row_date[6] = table.cell(row_start_num, line_start_num).value
                if row_date[9] == '':
                    if row >= row_start_num and row < row_end_num and 9 >= line_start_num and 9 < line_end_num:
                        row_date[9] = table.cell(row_start_num, line_start_num).value
            return row_date
        except IndexError:
            pass

     # 获取某功能的所有顺序id
    def get_function_all_id(self, function_name):
        num = 1
        all_id = []
        while 1:
            row_date = self.get_function_data('function', num)
            if row_date is None:  # 整表循环完成
                return all_id
            if row_date[3] == function_name:
                all_id.append(int(row_date[0]))
            num += 1
        return all_id

    # 创建文件
    def create_test_case_file(self, test_case_path, order_num, file_name):
        number = "%04d" %order_num
        file_path = test_case_path + '\\' + number + '-' + file_name + '.txt'
        if isinstance(file_name, unicode):
            file_path_new =test_case_path + '\\' + number + '-' + file_name.encode('utf-8') + '.txt'
        print ('新建文件，路径为：%s' % file_path_new)
        return open(file_path, 'w')

    #  功能删除文件
    def file_processing(self, file_path, operation, target):
        all_file = os.listdir(file_path)
        if operation == 'remove':
            if target == '*':
                for file_name in all_file:
                    os.remove(file_path + '\\' + file_name)
                    print('删除文件，文件路径为： ' + file_path + '\\' + file_name.decode('gbk').encode('utf-8'))
        elif operation == 'only_reserve':
            need_save_file =[]
            for file_name in target.split(';'):
                if file_name in all_file and file_name not in need_save_file:
                    need_save_file.append(file_name)
            for name in need_save_file:
                all_file.remove(name)
            for file_name in all_file:
                os.remove(file_path + '\\' + file_name)
                print('删除文件，文件路径为： ' + file_path + '\\' + file_name.decode('gbk').encode('utf-8'))

    # 写文件 mode  only_write   replace_content
    def write_test_case_file(self, open_test_case_file, mode, case_content, file_type='', *test_case_data):
        if mode == 'only_write':
            open_test_case_file.writelines(case_content)
            return open_test_case_file
        elif mode == 'replace_content':
            if file_type == 'interface':
                case_tags = ''
                for t in test_case_data[6].split(';'):
                    case_tags = case_tags + '    ' + t
                suite_name = test_case_data[0].encode('utf-8') + '-' + test_case_data[3].encode('utf-8')
                suite_documentation = test_case_data[27].encode('utf-8')
                case_content = Template(case_content)
                if isinstance(case_tags, unicode):
                    case_tags =case_tags.encode('utf-8')
                case_content = case_content.substitute(test_case_suite=suite_name, test_case_suite_documentation=suite_documentation,
                                                       test_case_tags=case_tags,
                                                       test_case_id=test_case_data[0].encode('utf-8'))
                open_test_case_file.writelines(case_content)
                self.all_test_case_sum += 1
                return open_test_case_file
            elif file_type == 'function_all_case_id':
                all_id = ''
                for i in test_case_data:
                   all_id =all_id +  '    ' + str(i)
                case_content = Template(case_content)
                case_content = case_content.substitute(function_case_all_id=all_id)
                open_test_case_file.writelines(case_content)
                return open_test_case_file
            elif file_type == 'function':
                case_tags = ''
                for t in test_case_data[3].split(';'):
                    case_tags = case_tags + '    ' + t
                case_content = Template(case_content)
                case_content = case_content.substitute(function_case_name=(test_case_data[0].encode('utf-8') + '-' + test_case_data[2].encode('utf-8')),
                                                       test_case_tags=case_tags,test_case_id=test_case_data[0].encode('utf-8'))
                open_test_case_file.writelines(case_content)
                self.all_test_case_sum += 1
        return open_test_case_file

    # 检查json数据是否有效
    def check_json_data(self, data):
        try:
            json.loads(data)
            return '1'
        except ValueError:
            return '0'

    # 获取动态测试用例列号id
    def get_dynamic_id(self, *case_data):
        dynamic_id =[]
        for j in range(1,16): # 检测动态的列 1-15
            for k in [15, 16, 18, 19]:
                id = k + 6*(j-1)
                if id > len(case_data):
                    return dynamic_id
                elif len(case_data[id]) !=0:
                    dynamic_id.append(id)
        return dynamic_id

    def check_test_case_data(self, test_case_file_path, mode):
        error_info = {}
        cache =[]
        if mode == 'interface':
            self.open_table(test_case_file_path)
            self.get_all_mered_calls(mode)
            check_list =[5, 8, 9, 13, 14,17, 19, 21, 22, 23]
            test_case_id = 1
            while 1:
                test_case_data = self.get_test_case_data(mode, test_case_id)
                if test_case_data is None:
                    print('interface全表信息检查完成。')
                    break
                for i in check_list:
                    if len(test_case_data[i]) != 0:
                        result = self.check_json_data(test_case_data[i])
                        if result == '0':
                            cache.append(i)
                if len(cache) !=0:
                    error_info[test_case_id] =cache
                    cache =[]
                test_case_id +=1
        elif mode == 'function':
            self.open_table(test_case_file_path)
            self.get_all_mered_calls(mode)
            self.get_all_mered_calls('data')
            check_rule_list =[5, 7, 9, 10, 11]
            cache =[]        # 保存错误列号
            test_case_id = 1
            while 1:
                test_case_data = self.get_test_case_data('data', test_case_id)
                if test_case_data is None:
                    print('function表中的data全表信息检查完成。')
                    break
                check_list = check_rule_list + self.get_dynamic_id(*test_case_data)  # 固定列和动态列合并
                # print 'check_rule_list:', check_list
                for i in check_list:   # 检测列
                    if len(test_case_data[i]) != 0:
                        result = self.check_json_data(test_case_data[i])
                        if result == '0':
                            cache.append(i)
                if len(cache) !=0:
                    error_info[test_case_id] =cache
                    cache =[]
                test_case_id +=1
        if len(error_info) != 0:
            print '****注意****\n\t有一种情况可能是误报错误，但实现运行自动化时不会报错，此种情况是：参化json非字符串的数据。\n' \
                  'json格式错误的信息（**格式说明：{用例序号: [列号]}）：\n',error_info
        else:
            print ('json格式检验通过。')


    # 创建测试用例
    def create_auto_case(self, test_case_file_path, mode):
        if mode == 'interface':
            self.open_table(test_case_file_path)
            self.get_all_mered_calls(mode)
            interface_name = ''
            interface_uri = ''
            interface_sum = 0
            current_file = ''
            test_case_id = 1
            while 1:
                test_case_data = self.get_test_case_data(mode, test_case_id)
                # print(test_case_data)
                if test_case_data is None:
                    current_file.close()
                    print('生成:%d 份文件，共：%d 条测试用例' % (interface_sum, self.all_test_case_sum))
                    break
                if interface_name != test_case_data[2] or interface_uri !=test_case_data[1]:
                    if test_case_data[26] in('0', 0):
                        test_case_id += 1
                        continue
                    interface_uri = test_case_data[1]
                    interface_name = test_case_data[2]
                    interface_sum += 1
                    new_test_file = self.create_test_case_file(self.current_path, interface_sum, test_case_data[2])
                    new_test_file = self.write_test_case_file(new_test_file, 'only_write', start_content)
                    if current_file == '':   # 处理第一次
                        current_file = new_test_file
                    if current_file != new_test_file:
                        current_file.close()
                        current_file = new_test_file
                current_file = self.write_test_case_file(current_file, 'replace_content', content, mode, *test_case_data)
                test_case_id += 1
        elif mode == 'function':
            self.open_table(test_case_file_path)
            self.get_all_mered_calls(mode)
            self.get_all_mered_calls('data')
            function_name = ''
            function_sum = 0
            current_file = ''
            test_case_id = 1
            while 1:
                test_case_data = self.get_test_case_data('data', test_case_id)
                if test_case_data is None:
                    current_file.close()
                    print('生成:%d 份文件，共：%d 条测试用例' % (function_sum, self.all_test_case_sum))
                    break
                if function_name != test_case_data[1]:
                    if test_case_data[12] in('0', 0):
                        test_case_id += 1
                        continue
                    function_case_all_id = self.get_function_all_id(test_case_data[1])
                    if len(function_case_all_id) !=0:
                        function_name = test_case_data[1]
                        function_sum += 1
                        function_data = self.get_function_data(mode,function_case_all_id[0])
                        new_test_file = self.create_test_case_file(self.current_path, function_sum, function_data[4])
                        new_test_file = self.write_test_case_file(new_test_file, 'only_write', function_start_content)
                        new_test_file = self.write_test_case_file(new_test_file, 'replace_content', function_variables,
                                                                  'function_all_case_id',*function_case_all_id)
                        if current_file == '':
                            current_file = new_test_file
                        if current_file != new_test_file:
                            current_file.close()
                            current_file = new_test_file
                if function_name == test_case_data[1]:
                    current_file = self.write_test_case_file(current_file, 'replace_content', function_case, mode, *test_case_data)
                test_case_id += 1

if __name__ == '__main__':
    toast = '''**注意**
    1.脚本在创建文件时，会删除所有旧的测试用例；
    2.确保文件夹里需要保存的文件名已加入到need_save_file_name列表里；
    3.需要确定 case_model 模式是否与测试用例相对应；
    4.此脚本需放在与测试用例同一目录里；
    5.运行模式序号：1   功能：校验测试用例json数据格式是否正确；
      运行模式序号：2   功能：生成自动化测试用例。
'''
    if len (sys.argv) >1:
        current_path = sys.argv[1]
        run_model = '2'
        box = robot_tool_box(current_path)
    else:
        print (toast)
        run_model = raw_input('请输入运行模式的序号：')
        current_path = os.getcwd()
        box = robot_tool_box()
    ignore =''                    # 忽略的行号和列号  常误报的列号可以设置此参数
    case_model = 'interface'      # 根据实际情况来修改  如果是接口测试的请填写 interface， 如果 功能测试的 则填写function
    need_save_file_name = '.idea;__init__.txt;RF_tool_box.py;RF_tool_box_3.py;AutomaticTestResources.txt;function.xlsx;~$function.xlsx;interface.xlsx;~$interface.xlsx'
    interface_test_case_path = ''
    function_test_case_path = ''
    if case_model == 'interface':
        interface_test_case_path = os.path.join(current_path, 'interface.xlsx')   # 接口测试用例
    elif case_model == 'function':
        function_test_case_path = os.path.join(current_path, 'function.xlsx')     # 功能测试用例
    if function_test_case_path != '':
        print ('当前路径: %s   测试用例文件路径： %s' %(current_path, function_test_case_path))
        if run_model == '1':
            box.check_test_case_data(function_test_case_path, 'function')
        elif run_model == '2':
            box.file_processing(current_path, 'only_reserve', need_save_file_name)
            box.create_auto_case(function_test_case_path, 'function')
        else:
            print ('提示：请重新运行脚本，并请输入正确的运行模式序号！！！')
    elif interface_test_case_path != '':
        print ('当前路径: %s   测试用例文件路径： %s' %(current_path, interface_test_case_path))
        if run_model == '1':
            box.check_test_case_data(interface_test_case_path, 'interface')
        elif run_model == '2':
            box.file_processing(current_path, 'only_reserve',need_save_file_name)
            box.create_auto_case(interface_test_case_path, 'interface')
        else:
            print ('提示：请重新运行脚本，并请输入正确的运行模式序号！！！')
    else:
        print ('提示：没有找到指定测试用例文件，请填写正确的case_model模式。')
