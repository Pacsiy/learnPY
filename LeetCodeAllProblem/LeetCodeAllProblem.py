#! /usr/bin/python
# -*- coding:UTF-8 -*-

import xlrd
import xlwt


class myExcel(object):
    def __init__(self, excelPath):
        self.path = excelPath

    def readExcel(self):
        excel = xlrd.open_workbook(self.path)

        # get sheet names
        print(excel.sheet_names())
        # get sheet content(By index or By name)
        sheet = excel.sheet_by_index(0)
        sheet1 = excel.sheet_by_name("Sheet1")
        sheet2 = excel.sheets()[0]
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

        return excel

    def printExcel(self):
        excel = self.readExcel()
        sheet = excel.sheets()[0]
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
        excel = xlwt.Workbook()
        sheet = excel.add_sheet('sheet1', cell_overwrite_ok=True)

        headList = ['Stu_id', 'name', 'sex']
        data = [['1', 'stu1', '男'],
                ['2', 'stu2', '男'],
                ['3', 'stu3', '女'],]

        self.writeOneRow(sheet, 0, headList)
        for nrow in range(0, 3):
            self.writeOneRow(sheet, nrow, data[nrow])

        excel.save(excelName)

    def toMarkdown(self, mdName):
        excel = self.readExcel()
        sheet = excel.sheets()[0]

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


def main():
    excel = myExcel(r'./LeetCodeAllProblem.xlsx')
    excel.readExcel()
    excel.writeExcel(r'newExcel.xls')
    print('开始写入Markdown文件...')
    excel.toMarkdown(r'LeetCodeAll.md')


if __name__ == "__main__":
    main()