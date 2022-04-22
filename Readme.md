# Readme

本函数实现功能：

将文件夹下/input目录的所有图片读入为灰度图，按已经定义的
wrate：窗口比原图宽的1/N，输入N
hrate：窗口比原图高的1/M,输入M
grate：灰度阈值倍率，微调框图效果
Layer：分解子图层数，越大分解越细，越能精准勾勒轮廓，但耗时增加，一般3-5即可
框出图符合条件的子图集，从而找出素描主体，本输出矩形框图一幅，取子图集内最左上与最右下输出矩形结果图，为检验准确，以绿框描出最终的子图集查看

## GreyDepartCommon.py

### 子图类 sub_graph

```python
class sub_graph:#子图类
       x=0 #图左上角顶点x轴坐标
       y=0#图左上角顶点y轴坐标
       height=0#图高
       width=0#图宽
       Link=0#联通标志，1则子图联通，0则无
       GreyScale=0#用来判断是否越过灰度锁被录用，1则通过，0则无
       def _init_(self):
        self.x=0
        self.y=0
        self.height=0
        self.width=0
        self.Link=0
        self.GreyScale=0
                                                        
       def _setGraph_(self,x,y,width,height):#设置子图参数
        self.x=x
        self.y=y
        self.height=height
        self.width=width
        
       def graphInfo(self):
        print("("+str(self.x) + ","+str(self.y)+")"+"The width and height of the picture:"+str(self.width)+" "+str(self.height)+"."+"GreyScale: "+str(self.GreyScale))#子图信息输出


```



### 通用函数类pic_common

**calGreyAvenge**(self,image,GreyScaleLock,ImageSource):计算子图类对象image记录的子图的平均灰度。

<u>GreyScaleLock</u>：灰度阈值，用来之后子图灰度标杆的比较

<u>ImageSource</u>：图源，未被分割的整图

**sliding_window**(self,start_x,start_y,image, stepSize, windowSize,ImageSource):

从（start_x,start_y）这一顶点开始依据步长stepsize以及窗口长windowsize划动划分窗口

**get_slice**(self,start_x,start_y,image, stepSize, windowSize,ImageSource,GreyScaleLock,calgreyfunction)：从（start_x,start_y）这一顶点开始，子图集内每一张子图以calgreyfunction计算出的灰度指标为指标，通过GreyScaleLock灰度锁筛选的图片则被传入子图集作为输出。

<u>calgreyfunction</u>：用来计算灰度指标的函数，自定义，一般传参格式为(image,GreyScaleLock,ImageSource)，把越过灰度锁的子图类中GreyScale标记为1

**saveImageList**(self,imagelist,ImageSource,picname,outputPath)：把imagelist内的子图储存到outputPath文件夹内

<u>picname</u>：文件名

默认储存格式：after_原图文件名（包括后缀）

**draw_rectangle_by_point**(self,image,ImageSource):给子图画框，可视化用

**FindOneInList**(self,imagelist,x,y)：检测坐标为x，y的子图在当前尺度下的imagelist子图集内是否存在

**searchLink**(self,imagelist,image)：判断子图image是否联通，并更改子图的link标记

**deleteNonLink**(self,imagelist):删除imagelist内非联通状态的子图

**greylockFunction**(self,image,grate)：计算并输出灰度锁指标

<u>grate</u>：灰度阈值倍率，若取图源平均值作为灰度锁，则一般grate=1.005

**readIntoList**(self,picpath,wrate,hrate,grate,greylockFunction)输出一张图的初次分割子图集

picpath：图源的文件路径

greylockFunction：计算灰度阈值函数

## depart.py

### 筛选函数类pic_select



```python
 def _init_(select_function_new,transfer_new):#改变按层数迭代的方法/改变输出转换子图的方法
	 self.selectByLayer=select_function_new
	 self.transFer=transfer_new
 def rebuildSelect(select_function_new):#改变按层数迭代的方法
	 self.selectByLayer=select_function_new
 def rebuildTransfer(transfer_new):#改变输出转换子图的方法
	 self.transFer=transfer_new
```

**selectByLayer**(self,imagelist,layer,wrate,hrate,ImageSource,GreyScaleLock):#按迭代层数layer进行layer次选择,输出一个划分好的子图集

**transFer**(self,inputpath,wrate,hrate,grate,layer,outputpath,selectfunction,lockfunction)

输入参数：要转换的文件夹路径，宽比，高比，灰度阈值倍率，分解子图层数,输出目录,层筛选函数，灰度锁函数

## 命令行使用

参数：

'**--input**',type=str,default='input/',help='where the path pictures wanted to be traned,要转换的文件夹路径')
'**--wrate**',type=int,default=5,help='how many pieces the width would be departed,宽比')
'**--hrate**',type=int,default=5,help='how many pieces the height would be departed,高比')
'**--grate**',type=float,default=1.005,help='the rate geryscale would plus,influences the greyloak and the departture,灰度阈值倍率')
'**--layer**',type=int,default=3,help='how mant times the subgraphs would be departed into subgraphsets,分解子图层数')
'**--output**',type=str,default='output/',help='where the path pictures wanted to be outlist,输出目录'

标准使用：

python depart.py --input input/ --wrate 5 --hrate 5 --grate 1.005 --layer 3   --output output/