;       display.pro
;       Written by Howard Gifford
;       Date: 14Mar01
PRO display, fimg, dimx, dimy, dimz, outmat, NSLICE=nslice, SLICE0=slice0, TV=tv, ROT=rot, VIEW=view, OPUT=oput, PRISM=prism, POS=pos

  nparam=n_params()
  if(nparam lt 4) then begin
    print, 'Input: display, img file, x dim, y dim, z dim, [optional output array],'
    print, '       nslice=<slices to display> (default:20),'
    print, '       slice0=<first slice to display> (default:0), /tv'
    print, '       view=<1,2,3> (1:sag;2=cor;3=trans(default))'
    print, '       oput= output file name'
    print, '       rot: rotate/flip each 2D image'
    print, '           : 0= no transform (default)'
    print, '           : 1= rotate 180 deg <rotate(img,2)>'
    print, '           : 2= flip about x-axis <rotate(img,7)>'
    print, '           : 3= flip about y-axis <rotate(img,5)>'
    print, '       /prism: file= big-endian; short int; has 2048-byte header'
    print, '       /prism: file= big-endian; short int; has 2048-byte header'
    print, '       pos= starting position argument [0,1, ...] for tvscl'
    RETURN
  endif
  IF(NOT KEYWORD_SET(view)) THEN view= 3
  ;IF(NOT KEYWORD_SET(rot)) THEN rot= 0
  IF(NOT KEYWORD_SET(pos)) THEN pos= 0
  IF (view eq 1) THEN BEGIN
    vdim= dimx
    dim1= dimy
    dim2= dimz
  ENDIF ELSE IF (view eq 2) THEN BEGIN
    vdim= dimy
    dim1= dimx
    dim2= dimz
  ENDIF ELSE BEGIN
    vdim= dimz
    dim1= dimx
    dim2= dimy
  ENDELSE
;
  IF(NOT KEYWORD_SET(nslice)) THEN BEGIN
    IF( vdim lt 20 ) THEN nslice= vdim ELSE nslice= 20
  ENDIF
  IF(NOT KEYWORD_SET(slice0)) THEN slice0= 0
  if ((slice0 lt 0) OR ((slice0+nslice) gt vdim)) then BEGIN
    MESSAGE, 'Check dim*, nslice and slice0 parameters'
    STOP
  ENDIF
;
  HDSZ= 2048
  vdim= nslice
  img= fltarr(dimx,dimy,dimz)
  vimg= fltarr(dim1,dim2,vdim)
  close, 1
  openr, 1, fimg
  A = FSTAT(1)
  print, 'File ',  A.NAME, ' is ', A.SIZE, ' bytes long.'
  if (KEYWORD_SET(prism)) THEN BEGIN
    print, "Header is ", HDSZ, " bytes"
    A.SIZE= (A.SIZE-HDSZ)
  ENDIF
  typ= A.SIZE/(long(dimx)*dimy*dimz)
  print, 'Data type= ', typ
  img= fix(img,TYPE=typ)
  if (KEYWORD_SET(prism)) THEN BEGIN
    print,"Prism format: 2048-byte header; unsigned short-int; big-endian"
    img= uint(img)
    head= bytarr(HDSZ)
    readu, 1, head
    readu, 1, img
    close, 1
    BYTEORDER, img, /SSWAP
    img= float(img)
  ENDIF Else BEGIN
    readu, 1, img
    close, 1
  ENDELSE
;Next line commented 12Sep06
  ;if (keyword_set(tv)) then BEGIN
  ;  img= (!d.table_size-1)*(img-min(img))/(max(img)-min(img))
  ;ENDIF
;
  IF (view eq 1) THEN BEGIN
    for i=0,(nslice-1) do vimg(*,*,i)= img(slice0+i,*,*)
  ENDIF ELSE IF (view eq 2) THEN BEGIN
    for i=0,(nslice-1) do vimg(*,*,i)= img(*,slice0+i,*) 
  ENDIF ELSE BEGIN
    for i=0,(nslice-1) do vimg(*,*,i)= img(*,*,slice0+i) 
  ENDELSE
;
  if (keyword_set(rot)) then BEGIN
    rotmat= [0,2,7,5]
    for i=0,(nslice-1) do vimg(*,*,i)= rotate(vimg(*,*,i),rotmat[rot])
  ENDIF
  if (keyword_set(tv)) then BEGIN
    vimg= (!d.table_size-1)*(vimg-min(vimg))/(max(vimg)-min(vimg))
    for i=0,(nslice-1) do tv, vimg(*,*,i),pos+i
  ENDIF ELSE BEGIN
    for i=0,(nslice-1) do tvscl, vimg(*,*,i),pos+i
  ENDELSE
  print, 'Max= ',max(vimg),';Min= ',min(vimg)
  print, 'Mean= ',mean(vimg),';SD= ',sqrt(variance(vimg))
  IF (KEYWORD_SET(oput)) THEN BEGIN
    print, 'Writing to file ', oput
    openw, 1, oput
    writeu, 1, vimg
    close, 1
  ENDIF
  outmat= vimg ;pass image to named variable
END
