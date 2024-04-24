from photostereo import photometry
import cv2 as cv
import time
import numpy as np
import os

IMAGES = 4
root_fold = r"cropped_data\2083\2008-03-13_10-47-25"
# root_fold = r'cropped_data\1010\2009-07-08_20-24-55'
root_light = r'Photoface_dist\PhotofaceDB'
format = ".png"
light_manual = True

#Load input image array
image_array = []

list_name_image = [x for x in os.listdir(root_fold) if x.endswith('.bmp') or x.endswith(".png")]

image_array = [(cv.imread(os.path.join(root_fold, x), cv.IMREAD_GRAYSCALE)) for x in list_name_image]

myps = photometry(IMAGES, False)

if light_manual:
    # SETTING LIGHTS MANUALLY
    # slants = [71.4281, 66.8673, 67.3586, 67.7405]
    # tilts = [140.847, 47.2986, -42.1108, -132.558]

#     LightAngle = [
#    90-15.7 360-117.3;
#    90-17.9 360-50.3;
#    90-18.4 360-302.8;
#    90-20.0 360-229.3;
#    ]; 

    # LightAngle = [
    #     90-36 360-134;
    #     90-42 360-47;
    #     90-40 360-313;
    #     90-36 360-233];

    # slants = [90-36, 90-42, 90-40, 90-36]
    # tilts = [180-134, 180-47, 180-313, 180-233]
    
    slants = [90-36, 90-42, 90-40, 90-36]
    tilts = [180-134, 180-47, 180-313, 180-233]

    # slants = [36, 42, 40, 36]
    # tilts = [180-134, 180-47, 180-313, 180-233]

    slants = [36, 42, 40, 36]
    tilts = [90-134, 90-47, 90-313, 90-233]

    # slants = [15.7, 17.9, 18.4, 20]
    # tilts = [360-117.3, 360-50.3, 360-302.8, 360-229.3]

    myps.setlmfromts(tilts, slants)
    print(myps.settsfromlm())
else:
    # LOADING LIGHTS FROM FILE
    fs = cv.FileStorage(root_fold + "LightMatrix.yml", cv.FILE_STORAGE_READ)
    fn = fs.getNode("Lights")
    light_mat = fn.mat()
    myps.setlightmat(light_mat)
    #print(myps.settsfromlm())

tic = time.time()
# print(root_fold + "mask" + format)
# mask = cv.imread(root_fold + "mask" + format, cv.IMREAD_GRAYSCALE)
# print(mask)
# print(image_array)


# Tạo một ảnh mask trắng có cùng kích thước với ảnh gốc
mask = np.ones_like(image_array[0]) * 255

normal_map = myps.runphotometry(image_array, np.asarray(mask, dtype=np.uint8))
normal_map = cv.normalize(normal_map, None, 0, 255, cv.NORM_MINMAX, cv.CV_8UC3)
albedo = myps.getalbedo()
albedo = cv.normalize(albedo, None, 0, 255, cv.NORM_MINMAX, cv.CV_8UC1)
gauss = myps.computegaussian()
med = myps.computemedian()

cv.imwrite('normal_map1.png',normal_map)
cv.imwrite('albedo.png',albedo)
cv.imwrite('gauss.png',gauss)
cv.imwrite('med.png',med)
cv.imshow("normal", normal_map)
cv.waitKey(0)
cv.destroyAllWindows()
toc = time.time()
print("Process duration: " + str(toc - tic))

# # TEST: 3d reconstruction
# #myps.computedepthmap()
# myps.computedepth2()
# myps.display3dobj()
# cv.imshow("normal", normal_map)
# cv.imshow("mean", med)
# cv.imshow("gauss", gauss)
# cv.waitKey(0)
# cv.destroyAllWindows()