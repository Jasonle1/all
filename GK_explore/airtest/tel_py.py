# -*- encoding=utf8 -*-
__author__ = "admin"

from airtest.core.api import *
import time
from airtest.core.android.android import Android
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

auto_setup(__file__)

appName_camera = "com.android.camera"

connect_device('android:///127.0.0.1:7555?touch_method=adb')
# connect_device('android:///')

print('lel')
# for i in range(0, 1000, 1):
#     start_app(appName_camera)#打开相机应用
#
#     keyevent("27")#拍照
#     sleep(1.0)
#     keyevent("3")#home键退出
