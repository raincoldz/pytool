# -*- coding:utf-8*-
import os
from PyPDF2 import PdfFileReader, PdfFileWriter
import zipfile


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


def deletePDF(input_dirPath, output_dirPath, delete_page):
    '''
    删除PDF文件中的指定页码
    '''
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


def splitPDF(input_dirPath, output_dirPath, interval=1):
    """
    将PDF文件每n页拆分为一个文件
    命名为 i-i+n-1.pdf
    """
    if not os.path.exists(output_dirPath):
        os.makedirs(output_dirPath)

    # 读取源pdf文件
    input = PdfFileReader(open(input_dirPath, "rb"))

    # 如果pdf文件已经加密，必须首先解密才能使用pyPdf
    if input.isEncrypted:
        input.decrypt("map")

    # 获得源pdf文件中页面总数
    pageCount = input.getNumPages()
    print("Total Pages: " + str(pageCount))

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
                save_dirPath = os.path.join(
                    output_dirPath,
                    str(iPage) + "-" + str(iPage + interval - 1) + ".pdf")

        print("Current Pages Number:" + str(iPage) + "-" +
              str(iPage + interval - 1))
        # 最后写pdf文件
        outputStream = open(save_dirPath, "wb")
        output.write(outputStream)
        outputStream.close()
    print("finished")


def zipDir(dirpath, outFullName):
    """
    压缩指定文件夹
    :param dirpath: 目标文件夹路径
    :param outFullName: 压缩文件保存路径+xxxx.zip
    :return: 无
    """
    zip = zipfile.ZipFile(outFullName, "w", zipfile.ZIP_DEFLATED)
    for path, dirnames, filenames in os.walk(dirpath):
        # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
        fpath = path.replace(dirpath, '')

        for filename in filenames:
            zip.write(os.path.join(path, filename),
                      os.path.join(fpath, filename))
    zip.close()


def makeCurWorkspace(curFileFolder):
    if not os.path.exists(curFileFolder):
        os.makedirs(curFileFolder)
    output_dirPath = os.path.join(curFileFolder, "output")
    if not os.path.exists(output_dirPath):
        os.makedirs(output_dirPath)


def makeZip(curFileFolder):
    uuid = curFileFolder.split("/")[-1]
    zipFileDirPath = os.path.join(curFileFolder, "..", uuid + ".zip")
    zipDir(curFileFolder, zipFileDirPath)