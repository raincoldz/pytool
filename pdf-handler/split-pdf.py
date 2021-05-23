# -*- coding:utf-8*-
import os
from PyPDF2 import PdfFileReader, PdfFileWriter
import time

time1 = time.time()


# ######################### 将PDF文件每n页拆分为一个文件，命名为 i-i+n-1.pdf ########################
def splitPDF(input_dirPath, output_dirPath, interval=1):
    if not os.path.exists(output_dirPath):
        os.makedirs(output_dirPath)

    # 读取源pdf文件
    input = PdfFileReader(open(input_dirPath, "rb"))

    # 如果pdf文件已经加密，必须首先解密才能使用pyPdf
    if input.isEncrypted:
        input.decrypt("map")

    # 获得源pdf文件中页面总数
    pageCount = input.getNumPages()
    print(pageCount)

    # 分别将page添加到输出output中
    for iPage in range(1, pageCount + 1, interval):
        output = PdfFileWriter()
        save_dirPath = ""
        if iPage == pageCount:
            output.addPage(input.getPage(iPage - 1))
            save_dirPath = os.path.join(output_dirPath, str(iPage) + ".pdf")
        else:
            for i in range(interval):
                output.addPage(input.getPage(iPage - 1 + i))
                save_dirPath = os.path.join(output_dirPath, str(iPage) + "-" + str(iPage + interval - 1) + ".pdf")

        print("Current Pages Number:" + str(iPage) + "-" + str(iPage + interval - 1))
        # 最后写pdf文件
        outputStream = open(save_dirPath, "wb")
        output.write(outputStream)
        outputStream.close()
    print("finished")


if __name__ == '__main__':
    input_dirPath = input("请输入要删除的文件路径: ")
    interval = input("请输入每隔多少页拆分为一个新的pdf文件: ")
    output_dirPath = os.path.join(input_dirPath, "..", "output-" + str(interval))
    splitPDF(input_dirPath, output_dirPath, interval)

    time2 = time.time()
    print(u'总共耗时：' + str(time2 - time1) + 's')