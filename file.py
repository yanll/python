# coding=utf-8

import os
import time
import shutil
import exifread


def get_modified_time(file):
    return time.ctime(os.path.getmtime(file))


# 获取文件的时间
def getdate(filename):
    # 以二进制方式，打开指定的文件
    f = open(filename, 'rb')
    # 调用exifread来获取图片文件的exif信息
    data = exifread.process_file(f)
    DateTimeOriginal = ''
    ImageDateTime = ''
    ModifiedDateTime = ''
    if data:
        # 如果获取到data值，则进行下述相关操作
        try:
            # 获取EXIF DateTimeOriginal值，即为图片的创建时间
            t = data['EXIF DateTimeOriginal']
            if str(t).strip() != '':
                DateTimeOriginal = str(t).replace(":", "").replace(" ", "")
        except:
            try:
                t = data['Image DateTime']
                # 将获取到的时间进行格式转换，并仅保留年份和月份，然后返回
                if str(t).strip() != '':
                    ImageDateTime = str(t).replace(":", "").replace(" ", "")
            except:
                pass

    if DateTimeOriginal.strip() != '':
        # print ('返回拍摄日期\t' + DateTimeOriginal + '\t' + filename)
        return DateTimeOriginal

    state = os.stat(filename)
    ModifiedDateTime = time.strftime("%Y%m%d%H%M%S", time.localtime(state[-2]))

    if ImageDateTime.strip() == '':
        # print ('拍摄日期&照片日期为空返回修改日期\t' + ModifiedDateTime + '\t' + filename)
        return ModifiedDateTime

    if ImageDateTime <= ModifiedDateTime:
        # print ('照片日期小于修改日期返回照片日期\t' + ImageDateTime + '\t' + filename)
        return ImageDateTime
    else:
        # print ('修改日期小于照片日期返回修改日期\t' + str(t) + '\t' + filename)
        return ModifiedDateTime
    # print ('返回空值\t' + str(t) + '\t' + filename)
    return ''


# 照片分类整理函数
def classifyPictures(path, targetpath, filetype):
    if filetype not in ('image', 'video'):
        print '文件类型错误，结束任务'
        return ''
    if not os.path.exists(targetpath):
        os.mkdir(targetpath)
    # 利用os.walk获取目录下的文件夹和文件的名称及其目录路径
    for root, dirs, files in os.walk(path, True):
        for filename in files:
            # 获取文件的完整路径
            file = os.path.join(root, filename)
            # 获取文件的后缀名
            p, f = os.path.splitext(file)
            if filetype == 'image':
                if f.lower() not in ('.jpg', '.jpeg', '.png', '.bmp'):
                    continue
            if filetype == 'video':
                if f.lower() not in ('.mp4', '.mov', '.3gp'):
                    continue
            try:
                t = getdate(file)
                if t.strip() == '':
                    continue
                t = t[:4] + '年' + t[4:6] + '月'
            except Exception as e:
                print(e)
                continue
            moveDir = targetpath + '/' + t + ''
            mf = moveDir + '/' + filename
            src = root + '/' + filename
            if os.path.exists(mf):
                print '文件存在 ' + src + ' ' + mf
                continue

            print '移动文件 ' + src + ' ' + mf
            if not os.path.exists(moveDir):
                os.mkdir(moveDir)
            shutil.move(src, mf)


# 调用函数

classifyPictures('/Volumes/Metal/重复文件/', '/Volumes/Metal/成功照片', 'image')

# for path in [
#     '2011年01月', '2011年02月', '2011年03月', '2011年04月', '2011年05月', '2011年06月',
#     '2011年07月', '2011年08月', '2011年09月', '2011年10月', '2011年11月', '2011年12月',
#     '2012年01月', '2012年02月', '2012年03月', '2012年04月', '2012年05月', '2012年06月',
#     '2012年07月', '2012年08月', '2012年09月', '2012年10月', '2012年11月', '2012年12月',
#     '2013年01月', '2013年02月', '2013年03月', '2013年04月', '2013年05月', '2013年06月',
#     '2013年07月', '2013年08月', '2013年09月', '2013年10月', '2013年11月', '2013年12月',
#     '2014年01月', '2014年02月', '2014年03月', '2014年04月', '2014年05月', '2014年06月',
#     '2014年07月', '2014年08月', '2014年09月', '2014年10月', '2014年11月', '2014年12月',
#     '2015年01月', '2015年02月', '2015年03月', '2015年04月', '2015年05月', '2015年06月',
#     '2015年07月', '2015年08月', '2015年09月', '2015年10月', '2015年11月', '2015年12月',
#     '2016年01月', '2016年02月', '2016年03月', '2016年04月', '2016年05月', '2016年06月',
#     '2016年07月', '2016年08月', '2016年09月', '2016年10月', '2016年11月', '2016年12月',
#     '2017年01月', '2017年02月', '2017年03月', '2017年04月', '2017年05月', '2017年06月',
#     '2017年07月', '2017年08月', '2017年09月', '2017年10月', '2017年11月', '2017年12月',
#     '2018年01月', '2018年02月', '2018年03月', '2018年04月', '2018年05月', '2018年06月',
#     '2018年07月', '2018年08月', '2018年09月', '2018年10月', '2018年11月', '2018年12月',
#     '2019年01月', '2019年02月', '2019年03月', '2019年04月', '2019年05月', '2019年06月',
#     '2019年07月', '2019年08月', '2019年09月', '2019年10月', '2019年11月', '2019年12月',
#     '2020年01月', '2020年02月', '2020年03月', '2020年04月', '2020年05月', '2020年06月',
#     '2020年07月', '2020年08月', '2020年09月', '2020年10月', '2020年11月', '2020年12月',
#     '2021年01月', '2021年02月', '2021年03月', '2021年04月', '2021年05月', '2021年06月',
#     '2021年07月', '2021年08月', '2021年09月', '2021年10月', '2021年11月', '2021年12月',
#     '手机相册'
# ]:
#     classifyPictures('/Volumes/Metal/个人网盘/来自相册/' + path, '/Volumes/Metal/成功照片', 'image')
