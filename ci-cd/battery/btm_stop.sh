#!/system/bin/sh

if [ -f /data/local/tmp/busybox ];then
	export bb="/data/local/tmp/busybox"
else
	echo "No /data/local/tmp/busybox"
	exit
fi
if [ -f /data/local/tmp/stop ];then
	$bb rm /data/local/tmp/stop
fi

echo "loop,uptime,battery_capacity,cpu_temperature,battery_voltage,battery_status,battery_health,cpufreq,Date_Time" >/data/local/tmp/btm.csv
loop=0
if [ -f /sys/class/power_supply/battery/temp ];then
	temp="/sys/class/power_supply/battery/temp"
elif [ -f /sys/class/power_supply/battery/batt_temp ];then
	temp="/sys/class/power_supply/battery/batt_temp"
fi
while true;do
	tmp=`cat /proc/uptime /sys/class/power_supply/battery/capacity $temp`
	if [ -f /sys/class/power_supply/battery/voltage_now ];then
		voltage=$((`cat /sys/class/power_supply/battery/voltage_now`/1000))
	elif [ -f /sys/class/power_supply/battery/batt_vol ];then
		voltage=`cat /sys/class/power_supply/battery/batt_vol`
	fi
	tmp2=`cat /sys/class/power_supply/battery/status /sys/class/power_supply/battery/health`
	part1=`echo $tmp $voltage $tmp2|$bb awk '{a=sprintf("%.0f",$1);b=$3;c=$4/10;d=sprintf("%.3f",$5/1000);e=$6;f=$7}END{printf a","b","c","d","e","f}'`
	part2=`cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_cur_freq|$bb awk '{if(NR>1)printf "|";printf $1/1000}'`
	data_t=`date +%Y/%m/%d" "%H:%M:%S`
	echo $loop","$part1","$part2","$data_t>>/data/local/tmp/btm.csv
	if [ -f /data/local/tmp/stop ];then
		echo "Found stop file!!!"
		break
	elif [ `$bb df /data|$bb awk '{r=substr($(NF-1),1,length($(NF-1))-1)}END{print r+0}'` -ge 90 ];then
		echo "The free space of data less 10%,stop!!!"
		break
	fi
	sleep $1
	loop=$((loop+1))
done
