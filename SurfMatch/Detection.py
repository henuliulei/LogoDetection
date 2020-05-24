#对Flickrlogos数据集进行检测，并把中间结果输出到对应文件里面
# coding=utf-8
import cv2
import scipy as sp
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
#添加高斯噪声函数

def gasuss_noise(image, mean=0, var=0.001):
  image = np.array(image/255, dtype=float)
  noise = np.random.normal(mean, var ** 0.5, image.shape)
  out = image + noise
  if out.min() < 0:
    low_clip = -1.
  else:
    low_clip = 0.
  out = np.clip(out, low_clip, 1.0)
  out = np.uint8(out*255)
  #cv.imshow("gasuss", out)
  return out
def Resize(img1,r):
    width, height = img1.shape[:2]
    #print(img1.shape, width, height)
    dstwidth = int(width * r)
    dstheight = int(height * r)
    img1 = cv2.resize(img1, (dstheight, dstwidth))
    return img1

def Detect(path1,path2):
    img1 = cv2.imread(path1, 0)  # queryImage
    img2 = cv2.imread(path2, 0)  # trainImage
    #plt.imshow(img2)
    #plt.show()
    img2 = gasuss_noise(img2, 0, 0.002)  # 加入高斯噪声
    #plt.imshow(img2)
    #plt.show()

    img1 = Resize(img1,1.2)
    # Initiate SIFT detector
    surf = cv2.xfeatures2d_SURF.create()
    # find the keypoints and descriptors with SUFT
    kp1, des1 = surf.detectAndCompute(img1, None)
    kp2, des2 = surf.detectAndCompute(img2, None)

    # FLANN parameters
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)  # or pass empty dictionary
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)
    #print('matches...', len(matches))
    # Apply ratio test
    good = []
    for m, n in matches:
        if m.distance < 0.6 * n.distance:
            good.append(m)
   # print('good', len(good))
    # #####################################
    # visualization
    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]
    view = sp.zeros((max(h1, h2), w1 + w2, 3), sp.uint8)
    view[:h1, :w1, 0] = img1
    view[:h2, w1:, 0] = img2
    view[:, :, 1] = view[:, :, 0]
    view[:, :, 2] = view[:, :, 0]
    num = 0;
    if len(good) >= 8:
        for m in good:
            num += 1
            #print(m.trainIdx)
            # draw the keypoints
            # print m.queryIdx, m.trainIdx, m.distance
            color = tuple([sp.random.randint(0, 255) for _ in range(3)])
            # print 'kp1,kp2',kp1,kp2
            #cv2.line(view, (int(kp1[m.queryIdx].pt[0]), int(kp1[m.queryIdx].pt[1])),
             #        (int(kp2[m.trainIdx].pt[0] + w1), int(kp2[m.trainIdx].pt[1])), color)
            if num == 1:
                xmin = int(kp2[m.trainIdx].pt[0] + w1)
                ymin = int(kp2[m.trainIdx].pt[1])
                xmax = int(kp2[m.trainIdx].pt[0] + w1)
                ymax = int(kp2[m.trainIdx].pt[1])
            else:
                if int(kp2[m.trainIdx].pt[0] + w1) < xmin:
                    xmin = int(kp2[m.trainIdx].pt[0] + w1)
                if int(kp2[m.trainIdx].pt[0] + w1) > xmax:
                    xmax = int(kp2[m.trainIdx].pt[0] + w1)
                if int(kp2[m.trainIdx].pt[1]) < ymin:
                    ymin = int(kp2[m.trainIdx].pt[1])
                if int(kp2[m.trainIdx].pt[1]) > ymax:
                    ymax = int(kp2[m.trainIdx].pt[1])
        cv2.rectangle(view, (xmin, ymin), (xmax, ymax), (0, 0, 255), 2)
        return 1,xmin - w1, ymin, xmax - w1, ymax
        cv2.putText(view, "logo detected", (w1 + 10, 100), cv2.FONT_HERSHEY_COMPLEX, 1.0, (100, 50, 200), 3)
    else:
        cv2.putText(view, "no logo detected", (w1 + 10, 100), cv2.FONT_HERSHEY_COMPLEX, 1.0, (100, 200, 200), 3)
        return 0

def detectShow(path1,path2):
    img1 = cv2.imread(path1, 0)  # queryImage
    img2 = cv2.imread(path2, 0)  # trainImage

    img2 = gasuss_noise(img2, 0, 0.002)  # 加入高斯噪声
    img1 = Resize(img1, 1.2)
    surf = cv2.xfeatures2d_SURF.create()
    kp1, des1 = surf.detectAndCompute(img1, None)
    kp2, des2 = surf.detectAndCompute(img2, None)

    # FLANN parameters
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)  # or pass empty dictionary
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)
    # print('matches...', len(matches))
    # Apply ratio test
    good = []
    for m, n in matches:
        if m.distance < 0.6 * n.distance:
            good.append(m)
    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]
    view = img2
    num = 0;
    if len(good) >= 8:
        for m in good:
            num += 1
            color = tuple([sp.random.randint(0, 255) for _ in range(3)])
            if num == 1:
                xmin = int(kp2[m.trainIdx].pt[0] + w1)
                ymin = int(kp2[m.trainIdx].pt[1])
                xmax = int(kp2[m.trainIdx].pt[0] + w1)
                ymax = int(kp2[m.trainIdx].pt[1])
            else:
                if int(kp2[m.trainIdx].pt[0] + w1) < xmin:
                    xmin = int(kp2[m.trainIdx].pt[0] + w1)
                if int(kp2[m.trainIdx].pt[0] + w1) > xmax:
                    xmax = int(kp2[m.trainIdx].pt[0] + w1)
                if int(kp2[m.trainIdx].pt[1]) < ymin:
                    ymin = int(kp2[m.trainIdx].pt[1])
                if int(kp2[m.trainIdx].pt[1]) > ymax:
                    ymax = int(kp2[m.trainIdx].pt[1])
        return xmin-w1,ymin,xmax-w1,ymax,h2,w2
        #cv2.rectangle(view, (xmin, ymin), (xmax, ymax), (0, 0, 255), 2)
        #cv2.putText(view, "logo detected", (w1 + 10, 100), cv2.FONT_HERSHEY_COMPLEX, 1.0, (100, 50, 200), 3)
        #print(view.shape)
        #return view
    else:
        return -1,-1,-1,-1,-1,-1

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
if __name__ == '__main__':
    path = "D:\\PIC\\FlickrLogos-v2\\all.spaces.txt"
    QueryPath = "D:/PIC/NewData/Query/"
    TargetPath = "D:/PIC/NewData/Target/"
    f = open(path)
    line = f.readline()
    num = 0
    f1 = open('bbox.txt', 'w')
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
        f1.write(str(Detect(src, dst)) + '\n')
        line = f.readline()
    f.close()
    f1.close()



