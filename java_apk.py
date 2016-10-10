#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
./channel文件内容如下：
360
91
qihu
uc
xiaomi
'''

import os
import shutil

def readChannelfile(filename):
    f = open(filename)
    while True:
        line = f.readline().strip('\n')
        if len(line) == 0:
            break
        else:
            channelList.append(line);
    f.close()

def backUpManifest():
    if os.path.exists('./AndroidManifest.xml'):
        os.remove('./AndroidManifest.xml')
    manifestPath = './temp/AndroidManifest.xml'
    shutil.copyfile(manifestPath, './AndroidManifest.xml')

def modifyChannel(value):
    tempXML = ''
    f = open('./AndroidManifest.xml')
    for line in f:
        if line.find('channel_value') > 0:
            line = line.replace('channel_value', value)
        tempXML += line
    f.close()

    output = open('./temp/AndroidManifest.xml', 'w')
    output.write(tempXML)
    output.close()
    
    unsignApk = r'./bin/%s_%s_unsigned.apk'% (easyName, value)
    cmdPack = r'java -jar apktool.jar b temp %s'% (unsignApk)
    os.system(cmdPack)
    
    unsignedjar = r'./bin/%s_%s_unsigned.apk'% (easyName, value)
    signed_unalignedjar = r'./bin/%s_%s_signed_unaligned.apk'% (easyName, value)
    signed_alignedjar = r'./bin/%s_%s.apk'% (easyName, value)
    cmd_sign = r'jarsigner -verbose -keystore %s -storepass %s -signedjar %s %s %s'% (keystore, storepass, signed_unalignedjar, unsignedjar, alianame)
    cmd_align = r'zipalign -v 4 %s %s' % (signed_unalignedjar, signed_alignedjar)
    os.system(cmd_sign)
    os.remove(unsignedjar)
    os.system(cmd_align)
    os.remove(signed_unalignedjar)
    

channelList = []
apkName = 'ApkTest.apk'
easyName = apkName.split('.apk')[0]
keystore='./keystore/ApkTest.keystore'
storepass='123456'
alianame='ApkTest.keystore'

output_apk_dir="./bin"
if os.path.exists(output_apk_dir):
    shutil.rmtree(output_apk_dir)

readChannelfile('./channel')
print('-------------------- your channel values --------------------')
print('channel list: ', channelList)
cmdExtract = r'java -jar apktool.jar  d -f -s %s temp'% (apkName)
os.system(cmdExtract)

backUpManifest()
for channel in channelList:
    modifyChannel(channel)

if os.path.exists('./temp'):
    shutil.rmtree('./temp')
if os.path.exists('./AndroidManifest.xml'):
    os.remove('./AndroidManifest.xml')
print('-------------------- Done --------------------')

