
import os
import json

class RestTemplateCheck(object):
    _file_fd = None
    _sep = None
    _lines = None
    _read_handle_line = []

    _is_success = True

    def __init__(self, file_path=None, sep=";"):
        if file_path:
            self._file_path = file_path
            self._sep = sep
            self.loadFile()
            self.checkFormat()
            self.checkEachLine()
        else:
            self._is_success = False

    # 读取rest模板文件
    def loadFile(self):
        self._file_fd = open(self._file_path, 'r')
        self._lines = self._file_fd.readlines()
        self._file_fd.close()

    # 检查每行的格式
    def checkFormat(self):
        for line in self._lines:
            rel = line.strip('\n')
            line = line.strip('\n').split(self._sep)

            if self.checkFlag(line):    # 10或11开头的为正确的模板行
                self._read_handle_line.append(rel)

    # 跳过非10、11的行
    def checkFlag(self, line_list):
        if line_list[0] != '10' and line_list[0] != '11':
            return False

        return True

    # 检查每一行符合flag要求的格式
    def checkEachLine(self):
        for r_line in self._read_handle_line:
            line_list = r_line.split(self._sep)
            if (line_list[0] == '11'):
                continue

            if len(line_list) != 7:
                self._is_success = False
                print('The following line, the length after split is not equal to 7')
                print(r_line)
                print('after split:')
                print(line_list)
                print('---------')
                continue

            '''
                正确的情况下，对语法格式做出判断
            '''
            self.checkContents(r_line)

    # introduction: 10,<id>,<method>,<uri>,<content-type>,<accept>,<template>
    def checkContents(self, line):
        line_list = line.split(self._sep)
        # 10;107;PUT;/inventory/managedObjects/%%;application/json;;{}
        flag = line_list[0]
        template_id = line_list[1]
        http_method = line_list[2]
        http_uri = line_list[3]
        content_type = line_list[4]
        accpet = line_list[5]

        if http_method == 'GET':
            return

        template = line_list[6]

        try:
            json_reader = json.loads(template)
        except Exception as e:
            self._is_success = False
            print('line cannot convert to json: ')
            print(line)

    def getResult(self):
        if self._is_success:
            return "template format correct"
        else:
            return  "template format incorrect"

if __name__ == '__main__':
    file_path = 'resttemplate.csv'
    rest_template_check = RestTemplateCheck(file_path=file_path)

    print(rest_template_check.getResult())