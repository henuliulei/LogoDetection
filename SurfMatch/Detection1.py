#对Topslogos数据集进行检测，并把中间结果输出到对应文件里面
# coding=utf-8
import cv2
import scipy as sp
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
#添加高斯噪声函数
ListName = ['adidas0','chanel','Gucci','HH','lacoste','MK','nike','prada','puma','supreme']
originjpgData = "D:\\PIC\\qmul_toplogo10\\jpg\\"
originmasksData = "D:\\PIC\\qmul_toplogo10\\masks\\"
newQueryData = "D:\\PIC\\qmul_toplogo10\\query\\"
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
        if m.distance < 0.8 * n.distance:
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
    if len(good) >= 5:
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
        #cv2.putText(view, "logo detected", (w1 + 10, 100), cv2.FONT_HERSHEY_COMPLEX, 1.0, (100, 50, 200), 3)
        #cv2.imshow("img",view)
        #cv2.waitKey(0)
    else:
        cv2.putText(view, "no logo detected", (w1 + 10, 100), cv2.FONT_HERSHEY_COMPLEX, 1.0, (100, 200, 200), 3)
        return 0

def detectShow(path1,path2):
    img1 = cv2.imread(path1, 0)  # queryImage
    img2 = cv2.imread(path2, 0)  # trainImage

    img2 = gasuss_noise(img2, 0, 0.001)  # 加入高斯噪声
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
        if m.distance < 0.8 * n.distance:
            good.append(m)
    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]
    view = img2
    num = 0;
    if len(good) >= 5:
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

if __name__ == '__main__':
    #Detect("D:\\PIC\\qmul_toplogo10\\query\\adidas0\\adidas1.jpg","D:\\PIC\\qmul_toplogo10\\jpg\\adidas0\\adidas1.jpg")

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
        f1.write(str(Detect(src, dst)) + '\n')
        line = f.readline()
        line = line.strip("\n")
    f.close()
    f1.close()




