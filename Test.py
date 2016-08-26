#coding: utf-8
#
# @note: 这里两张照片层叠选择的方法是：
#   假设两张照片的同一点的像素分别为A，B，则层叠之后该点得像素为(alpha取值在0和1之间)：
#       A * alpha + B * (1-alpha)
#
from __future__ import division
import PIL
import Image
import numpy
import os
import random
import numexpr
import time
import ImageFont,ImageDraw

STAG = time.time()

root = os.getcwd()+"/"
W_num = 13
H_num = 13
W_size = 640
H_size = 360

# aval 存放所有的照片
aval = []
alpha = 0.4

# name: treansfer
# todo: 将照片转为一样的大小
def transfer(img_path,dst_width,dst_height):
    im = Image.open(img_path)
    print "----%s"%im.mode
    if im.mode != "RGBA":
        im = im.convert("RGBA")
        print "----%s" % im.mode

    s_w,s_h = im.size
    if s_w < s_h:
        im = im.rotate(90)

    STA = time.time()
    resized_img = im.resize((dst_width,dst_height))
    print "Transfer Func Time %s"%(time.time()-STA)
    return numpy.array(resized_img)[:dst_height,:dst_width]

# name: getAllPhtots
# todo: 获得所有照片的路径
def getAllPhotos():
    src = root+"photos/"
    for i in os.listdir(src):
        if os.path.splitext(src+i)[-1] == ".png":
            aval.append(src+i)

# name: createNevImg
# todo: 创造一张新的图片，并保存
def createNewImg():
    iW_size = W_num * W_size
    iH_size = W_num * H_size
    print "路径为%s"%root+"lyf.png"
    I = transfer((root+"hansa.png"), iW_size, iH_size)
    I = numexpr.evaluate("""I*(1-alpha)""")

    for i in range(W_num):
        for j in range(H_num):
            SH = I[(j*H_size):((j+1)*H_size), (i*W_size):((i+1)*W_size)]
            STA = time.time()
            DA = transfer(random.choice(aval),W_size, H_size)
            print "Cal Func Time %s"%(time.time()-STA)
            res = numexpr.evaluate("""SH+DA*alpha""")
            I[(j*H_size):((j+1)*H_size), (i*W_size):((i+1)*W_size)] = res

    Image.fromarray(I.astype(numpy.uint8)).save("CreateNewImg_%s.png"%alpha)

# name: newRotateImage
# todo: 将createnewimg中得到的照片旋转，粘贴到另外一张照片中
def newRotateImage():
    imName = "CreateNewImg_%s_heheda.png"%alpha
    print "正在将图片旋转中..."
    im = Image.open(imName)
    im2 = Image.new("RGBA", (W_size * int(W_num + 1), H_size *(H_num + 4)))
    im2.paste(im, (int(0.5 * W_size), int(0.8 * H_size)))
    im2 = im2.rotate(359)
    im2.save("newRotateImage_%s_heheda.png"%alpha)

# name: writetoimage
# todo: 在图片中写祝福语
def writeToImage():
    print "正在向图片添加汉字..."
    img = Image.open("newRotateImage_%s_heheda.png"%alpha)
    font = ImageFont.truetype('xindexingcao57.ttf',600)
    draw = ImageDraw.Draw(img)
    draw.ink = 21 + 118*256 +65*259*256

    tHeight = H_num +1
    draw.text((W_size * 0.5, H_size * tHeight), "Hansa written by Dev")

# name:
# todo: 入口函数
if __name__ == "__main__":
    getAllPhotos()
    createNewImg()
    newRotateImage()
    writeToImage()
    print "总用时%s"%(time.time()-STAG)