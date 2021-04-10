# -*- coding:utf-8*-
import os
from PyPDF2 import PdfFileReader, PdfFileWriter
import time

time1 = time.time()


def getDeleteInterval(delete_page):
    interval = []
    nums_str = delete_page.split(",")
    for num_str in nums_str:
        if "-" in num_str:
            start = eval(num_str.split("-")[0])
            end = eval(num_str.split("-")[1])
            for page in range(start, end + 1):
                interval.append(page)
        else:
            page = eval(num_str)
            interval.append(page)
    return interval


# ######################### 删除PDF文件中的指定页码 ########################
def deletePDF(input_dirPath, delete_page):
    output_dirPath = input_dirPath.split(".pdf")[0] + "_new.pdf"
    output = PdfFileWriter()
    deleteInterval = getDeleteInterval(delete_page)
    print(deleteInterval)

    # 读取源pdf文件
    input = PdfFileReader(open(input_dirPath, "rb"))

    # 如果pdf文件已经加密，必须首先解密才能使用pyPdf
    if input.isEncrypted:
        input.decrypt("map")

    # 获得源pdf文件中页面总数
    pageCount = input.getNumPages()
    outputPages = pageCount - len(deleteInterval)
    print(pageCount)

    # 分别将page添加到输出output中
    for iPage in range(1, pageCount+1):
        if iPage not in deleteInterval:
            output.addPage(input.getPage(iPage-1))

    print("All Pages Number:" + str(outputPages))
    # 最后写pdf文件
    outputStream = open(output_dirPath, "wb")
    output.write(outputStream)
    outputStream.close()
    print("finished")


if __name__ == '__main__':
    input_dirPath = r'C:\Users\甄雨寒\Desktop\111.pdf'
    delete_page = input("请输入要删除的页码（多个页码用逗号隔开）: ")
    deletePDF(input_dirPath, delete_page)

    time2 = time.time()
    print(u'总共耗时：' + str(time2 - time1) + 's')