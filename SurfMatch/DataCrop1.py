#裁剪Toplogo数据集获取查询图像
from PIL import Image
import os
ListName = ['adidas0','chanel','gucci','hh','lacoste','mk','nike','prada','puma','supreme']
originjpgData = "D:\\PIC\\qmul_toplogo10\\jpg\\"
originmasksData = "D:\\PIC\\qmul_toplogo10\\masks\\"
newQueryData = "D:\\PIC\\qmul_toplogo10\\query\\"

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
    line = line.strip("\n")
    num = -1
    while line:
        num += 1
        print(num)
        if num == 700:
            print("裁剪完成")
            break

        # 切分为类名和图片名
        src = originjpgData +ListName[int(num/70)] + "\\" + line + ".jpg"
        src1 = originmasksData + ListName[int(num/70)] + "\\" + line + ".jpg.bboxes.txt"
        f1 = open(src1)
        f1 = f1.readline()
        x,y,width,height = getLocation(f1)
        x = int(x)
        y = int(y)
        width = int(width)
        height = int(height)
        dst = newQueryData + ListName[int(num/70)] + "\\" + line + ".jpg"
        if os.path.exists(os.path.join(newQueryData + ListName[int(num/70)])):
            im = Image.open(src)
            x1 = x + width
            y1 = y + height
            region = im.crop((int(x), int(y), int(x1), int(y1)))
            region = region.convert('RGB')
            region.save(dst)
        else:
            os.makedirs(os.path.join(newQueryData + ListName[int(num/70)]))
            im = Image.open(src)
            x1 = x + width
            y1 = y + height
            region = im.crop((int(x), int(y), int(x1), int(y1)))
            region.save(dst)
        line = f.readline()
        line = line.strip("\n")
    f.close()
if __name__ == '__main__':
    CropPic("D:\\PIC\\qmul_toplogo10\\ImageSets\\all.txt")#裁剪并保存query



