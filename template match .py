import cv2
import numpy as np
import glob
import os
import imutils
#insialisasi Template
templates=[]
files=glob.glob(r'D:/tempwang/dogshit/*.png')
for file in files :

       img = cv2.imread(file)
       img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
       img = cv2.Canny(img,50,200)
       
       templates.append(img)

for temp in templates :
    (tH, tW) = temp.shape[:2]
    cv2.imshow("Template",temp)

#Load data yang akan dimatch dengan template dan diproses
    for foto in glob.glob (r'D:/tempwang/test/*jpg'):
        imeg = cv2.imread(foto)
        abu = cv2.cvtColor(imeg,cv2.COLOR_BGR2GRAY)
        imeg = cv2.resize(imeg,(500,500))
        found = None
#Scaling gambar input
        for scale in np.linspace(0.2, 1.0, 20)[::-1]:
                # Scaling image dan kemudian di deteksi tepi
                resized = imutils.resize(abu, width = int(abu.shape[1] * scale))
                r = abu.shape[1] / float(resized.shape[1])
                if resized.shape[0] < tH or resized.shape[1] < tW:
                       break
                # Template matching
                edged = cv2.Canny(resized, 50, 200)
                cv2.imshow("Imade", edged)
                result = cv2.matchTemplate(edged, temp, cv2.TM_COEFF)
                (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
                # Hasil deteksi akhir dan loop untuk membaca isi folder
                if found is None or maxVal > found[0]:
                        found = (maxVal, maxLoc, r)
                        if maxVal >= 0.4:
                            rep = "uang"
                            foto1 = foto
                            foto1 = foto1.replace(rep,"")
                            foto1 = foto1.replace("\\","")
                            foto1 = foto1.replace(".jpg","")

        # Bounding Box 
        (maxVal, maxLoc, r) = found
        (startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
        (endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))
        # Bounding box digambar pada hasil
        if maxVal>= 0.4:
               cv2.rectangle(imeg, (startX, startY), (endX, endY), (0, 0, 255), 2)
        cv2.imshow("Image", imeg)
        cv2.waitKey(0)
