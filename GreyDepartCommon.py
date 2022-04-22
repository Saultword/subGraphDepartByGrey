import math
import numpy as np
import cv2

class sub_graph:#子图类
       x=0 #图左上角顶点x轴坐标
       y=0#图左上角顶点y轴坐标
       height=0#图高
       width=0#图宽
       Link=0#联通标志
       GreyScale=0#判断是否越过灰度锁被录用
       def _init_(self):
        self.x=0
        self.y=0
        self.height=0
        self.width=0
        self.Link=0
        self.GreyScale=0
                                                        
       def _setGraph_(self,x,y,width,height):
        self.x=x
        self.y=y
        self.height=height
        self.width=width
        
       def graphInfo(self):
        print("("+str(self.x) + ","+str(self.y)+")"+"The width and height of the picture:"+str(self.width)+" "+str(self.height)+"."+"GreyScale: "+str(self.GreyScale))#子图信息输出



class pic_common:#一些通用函数
 @classmethod
 def calGreyAvenge(self,image,GreyScaleLock,ImageSource):#计算图平均灰度,当前函数内，平均灰度在灰度锁这一衡量标准之下的子图被淘汰
    greyscale=0
    if np.mean(ImageSource[image.y:image.y + image.height, image.x:image.x + image.width])<=GreyScaleLock:
        image.GreyScale=1
    else:
        image.GreyScale=0
    return image


#以下2函数作为滑动分割使用
 @classmethod
 def sliding_window(self,start_x,start_y,image, stepSize, windowSize,ImageSource):#滑动帧划分
    # slide a window across the image
    for y in range(start_y, image.height+start_y, stepSize[1]):
        for x in range(start_x, image.width+start_x, stepSize[0]):
            # yield the current window
            yield (x, y, ImageSource[y:y + windowSize[1], x:x + windowSize[0]])
 @classmethod
 def get_slice(self,start_x,start_y,image, stepSize, windowSize,ImageSource,GreyScaleLock,calgreyfunction):
    slice_sets = []
    
    for (x, y, window) in self.sliding_window(start_x,start_y,image, stepSize, windowSize,ImageSource):
        
        # if the window does not meet our desired window size, ignore it
        if window.shape[0] != windowSize[1] or window.shape[1] != windowSize[0]:
            continue
        p1=sub_graph()
        p1._setGraph_(x,y,windowSize[0],windowSize[1])
        p1=calgreyfunction(p1,GreyScaleLock,ImageSource)#灰度迭代                     
        if p1.GreyScale == 1:
         slice_sets.append(p1)#超过灰度锁则录入
    slice_sets=self.deleteNonLink(slice_sets)#检查联通
    return slice_sets

 @classmethod
 def saveImageList(self,imagelist,ImageSource,picname,outputPath):#保存子图列表内图片，可扩展性不强
    if imagelist==None:
      print("None image limited")
      exit()
    t=0
    outputImage=ImageSource
    
    for i in imagelist:
        outputImage=self.draw_rectangle_by_point(i,outputImage)
    cv2.imwrite(outputPath+"after_"+picname, outputImage)    #保存参数
 @classmethod
 def draw_rectangle_by_point(self,image,ImageSource):#画框函数，可扩展性不强，用于子图集可视化
    image2 = ImageSource
    point=[image.x,image.y,image.x+image.width,image.y+image.height]#左上右下的点集
    first_point=(int(point[0]),int(point[1]))#左上坐标
    last_point=(int(point[2]),int(point[3]))#右下坐标

        # first_point = (point[0] * 2, point[1] * 2)
        # last_point = (point[2]* 2, point[3] * 2)
    
    cv2.rectangle(image2, first_point, last_point, (0, 255, 0), 1)#在图片上进行绘制框
    #cv2.putText(image2, '('+str(image.x)+','+str(image.y)+')', first_point, cv2.FONT_HERSHEY_COMPLEX, fontScale=0.5, color=(255,0,0), thickness=1)#在矩形框上方绘制该框的名
    
    return image2
 @classmethod
 def FindOneInList(self,imagelist,x,y):#find a subgraph in imagelist 
    
    for i in imagelist:#检测该坐标的子图是否在子图集内，或可修改为传入子图对象
        if i.x==x and i.y==y:
            return 1
    return 0
 @classmethod
 def searchLink(self,imagelist,image):#判断子图们是否联通
    image.Link=0
    ix=image.x
    iw=image.width
    ih=image.height
    iy=image.y
    if self.FindOneInList(imagelist,ix-iw,iy)==1 or self.FindOneInList(imagelist,ix+iw,iy)==1 or self.FindOneInList(imagelist,ix,iy+ih)==1 or self.FindOneInList(imagelist,ix,iy-ih)==1:#上下四方是否有联通
        image.Link=1
    return image.Link
 @classmethod
 def deleteNonLink(self,imagelist):#删除非联通的子图
    list1=imagelist
    for i in list1:
        if(self.searchLink(list1,i)==0):
            imagelist.remove(i)
    return imagelist
 @classmethod
 def greylockFunction(self,image,grate):#该函数用于计算灰度锁，读入图像和灰度倍率
    GreyScaleLock=np.mean(image)*(grate)
    return GreyScaleLock
 @classmethod
 def readIntoList(self,picpath,wrate,hrate,grate,lockFunction):#文件路径，wrate，hrate，grate，灰度锁计算函数，输出一张图的初次分割子图集
        common=pic_common
        temp = cv2.imread(picpath)
        timage=cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)#转换灰度图
        width=timage.shape[1]#图宽
        height=timage.shape[0]#图高
        image=timage
        greylock=lockFunction(image,grate)
        fw=image.shape[1]/wrate#帧宽
        fh=image.shape[0]/hrate#帧高
        windowsize=[int(fw),int(fh)]#窗口大小
        imagetest=sub_graph()
        imagetest._setGraph_(0,0,image.shape[1],image.shape[0])
        outputlist=common.get_slice(0,0,imagetest,windowsize,windowsize,image,greylock,common.calGreyAvenge)

        return outputlist
