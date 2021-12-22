# -*-coding: utf-8-*-
# Juyeong 210720
# Chaeho 210720

import glob
import os
import shutil
import cv2
import rosbag
import csv
import sys
import numpy as np
import rospy

def imgmsg_to_cv2(img_msg):

    if img_msg.encoding != "bgr8":
        rospy.logerr("This Coral detect node has been hardcoded to the 'bgr8' encoding. Come change the code if "
                     "you're actually trying to implement a new camera")
    dtype = np.dtype("uint8") # Hardcode to 8 bits...
    dtype = dtype.newbyteorder('>' if img_msg.is_bigendian else '<')
    image_opencv = np.ndarray(shape=(img_msg.height, img_msg.width, 3), # and three channels of data. Since OpenCV works with bgr natively, we don't need to reorder the channels.
                    dtype=dtype, buffer=img_msg.data)
    # If the byt order is different between the message and the system.
    if img_msg.is_bigendian == (sys.byteorder == 'little'):
        image_opencv = image_opencv.byteswap().newbyteorder()
    return image_opencv

def extractImages(bagdir):
    filelist = glob.glob1(bagdir, "*.bag")
    for bagfile in filelist:
        bag = rosbag.Bag(os.path.join(bagdir, bagfile), 'r')
        topicCamera = "/camera1/cv_camera/image_raw"
        topicCSV = ""
        imagedir = os.path.splitext(os.path.join(bagdir, bag.filename))[0]
        if not os.path.isdir(imagedir):
            os.makedirs(imagedir)
        idx = 0
        latestCSV = None
        latestImg = None
        for topic, msg, t in bag.read_messages(topics=[topicCamera]):
            if topic == topicCSV:
                msgString = str(msg)
                msgList = msgString.split('\n')
                latestCSV = msgList
                #handle CSV Image
            elif topic == topicCamera:
                cv_img = imgmsg_to_cv2(msg)
                latestImg = cv_img
                cv2.imwrite(os.path.join(imagedir, str(t.secs)+"_"+str(t.nsecs)+".jpg"), cv_img)
                print("Wrote "+str(t.secs)+"_"+str(t.nsecs)+".jpg"+" at "+str(imagedir))
            filename = os.path.join(imagedir, str(idx))
            if latestCSV is not None and latestImg is not None:
                cv2.imwrite(filename+".jpg", latestImg)
                with open(filename+".csv", 'w+', newline='') as csvfile:
                    filewriter = csv.writer(csvfile)
                    filewriter.writerows(latestCSV)
                    csvfile.close()
            idx += 1
        bag.close()



def RenameFiles(inputdir):
    files = []
    ext = input('jpg / txt: ')  # 이미지 확장자
    for root, dirs, F in os.walk(inputdir):
        for file in F:
            if file.endswith("."+ext):
                files.append(os.path.join(root, file))

    #####################################
    # 이미지, 어노테이션 둘 다 바꿀 때
    # files_jpg = glob.glob(dir+'/*.jpg')
    # files_txt = glob.glob(dir+'/*.txt')
    #####################################

    img_num = len(files)  # 총 이미지/어노테이션 개수
    #####################################
    # img_num_jpg = len(files_jpg)
    # img_num_txt = len(files_txt)
    #####################################

    tag_time = input('day / evening: ')  # 파일명-시간 입력받음
    tag_weather = input('sunny / cludy / foggy / rainy: ')  # 파일명-날씨 입력받음

    while True:
        pathtoimg = input("Please Enter the path to img folder on root of dataset: ")  # 폴더 경로 입력
        if os.path.isdir(inputdir):
            break
    outputdir = os.path.join(pathtoimg, tag_time+'/'+tag_weather)
    start_number = len(glob.glob1(outputdir, "*."+ext))+1

    isnumbercorrect = input("Firse Data index calculated by program is "+str(start_number)+". is this number correct? (Y/N)")
    if isnumbercorrect == 'N' or extractbag == 'n' or extractbag == 'no' or extractbag == 'No':
        start_number = input("Please Enter the first index of output file.(usually the number of existing file +1)")

    if not os.path.exists(outputdir):
        os.makedirs(outputdir)

    print(tag_time, tag_weather, ', from', start_number)
    # print(files_jpg)
    # print(files_txt)

    for idx in range(img_num):
        filename = str(files[idx])
        #####################################
        # filename_jpg = str(files_jpg[idx])
        # filename_txt = str(files_txt[idx])
        #####################################

        file_number = int(start_number) + idx
        # print('org: ' + filename)

        new_name = outputdir + '/' + tag_time + '_' + tag_weather + '_' + str(file_number) + '.' + ext
        #####################################
        # new_name_jpg = dir + '/' + tag_time + '_' + tag_weather + '_' + str(file_number) + '.jpg'
        # new_name_txt = dir + '/' + tag_time + '_' + tag_weather + '_' + str(file_number) + '.txt'
        #####################################

        print('new: ' + new_name)
        print('-*-')

        shutil.copy(filename, new_name)
        #####################################
        # os.rename(filename_jpg, new_name_jpg)
        # os.rename(filename_txt, new_name_txt)
        #####################################


while True:

    while True:
        directory = input('Input Directory: ')  # 폴더 경로 입력
        if os.path.isdir(directory):
            break
        else:
            print('Invalid Directory! Please check if directory is valid.')

    extractbag = input('Extract images from rosbag first? (Y/N): ')
    if extractbag == 'Y' or extractbag == 'y':
        extractImages(directory)

    shouldrename = input('Proceed to Renaming Process? (Y/N): ')
    if shouldrename == 'Y' or extractbag == 'y' or extractbag == 'yes' or extractbag == 'Yes':
        RenameFiles(directory)
    shouldrepeat = input('Continue Renaming files? (Y/N): ')
    if shouldrepeat == 'N' or extractbag == 'n' or extractbag == 'no' or extractbag == 'No':
        break
    elif shouldrepeat != 'Y':
        print("please type Y(yes) or N(no)")
