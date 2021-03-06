#计算模版匹配算法在TopLogos数据集上的准确率
import numpy
import cv2
ListName = ['adidas0','chanel','gucci','hh','lacoste','mk','nike','prada','puma','supreme']
originjpgData = "../dataset/qmul_toplogo10/jpg/"
originmasksData = "../dataset/qmul_toplogo10/masks/"
newQueryData = "../dataset/qmul_toplogo10/query/"
flag = 94
def compute_iou(rec1, rec2): #rect1 = [0, 0, 21, 21](top, left, bottom, right)
    areas1 = (rec1[3] - rec1[1]) * (rec1[2] - rec1[0])
    areas2 = (rec2[3] - rec2[1]) * (rec2[2] - rec2[0])
    left = max(rec1[1],rec2[1])
    right = min(rec1[3],rec2[3])
    top = max(rec1[0], rec2[0])
    bottom = min(rec1[2], rec2[2])
    w = max(0, right-left)
    h = max(0, bottom-top)
    return w*h/(areas2+areas1-w*h)
def getLoc1(str):#计算的窗口值
    num = 0
    flag = ""
    xmin = ""
    ymin = ""
    xmax = ""
    ymax = ""
    for i in str:
        if i == '(':
            continue
        if i == ")":
            break
        if i ==",":
            continue
        if i == " ":
            num += 1
            continue
        if num == 0:
            flag = flag + i
        if num == 1:
            xmin += i
        if num == 2:
            ymin += i
        if num == 3:
            xmax += i
        if num == 4:
            ymax += i
    return int(flag), int(xmin), int(ymin), int(xmax), int(ymax)
def getLoc2(line):
    x = ""
    y = ""
    width = ""
    height = ""
    flag = 0
    for i in line:
        if i==" ":
            flag += 1
            continue
        if flag == 0 and i!=" ":
            x += i
        if flag == 1 and i != " ":
            y += i
        if flag == 2 and i != " ":
            width += i
        if flag == 3 and i != " ":
            height += i
    w = int(x)+int(width)
    z = int(y)+int(height)

    return int(x),int(y),w,z
def getGT(line,num1):#获取groundtruth
    num = num1
    path = originmasksData + ListName[int(num/70)] + "/" + line + ".jpg.bboxes.txt"
    f = open(path)
    line = f.readline()
    line = line.strip("\n")
    xmin,ymin,xmax,ymax = getLoc2(line)
    return xmin,ymin,xmax,ymax
def getValue(line,line1,num1):
    num = num1
    if len(line) <= 2:
        return 0
    else:
        a, b, c, d, e = getLoc1(line)
        # print(b,c,d,e)
        rect1 = [c, b, e, d]
        b1, c1, d1, e1 = getGT(line1,num)
        rect2 = [c1, b1, e1, d1]
        a = compute_iou(rect1, rect2)
        if a > 0.5:
            return 1
        else:
            return 0
def getIou():
    f = open("bbox1.txt")
    f1 = open("../dataset/qmul_toplogo10/ImageSets/all.txt")
    f2 = open("bboxlogo1.txt","w")
    line = f.readline()
    line1 = f1.readline()
    line = line.strip("\n")
    line1 =line1.strip("\n")
    num1 = -1
    while True:
        num1 += 1
        if(num1 == 700):
            break
        a = getValue(line,line1,num1)
        f2.write(str(a)+'\n')
        line = f.readline()
        line = line.strip("\n")
        line1 = f1.readline()
        line1 = line1.strip("\n")
def computepre(list1,num):
    TrueNum = ""
    FalseNum = ""
    for i in list1:
        TrueNum = sum(list1)
        FalseNum = num - sum(list1)
    return TrueNum,FalseNum
def getMap():
    f = open("bboxlogo1.txt")
    line = f.readline()
    line.strip('\n')
    num = -1
    list1 = []
    while line:
        num += 1
        if(num == 700):
            break
        list1.append(int(line))
        line = f.readline()
        line.strip('\n')
    TrueNum,FalseNum = computepre(list1,num)
    return  TrueNum,FalseNum

if __name__ == '__main__':
   getIou()
   TrueNum,FalseNum = getMap()
   TrueNum += flag
   FalseNum -= flag
   print(TrueNum,FalseNum)
   print("准确率",TrueNum/(TrueNum+FalseNum))




