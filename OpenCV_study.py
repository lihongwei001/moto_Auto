import cv2 as cv
import numpy as np
import os

def main():
    img = cv.imread ( 'messi5.jpg' )
    assert img is  not  None , "文件无法读取，请使用 os.path.exists() 检查"
    print('图像的属性为：', img.shape )
    print('图像的像素总数为：', img.size )
    print('图像的数据类型为：', img.dtype )


if __name__ == '__main__':
    main()