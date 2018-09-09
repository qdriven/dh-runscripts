# -*- coding: utf-8 -*-
import os
import sys
import time

import datetime as dt
import pandas as pd


reload(sys)
sys.setdefaultencoding( "utf-8" )

def copyFiles(sourceDir, targetDir):
    copyFileCounts = 0
    print sourceDir
    print '%s copy %s the %sth file'%(dt.datetime.now(), sourceDir,copyFileCounts)
    for f in os.listdir(sourceDir):
        sourceF = os.path.join(sourceDir, f)
        targetF = os.path.join(targetDir, f)

        if os.path.isfile(sourceF):
            if not os.path.exists(targetDir):
                os.makedirs(targetDir)
            copyFileCounts += 1
            if not os.path.exists(targetF) or (os.path.exists(targetF) and (os.path.getsize(targetF) != os.path.getsize(sourceF))):
                open(targetF, "wb").write(open(sourceF, "rb").read())
                print '%s %s finish copying'%(dt.datetime.now(), targetF)
            else:
                print '%s %s exist'%(dt.datetime.now(), targetF)

        if os.path.isdir(sourceF):
            copyFiles(sourceF, targetF)

def btm(csvPath):
    print '%s Start btm'%dt.datetime.now()
    data=pd.read_csv(r'%s'%csvPath,warn_bad_lines=False,error_bad_lines=False).fillna(value='null')
    x_min=data['uptime'][0]
    loop=data['loop'].tolist()
    uptime=data['uptime'].tolist()
    battery_capacity='[[%s,%s]'%(data['uptime'][0],data['battery_capacity'][0])
    cpu_temperature='[[%s,%s]'%(data['uptime'][0],data['cpu_temperature'][0])
    battery_voltage='[[%s,%s]'%(data['uptime'][0],data['battery_voltage'][0])
    pdata='[[%s,%s,"%s",%s,%s,"%s","%s","%s"]'%(data['loop'][0],data['cpu_temperature'][0],data['cpufreq'][0],data['battery_capacity'][0],data['battery_voltage'][0],data['battery_status'][0],data['battery_health'][0],data['Date_Time'][0])
    for i in range(1,len(loop)-1):
        battery_capacity+=',[%s,%s]'%(data['uptime'][i],data['battery_capacity'][i])
        cpu_temperature+=',[%s,%s]'%(data['uptime'][i],data['cpu_temperature'][i])
        battery_voltage+=',[%s,%s]'%(data['uptime'][i],data['battery_voltage'][i])
        pdata+=',[%s,%s,"%s",%s,%s,"%s","%s","%s"]'%(data['loop'][i],data['cpu_temperature'][i],data['cpufreq'][i],data['battery_capacity'][i],data['battery_voltage'][i],data['battery_status'][i],data['battery_health'][i],data['Date_Time'][i])
    battery_capacity+="]"
    cpu_temperature+="]"
    battery_voltage+="]"
    pdata+="]"
    result="""function isHasElement(arr,value){
    var str = arr.toString();
    var index = str.indexOf(value);
    if(index >= 0){
        //存在返回索引
        var reg1 = new RegExp("((^|,)"+value+"(,|$))","gi");
        return str.replace(reg1,"$2@$3").replace(/[^,@]/g,"").indexOf("@");
    }else{
        return -1;//不存在此项
    }
}
function getp(x){
    var uptime=%s
return isHasElement(uptime,x);}

var x_min=%s
var battery_capacity=%s
var cpu_temperature=%s
var battery_voltage=%s
var pdata=%s"""%(uptime,x_min,battery_capacity,cpu_temperature,battery_voltage,pdata)
    f=open(r'%s/result/head/data.js'%os.path.dirname(csvPath),'a')
    f.write('%s'%result)
    f.close()
    print '%s Finish btm'%dt.datetime.now()

if __name__ == '__main__':
    csvPath=sys.argv[1]
    resultPath=os.path.dirname(csvPath)
    import shutil
    if os.path.exists(r'%s/result'%resultPath):
        try:
            shutil.rmtree(r'%s/result'%resultPath)
        except os.error, err:
            time.sleep(0.5)
            try:
                shutil.rmtree(r'%s/result'%resultPath)
            except os.error, err:
                print "Delete BTM_HTML Error!!!"
    else:
        os.mkdir(r'%s/result'%resultPath)
    print '%s Copying BTM_HTML'%dt.datetime.now()
    copyFiles('%s/BTM_HTML'%os.path.dirname(sys.argv[0]), '%s/result'%resultPath)
    print '%s Finish Copying BTM_HTML'%dt.datetime.now()
    btm(csvPath)
