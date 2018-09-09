# android adb shell scripts

# adb backend process
adb shell ps | grep adbd

# adb command

# getting device lists and device status
adb devices
# device,offline,unknown
adb get-state

# kill-server,start-server
adb kill-server
adb start-server

# adb logcat
adb logcat
adb bugreport
# adb bugreport > <location>

adb install
adb install -r
adb uninstall
# adb pull sdcard/pull.txt <location>
adb push # local file to device

adb root
adb reboot
adb forward tcp:1134 tcp:8888
adb connect

# adb shell
adb shell pm list package
adb shell pm list package -f -3 -i zhihu
adb shell pm path com.tencent.mobileqq
adb shell pm dump com.tencent.mobileqq
adb shell pm list instrumentations com.tencent.mobileqq
adb install /adb pm install
adb pm uninstall
adb pm clear
adb pm set-install-location
adb pm get-install-location

# am activity management
adb shell am start -n com.android.camera/.camera
adb shell am start -S com.android.camera/.camera
adb shell am start -W com.android.camera/.camera
adb shell am start -a android.intent.action.VIEW -d http://testerhome.com
adb shell am start -a android.intent.action.CALL -d tel:10086
adb shell am monitor
am force-stop
am startservice
am broadcast
am shell input text abcds
adb shell input keyevent KEYCODE_HOME
adb shell input tap 500 500
adb shell input swipe 900 500 100 500
adb shell input swipe 500 500 501 501 2000
adb shell screencap -p /sdcard/screen.png
adb shell screenrecord sdcard/record.mp4
adb shell uiautomator dump
adb shell ime list -s
adb shell ime set com.baidu.input_mi/.ImeService

## others
monkey
settings
dumpsys
log
getprop

## linux command
cat,cd,chmod,cp,date,df,du,grep,kill,ln,ls,isof,netstat,ping,ps,rm,rmdir,top
touch, >/>>, |
