# coding=utf-8

import xlrd
from robot.api import logger

class read_test_case_data(object):
    # 打开表格
    def __int__(self):
        self.interface_all_mered_calls=None     # 单接口测试
        self.function_all_mered_calls = None    # 功能测试组
        self.function_data_all_mered_calls = None  # 功能测试用例
        self.default_all_mered_calls = None        # 默认时使用

    def open_table(self, table_path):
        '''open_table 打开表格
            | ${openfile} | open_table | table_path |
        '''
        ex = xlrd.open_workbook(table_path)
        return ex
		
    # 获取表中的所有合并单元格位置
    def get_all_mered_calls(self, work_table, table_name =''):
        '''get_all_mered_calls 获取合并单元格位置
            | ${openfile} | open_table | table_path |
            | @{all_mered_calls} | get_all_mered_calls | ${openfile} |
        '''
        if table_name == 'function':
            table = work_table.sheet_by_name(table_name)
            all_merged_cells = table.merged_cells
            self.function_all_mered_calls = all_merged_cells
        elif table_name == 'data':
            table = work_table.sheet_by_name(table_name)
            all_merged_cells = table.merged_cells
            self.function_data_all_mered_calls = all_merged_cells
        elif table_name == 'interface':
            table = work_table.sheet_by_name(table_name)
            all_merged_cells = table.merged_cells
            self.interface_all_mered_calls = all_merged_cells
        else:
            table = work_table.sheet_by_index(0)
            all_merged_cells = table.merged_cells
            self.default_all_mered_calls = all_merged_cells
        return all_merged_cells

    # 获取接口测试用例数据
    def get_test_case_data(self, work_table, table_name, row):
        '''get_row_all_data 获取接口测试用例数据单条数据
            | ${openfile} | open_table | table_path |
            | @{all_mered_calls} | get_all_mered_calls | ${openfile} |
            | @{test_case_date} | get_interface_test_case_data | ${openfile}| interface | 1 | @{all_mered_calls} |
        '''
        try:
            if table_name == 'function':
                merged_info = self.function_all_mered_calls
            elif table_name == 'data':
                merged_info = self.function_data_all_mered_calls
            elif table_name == 'interface':
                merged_info = self.interface_all_mered_calls
            table = work_table.sheet_by_name(table_name)
            row = int(row)
            row_date = table.row_values(row)
            for merged in merged_info:
                row_start_num, row_end_num, line_start_num, line_end_num = merged
                if row_date[1] == '':
                    if row >= row_start_num and row < row_end_num and 1 >= line_start_num and 1 < line_end_num:
                        row_date[1] = table.cell(row_start_num, line_end_num - line_start_num).value
                        logger.debug(row_date[1])
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
    def get_function_data(self, work_table, table_name, row):
        '''get_function_data 获取单条功能数据
            | ${openfile} | open_table | table_path |
            | @{all_mered_calls} | get_all_mered_calls | ${openfile} |
            | @{test_case_date} | get_function_data | ${openfile}| function | 1 | @{all_mered_calls} |
        '''
        try:
            if table_name == 'function':
                merged_info = self.function_all_mered_calls
            elif table_name == 'data':
                merged_info = self.function_data_all_mered_calls
            elif table_name == 'interface':
                merged_info = self.interface_all_mered_calls
            table = work_table.sheet_by_name(table_name)
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

    def get_function_all_id(self, work_table, function_name):
        '''get_function_all_id 获取某功能的所有顺序id  function_name:暂时只支持 function
            |@{test_case_date}| combined_case | ${work_table} | function |
        '''
        num = 1
        all_id = []
        while 1:
            row_date = self.get_function_data(work_table, 'function', num)
            if row_date is None:  # 整表循环完成
                return all_id
            if row_date[3] == function_name:
                all_id.append(int(row_date[0]))
            num += 1
        return all_id

    def combined_case(self, function_sum,*data_package):
        '''combined_case 组合用例  function_sum:功能组个数 data_package = 功能组 + 功能数据 + 测试用例数据
            |@{test_case_date}| combined_case | ${function_sum} |@{data_package} |
        '''
        function_sum = int(function_sum)
        function_data_end_id = function_sum + 16   # 16代表功能的列数
        completion = ['']
        function_all_id = data_package[0:function_sum]
        function_data = list(data_package[function_sum:function_data_end_id]) # 功能数据
        all_test_case_data = list(data_package[function_data_end_id:])       # 用例数据
        test_case_id = function_data[0]
        request_data_start = 15 +(6*(int(function_data[8]) -1))         # 请求数据开始位置
        response_data_start = 18 +(6*(int(function_data[11]) -1))       # 响应数据开始位置
        case_data = []
        logger.debug('test_case_id:%s  type:%s  function_all_id[0]:%s  type:%s  function_all_id[-1]:%s  type:%s' %
                     (test_case_id, type(test_case_id), function_all_id[0], type(function_all_id[0]), function_all_id[-1], type(function_all_id[-1])))
        if len(function_all_id) ==1:                # 处理只一个接口的情况
            case_data.append(all_test_case_data[0]) # 用例序号0
            case_data.append(function_data[1])      # 接口地址1
            case_data.append(function_data[2])      # 接口说明2
            case_data.append(all_test_case_data[2]) # 用例标题3
            case_data.append(function_data[5])      # 请求方式4
            case_data.append(function_data[6])      # 请求头5
            case_data.append(function_data[7])      # 标签6
            case_data = case_data + all_test_case_data[request_data_start:request_data_start +3] + function_data[9:11] +\
                        all_test_case_data[response_data_start:response_data_start +3]
            case_data.append(function_data[12])     # 关键数据-15
            if all_test_case_data[14] != '1':       # 判断响应数据是否需要加解密
                case_data.append(function_data[13])     # 加密数据-16
            else:
                case_data.append('')     # 加密数据-16
            case_data = case_data + all_test_case_data[4:12] + 2*completion
            return case_data
            
        elif test_case_id == function_all_id[0]:      # 判断是否第一条数据
            case_data.append(all_test_case_data[0]) # 用例序号0
            case_data.append(function_data[1])      # 接口地址1
            case_data.append(function_data[2])      # 接口说明2
            case_data.append(all_test_case_data[2]) # 用例标题3
            case_data.append(function_data[5])      # 请求方式4
            case_data.append(function_data[6])      # 请求头5
            case_data.append(function_data[7])      # 标签6
            case_data = case_data + all_test_case_data[request_data_start:request_data_start +3] + function_data[9:11] +\
                        all_test_case_data[response_data_start:response_data_start +3]
            case_data.append(function_data[12])     # 关键数据-15
            if all_test_case_data[14] != '1':       # 判断响应数据是否需要加解密
                case_data.append(function_data[13])     # 加密数据-16
            else:
                case_data.append('')     # 加密数据-16
            case_data = case_data + all_test_case_data[4:6] + 8*completion
            return case_data
        elif test_case_id == function_all_id[-1]: # 判断是否最后一条数据
            case_data.append(all_test_case_data[0])
            case_data.append(function_data[1])
            case_data.append(function_data[2])
            case_data.append(all_test_case_data[2])
            case_data.append(function_data[5])
            case_data.append(function_data[6])
            case_data.append(function_data[7])
            case_data = case_data + all_test_case_data[request_data_start:request_data_start +3] + function_data[9:11] +\
                        all_test_case_data[response_data_start:response_data_start +3]
            case_data.append(function_data[12])     # 关键数据-15
            if all_test_case_data[14] != '1':       # 判断响应数据是否需要加解密
                case_data.append(function_data[13])     # 加密数据-16
            else:
                case_data.append('')                # 加密数据-16
            case_data = case_data + 2*completion + all_test_case_data[6:12] + 2*completion
            return case_data
        else: # 普通合成
            case_data.append(all_test_case_data[0])
            case_data.append(function_data[1])
            case_data.append(function_data[2])
            case_data.append(all_test_case_data[2])
            case_data.append(function_data[5])
            case_data.append(function_data[6])
            case_data.append(function_data[7])
            case_data = case_data + all_test_case_data[request_data_start:request_data_start +3] + function_data[9:11] +\
                        all_test_case_data[response_data_start:response_data_start +3]
            case_data.append(function_data[12])     # 关键数据-15
            if all_test_case_data[14] != '1':       # 判断响应数据是否需要加解密
                case_data.append(function_data[13])     # 加密数据-16
            else:
                case_data.append('')                # 加密数据-16            
            case_data = case_data +10*completion
            return case_data

if __name__ == '__main__':
    pass
