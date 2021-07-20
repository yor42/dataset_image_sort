# -*-coding: utf-8-*-
# Juyeong 210720
# Chaeho 210720

import glob
import os
import shutil


def RenameFiles():
    files = []
    while True:
        inputdir = input('Input Directory: ')  # 폴더 경로 입력
        if os.path.isdir(inputdir):
            break
        else:
            print('Invalid Directory! Please check if directory is valid.')
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
        pathtoimg = input("Please Enter the path to img folder on root of dataset")  # 폴더 경로 입력
        if os.path.isdir(inputdir):
            break
    outputdir = os.path.join(pathtoimg, tag_time+'/'+tag_weather)
    start_number = len(glob.glob1(outputdir, "*."+ext))+1

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
    RenameFiles()
    shouldrepeat = input('Continue Renaming files? (Y/N)')
    if shouldrepeat == 'N':
        break
    elif shouldrepeat != 'Y':
        print("please type Y(yes) or N(no)")
