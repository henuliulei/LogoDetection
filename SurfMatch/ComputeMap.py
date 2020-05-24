#计算特征提取算法在Flickrlogo数据集上的map值
logoList = ["google","apple","adidas","HP","stellaartois","paulaner","guiness","singha","cocacola","dhl","texaco",
            "fosters","fedex","aldi","chimay","shell","becks","tsingtao","ford","carlsberg","bmw","pepsi","esso","heineken",
            "erdinger","corona","milka","ferrari","nvidia","rittersport","ups","starbucks"]
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
def getGT(line):#获取groundtruth
    classname,picname = Spilt(line)
    maskpath = "D:\\PIC\\FlickrLogos-v2\\classes\\masks"
    path = maskpath + "\\" +classname + "\\" +  picname + ".bboxes.txt"
    f = open(path)
    f.readline()
    line = f.readline()
    xmin,ymin,xmax,ymax = getLoc2(line)
    return xmin,ymin,xmax,ymax
def getValue(line,line1):
    if len(line) <= 2:
        return 0
    else:
        a, b, c, d, e = getLoc1(line)
        # print(b,c,d,e)
        rect1 = [c, b, e, d]
        b1, c1, d1, e1 = getGT(line1)
        rect2 = [c1, b1, e1, d1]
        a = compute_iou(rect1, rect2)
        if a > 0.5:
            return 1
        else:
            return 0
def getIou():
    f = open("bbox.txt")
    f1 = open("D:\\PIC\\FlickrLogos-v2\\all.spaces.txt")
    f2 = open("bboxlogo.txt","w")
    line = f.readline()
    line1 = f1.readline()
    line.strip('\n')
    line1.strip('\n')
    num1 = 0
    while True:
        num1 += 1
        if(num1 == 2241):
            break
        a = getValue(line,line1)
        f2.write(str(a)+'\n')
        line = f.readline()
        line.strip('\n')
        line1 = f1.readline()
        line1.strip('\n')
def computeAp(list1,list2):
    listTP=[]
    listTN=[]
    listFP=[]
    listFN=[]
    listPre=[]
    listRec=[]
    Ap = 0
    for i in range(7):
        end = (i+1)*10
        listTP.append(sum(list1[0:end]))
        listFN.append(end-sum(list1[0:end]))
        listFP.append(sum(list2[0:end]))
        listTN.append(end-sum(list2[0:end]))
    for i in range(7):
        if listTP[i]+listFP[i] == 0:
            listPre.append(0)
        else:
            listPre.append(listTP[i] / (listTP[i] + listFP[i]))

        listRec.append(listTP[i]/70)
    for i in range(7):
        if i==0:
            Ap+=listRec[i]*listPre[i]
        else:
            Ap += listPre[i]*(listRec[i]-listRec[i-1])
    return Ap
def getMap():
    f = open("bboxlogo.txt")
    f1 = open("bboxnologo.txt")
    line = f.readline()
    line.strip('\n')
    line1 = f1.readline()
    line1.strip('\n')
    listAp = []
    num = -1
    list1 = []
    list2 = []
    while line:
        num += 1
        if(num == 2240):
            break
        if(num % 70 ==0):
            list1 = []
            list2 = []
        list1.append(int(line))
        if len(line1)> 2:
            list2.append(1)
        else:
            list2.append(0)
        if(num%70 == 69):
            listAp.append(computeAp(list1,list2))
        line = f.readline()
        line.strip('\n')
        line1 = f1.readline()
        line1.strip('\n')
    return listAp



if __name__ == '__main__':
   #getIou()
   list = []
   list = getMap()
   for i in range(len(list)):
       print(logoList[i]+"_AP:      "+str(list[i]))
   print("Map:      "+str(sum(getMap())/32))

