#用模版匹配算法在两个数据集上进行检测，并把中间结果输出到相应的文件里面
import cv2 as cv
import numpy as np
ListName = ['adidas0','chanel','Gucci','HH','lacoste','MK','nike','prada','puma','supreme']
originjpgData = "D:\\PIC\\qmul_toplogo10\\jpg\\"
originmasksData = "D:\\PIC\\qmul_toplogo10\\masks\\"
newQueryData = "D:\\PIC\\qmul_toplogo10\\query\\"
#切分类名和图片名
def Spilt(line):
    className=""
    picName=""
    flag = 0
    for i in line:
        #print(i)
        if i!=" " and flag==0:
            className += i
        elif i==" " and flag==0:
            flag=1
        elif i!=" " and flag==1 and i!='\n':
            picName += i
    return className,picName
def template_image(path1,path2):
    tpl = cv.imread(path1)
    tpl =  cv.resize(tpl, (0, 0), fx=0.85, fy=0.85, interpolation=cv.INTER_CUBIC)
    target = cv.imread(path2)
    #cv.imshow("modul", tpl)
    #cv.imshow("yuan", target)
    methods = [cv.TM_SQDIFF_NORMED]
    th, tw = tpl.shape[:2]
    for md in methods:
        result = cv.matchTemplate(target, tpl, md)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        tl = min_loc
        #print(tl)
        br = (tl[0] + tw, tl[1] + th)
        #print(br)
        #cv.rectangle(target, tl, br, [100, 0, 100],5)
       # cv.imshow("传统目标检测算法模板匹配算法" + np.str(md), target)
        #cv.waitKey(0)
        return 1,tl[0],tl[1],br[0],br[1]
def FlickrLogos32():
    path = "D:\\PIC\\FlickrLogos-v2\\all.spaces.txt"
    QueryPath = "D:/PIC/NewData/Query/"
    TargetPath = "D:/PIC/NewData/Target/"
    f = open(path)
    line = f.readline()
    num = 0
    f1 = open('bbox2.txt', 'w')
    while line:
        num += 1
        print(num)
        if num == 8241:
            print("完成")
            break
        className = ""
        picName = ""
        # 切分为类名和图片名
        className, picName = Spilt(line)
        src = QueryPath + className + "/" + picName
        dst = TargetPath + className + "/" + picName
        if className == "no-logo":
            continue
        f1.write(str(template_image(src, dst)) + '\n')
        line = f.readline()
    f.close()
    f1.close()
def Toplogos10():
    path = "D:\\PIC\\qmul_toplogo10\\ImageSets\\all.txt"
    f = open(path)
    line = f.readline()
    line = line.strip("\n")
    num = -1
    f1 = open('bbox1.txt', 'w')
    while line:
        num += 1
        print(num)
        if num == 700:
            print("完成")
            break
        className = ""
        picName = ""
        # 切分为类名和图片名
        src = newQueryData + ListName[int(num / 70)] + "\\" + line + ".jpg"
        dst = originjpgData + ListName[int(num / 70)] + "\\" + line + ".jpg"
        f1.write(str(template_image(src, dst)) + '\n')
        line = f.readline()
        line = line.strip("\n")
    f.close()
    f1.close()
if __name__ == '__main__':
   #FlickrLogos32()
   Toplogos10()

