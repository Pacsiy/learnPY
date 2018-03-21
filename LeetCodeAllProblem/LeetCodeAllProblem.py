#! /usr/bin/python
# -*- coding:UTF-8 -*-

import xlrd
import xlwt
import pymysql


class myExcel(object):
    def __init__(self, excelPath):
        self.path = excelPath
        self.excel = xlrd.open_workbook(excelPath)

    def readExcel(self):
        # get sheet names
        print(self.excel.sheet_names())
        # get sheet content(By index or By name)
        sheet = self.excel.sheet_by_index(0)
        sheet1 = self.excel.sheet_by_name("Sheet1")
        sheet2 = self.excel.sheets()[0]
        # get sheet info
        print(sheet.name, sheet.nrows, sheet.ncols)
        # get row/col content
        row = sheet.row_values(0)
        col = sheet.col_values(0)
        print(row, col)
        # get cell value
        cell = sheet.cell(0, 0)
        print(cell.value)
        print(sheet.cell_value(0, 0))
        print(sheet.row(0)[0].value)
        # get cell ctype:0empty 1string 2number 3date 4boolean 5error
        print(sheet.cell(0, 0).ctype)

    def printExcel(self):
        sheet = self.excel.sheets()[0]
        for i in range(0, sheet.nrows):
            row = sheet.row_values(i)
            for item in row:
                print(item, '|')

    def writeOneRow(self, sheet, nrow, rowList):
        # 格式：{单元格：背景黄色；字体：红色粗体}
        style = xlwt.easyxf('pattern: pattern solid, fore_colour yellow;font: bold 0, color red;')

        ncol = 0
        for row in rowList:
            sheet.write(nrow, ncol, row, style)
            ncol += 1

    def writeExcel(self, excelName):
        # create a Excel and add sheet
        newexcel = xlwt.Workbook()
        newsheet = newexcel.add_sheet('sheet1', cell_overwrite_ok=True)

        headList = ['题号', '题名', '过题率', '难度']
        self.writeOneRow(newsheet, 0, headList)

        sheet = self.excel.sheets()[0]
        for i in range(0, sheet.nrows):
            row = sheet.row_values(i)
            self.writeOneRow(newsheet, i+1, row)

        newexcel.save(excelName)

    def toMarkdown(self, mdName):
        sheet = self.excel.sheets()[0]

        file = open(mdName, 'w', encoding='utf-8')
        rowStr = "| %d | [%s]() | %.3f | %s |\n"

        try:
            file.write('| 编号 | 题名 | 过题率 | 难度 |' + '\n')
            file.write('| :------------: |:---------------: | :------------:| :-----:|' + '\n')

            for i in range(0, sheet.nrows):
                row = sheet.row_values(i)
                data = rowStr % (int(row[0]), str(row[1]).rstrip(), float(row[2]), str(row[3]))
                file.write(data)

            print('成功写入文件，共有%d条记录...' % sheet.nrows)
        except Exception as e:
            print(e)
        finally:
            file.close()

    def upload(self):
        db = pymysql.connect("localhost", "root", "love1125", "PythonTest", charset='utf8')
        cursor = db.cursor()
        cursor.execute('DELETE FROM problem')

        insertStr = '''INSERT INTO problem(pro_id, pro_name, pro_rate, pro_diff) VALUES (%d, "%s", %f, "%s")'''

        try:
            sheet = self.excel.sheets()[0]
            for i in range(0, sheet.nrows):
                row = sheet.row_values(i)
                insertSQL = insertStr % (int(row[0]), str(row[1]).rstrip('\xa0'), float(row[2]), str(row[3]))
                cursor.execute(insertSQL)

            db.commit()
            print('成功上传至数据库...')
        except Exception as e:
            print(e)
            db.rollback()
        finally:
            db.close()

    def main(self):
        self.readExcel()
        print('开始写入新文档...')
        self.writeExcel(r'newExcel.xls')
        print('开始写入Markdown文件...')
        self.toMarkdown(r'LeetCodeAll.md')
        print('开始上传数据库...')
        self.upload()


leetcode = myExcel(r'./LeetCodeAllProblem.xlsx')
leetcode.main()