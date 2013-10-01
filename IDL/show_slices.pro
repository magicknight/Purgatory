PRO show_slices

img1=fltarr(750,335)
img2=fltarr(750,335)
img3=fltarr(750,335)
img4=fltarr(750,335)
img5=fltarr(750,335)

openr,1,'test1.img'
readu,1,img1
close,1
openr,1,'test2.img' 
readu,1,img2        
close,1
openr,1,'test3.img' 
readu,1,img3        
close,1
openr,1,'test4.img' 
readu,1,img4        
close,1
openr,1,'test5.img' 
readu,1,img5        
close,1

window,0,XSIZE = 750*2, YSIZE = 335*3
             
tvscl,img1,1
tvscl,img2,2
tvscl,img3,3
tvscl,img4,4
tvscl,img5,0

end
