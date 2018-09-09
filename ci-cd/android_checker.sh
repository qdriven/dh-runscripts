#!/bin/bash
# windows
# 1. Run_EN.bat
# 2. Input the folder's path.
# 3. After finish checking, the result is in same folder.
# ANR: ANR.csv
# Force Close: FATAL_EXCEPTION.csv
# tombstone: tombstone.csv
#
# linx
# 1. sh check.sh "the folder's path"
# 2. Input the folder's path.
# 3. After finish checking, the result is in same folder.
# ANR: ANR.csv
# Force Close: FATAL_EXCEPTION.csv
# tombstone: tombstone.csv
#
# PS: the command of logcat is "logcat -v time". The script will check all subfolder's log file.

fatal(){
echo check_Fatal: $1
grep -E "E/AndroidRuntime|Force finishing activity|crashApplication" $1|sed 's/"//g'|awk -F ":" -v file="$1" -v csv="$2/FATAL_EXCEPTION.csv" -v t1="\"" 'BEGIN{p=0}{if(p==1||p==2){if($4!=" Process"){p=3;c=substr($4,2,length($4)-1)","t1 substr($5,2,length($5)-1) t1}};if($4==" Process"){p=2;if(NF==6){b=substr($5,2,length($5)-6)}else{b=$5":"substr($6,1,length($6)-5)}};if($4==" FATAL EXCEPTION"||$4==" *** FATAL EXCEPTION IN SYSTEM PROCESS"){p=1;if(a!="")print file","b","a","c","t1 d t1","t1 f t1","t1 r t1 >>csv;a=substr($5,2,length($5)-2);b="SYSTEM PROCESS";r=$0;f="";d=""};if(substr($4,4,15)=="Force finishing")b=substr($4,29,length($4)-28);if($4==" Caused by"){if(d!="")d=d"\n"substr($5,2,length($5)-1);else d=substr($5,2,length($5)-1)};if(substr($4,3,2)=="at"){e=substr($0,length($1)+length($2)+length($3)+9,length($0)-length($1)-length($2)-length($3)-6);if(f==""){f=e}else{f=f"\n"e}}if(p>1)r=r"\n"$0}END{if(a!="")print file","b","a","c","t1 d t1","t1 f t1","t1 r t1 >>csv}'
}

anr(){
echo check_ANR: $1
grep -A 9 "ANR in" $1|sed 's/"//g'|awk -F ":" -v file="$1" -v csv="$2/ANR.csv" -v t1="\"" 'BEGIN{p=0}{if(substr($4,2,3)=="ANR"){p=1;if(a!="")print file","a","b","t1 c t1 >>csv;a=t1 substr($4,9,length($4)-8) t1;c=$0};if($4==" PID")p=2;if($4==" Reason"){b=t1 $5 t1;p=2};if(p>1)c=c"\n"$0}END{if(a!="")print file","a","b","t1 c t1 >>csv}'
}

tombstone(){
echo check_tombstone: $1
grep "F/DEBUG|F/AEE/DEBUG|I/DEBUG" $1|sed 's/"//g'|awk -F ":" -v file="$1" -v csv="$2/tombstone.csv" -v t1="\"" 'BEGIN{p=0}{if($4==" Build fingerprint"){p=1;if(a!="")print file","a","t1 b t1","t1 c t1 >>csv;c=$0};if($4==" Revision")p=2;if($4==" Tombstone written to")p=0;if($4==" pid"){if(NF==7){a=$NF}else{a=$(NF-1)":"$NF}};if($4==" backtrace"){p=3;b=""}else{if(p==3){if(b!="")b=b"\n";j=0;for(i=1;i<length($4)+1;i++){s=substr($4,i,1);if(s==" ")j+=1;if(j==10){break}else{if(j==9&&s!=" ")b=b s}}}};if(p>1)c=c"\n"$0}END{if(a!="")print file","a","t1 b t1","t1 c t1 >>csv}'
sed -i 's/log,.*>>> /log,/g;s/ <<*,/,/g' $2/tombstone.csv
}


echo "File,Process,Thread,Exception,Exception info,Caused by,at,Log" >$1/FATAL_EXCEPTION.csv
echo "File,ANR in,Reason,Log" >$1/ANR.csv
echo "File,tombstone,Backtrace,Log" >$1/tombstone.csv
find $1 -name *.log|xargs grep -l -E ": ANR in|Build fingerprint|FATAL EXCEPTION"|while read log ;do
if [ `grep -c "FATAL EXCEPTION" $log` -ne 0 ];then
fatal $log $1
fi
if [ `grep -c ": ANR in" $log` -ne 0 ];then
anr $log $1
fi
if [ `grep -c "Build fingerprint" $log` -ne 0 ];then
tombstone $log $1
fi
done
if [ `awk 'END{print NR}' $1/FATAL_EXCEPTION.csv` -eq 1 ];then
	rm $1/FATAL_EXCEPTION.csv
fi
if [ `awk 'END{print NR}' $1/ANR.csv` -eq 1 ];then
	rm $1/ANR.csv
fi
if [ `awk 'END{print NR}' $1/tombstone.csv` -eq 1 ];then
	rm $1/tombstone.csv
fi
