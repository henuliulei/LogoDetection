#裁剪Flickrlogo数据集获取查询图像
from PIL import Image
originjpgData = "D:/PIC/FlickrLogos-v2/classes/jpg/"
originmasksData = "D:/PIC/FlickrLogos-v2/classes/masks/"

newQueryData = "D:/PIC/NewData/Query/"
newTargetData = "D:/PIC/NewData/Target/"
import os
import shutil
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

#读取all.space.txt里面的图片，并复制到新路径里面
def readPicture(path):

    f = open(path)
    line = f.readline()
    num = 0
    while line:
        num+=1
        print(num)
        if num == 41:
            print("复制完成")
            break
        className = ""
        picName = ""
        #切分为类名和图片名
        className , picName = Spilt(line)
        src = originjpgData + className + "/" + picName
        dst = newTargetData + className + "/" + picName
        if className == "no-logo":
            continue
        if os.path.exists(os.path.join(newTargetData+className)):
            shutil.copy(src,dst)
        else:
            os.makedirs(os.path.join(newTargetData,className))
            shutil.copy(src,dst)
        line = f.readline()

    f.close()

#获取masks里面box的坐标位置
def getLocation(line):
    x = " "
    y = " "
    width = " "
    height = " "
    flag = 0
    for i in line:
        if i==" ":
            flag += 1
        if flag == 0 and i!=" ":
            x += i
        if flag == 1 and i != " ":
            y += i
        if flag == 2 and i != " ":
            width += i
        if flag == 3 and i != " ":
            height += i
    return x,y,width,height


#根据标注框box裁剪要查询的图片并输出到新文件夹里面
def CropPic(path):
    f = open(path)
    line = f.readline()
    num = 0
    while line:
        num += 1
        print(num)
        if num == 8241:
            print("裁剪完成")
            break
        className = ""
        picName = ""
        # 切分为类名和图片名
        className, picName = Spilt(line)
        src = originjpgData + className + "/" + picName
        src1 = originmasksData + className + "/" +picName+".bboxes.txt"
        if className == "no-logo":
            continue
        f1 = open(src1)
        f1.readline()
        f1 = f1.readline()
        x,y,width,height = getLocation(f1)
        x = int(x)
        y = int(y)
        width = int(width)
        height = int(height)
        dst = newQueryData + className + "/" + picName
        if os.path.exists(os.path.join(newQueryData + className)):
            im = Image.open(src)
            x1 = x + width
            y1 = y + height
            region = im.crop((int(x), int(y), int(x1), int(y1)))
            region.save(dst)
        else:
            os.makedirs(os.path.join(newQueryData, className))
            im = Image.open(src)
            x1 = x + width
            y1 = y + height
            region = im.crop((int(x), int(y), int(x1), int(y1)))
            region.save(dst)
        line = f.readline()

    f.close()




if __name__ == '__main__':
    #className,picName = Spilt("google 462663740.jpg")
    #print(className,picName)
    readPicture("D:\\PIC\\FlickrLogos-v2\\all.spaces.txt")#复制target
    #print(getLocation("123 33 43 22"))
    CropPic("D:\\PIC\\FlickrLogos-v2\\all.spaces.txt")#裁剪并保存query



