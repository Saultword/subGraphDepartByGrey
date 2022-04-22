#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Graph_Color_Slices.py
#  
#  Copyright 2022 Lenovo <Lenovo@DESKTOP-MIKIRGF>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

#Ver5.0：更新可扩展，支持传入自定义灰度筛选函数使用，支持自定义
from GreyDepartCommon import pic_common,sub_graph
import math
import argparse
import cv2
import os
class pic_select:#重要的筛选函数
	
 def _init_(select_function_new,transfer_new):#改变按层数迭代的方法/改变输出转换子图的方法
	 self.selectByLayer=select_function_new
	 self.transFer=transfer_new
 def rebuildSelect(select_function_new):#改变按层数迭代的方法
	 self.selectByLayer=select_function_new
 def rebuildTransfer(transfer_new):#改变输出转换子图的方法
	 self.transFer=transfer_new

 def selectByLayer(self,imagelist,layer,wrate,hrate,ImageSource,GreyScaleLock):#按迭代层数进行N次选择,输出一个划分好的子图集
    tik=0
    outlist=imagelist
    common=pic_common()
    if layer==0:
       return outlist
    else:
       for time in range(0,layer):
         preparelist=[]
         for image in outlist:
          #image.graphInfo()
          stepSize=[math.ceil(image.width/wrate),math.ceil(image.height/hrate)]#ceil()取整用
          #print("width: "+str(image.width))
          output=common.get_slice(image.x,image.y,image,stepSize,stepSize,ImageSource,GreyScaleLock,common.calGreyAvenge)#得到切割后子图集
          
          #for i in output:
             #i.graphInfo()
          preparelist+=output
          
         outlist=preparelist
           
       return outlist
    
 def transFer(self,inputpath,wrate,hrate,grate,layer,outputpath,selectfunction,lockfunction):#读入参数：要转换的文件夹路径，宽比，高比，灰度阈值倍率，分解子图层数,输出目录,层筛选函数，灰度锁函数
    common=pic_common()
    
    for path in os.listdir(inputpath):
        image = cv2.imread(inputpath+'/'+path)
        #print('dealing with:'+path)
        
        outputlist=common.readIntoList(inputpath+'/'+path,wrate,hrate,grate,lockfunction)#把图像初次分割为子图集
        outputlist=selectfunction(outputlist,layer,wrate,hrate,image,lockfunction(image,1.005))#根据灰度与层数筛选子图集，可在之后类自定义
        common.saveImageList(outputlist,image,path,outputpath)#outputlist内子图集合经过变换整合输出到outputpath文件夹


parser=argparse.ArgumentParser(description='depart_pic')
parser.add_argument('--input',type=str,default='input/',help='where the path pictures wanted to be traned,要转换的文件夹路径')
parser.add_argument('--wrate',type=int,default=5,help='how many pieces the width would be departed,宽比')
parser.add_argument('--hrate',type=int,default=5,help='how many pieces the height would be departed,高比')
parser.add_argument('--grate',type=float,default=1.005,help='the rate geryscale would plus,influences the greyloak and the departture,灰度阈值倍率')
parser.add_argument('--layer',type=int,default=3,help='how mant times the subgraphs would be departed into subgraphsets,分解子图层数')
parser.add_argument('--output',type=str,default='output/',help='where the path pictures wanted to be outlist,输出目录')
def main(args):
    inputdata =parser.parse_args()
    common=pic_common()
    sel=pic_select()#初始化重要筛选类
    sel.transFer(inputdata.input,inputdata.wrate,inputdata.hrate,inputdata.grate,inputdata.layer,inputdata.output,sel.selectByLayer,common.greylockFunction)
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
