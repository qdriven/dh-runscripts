#!/bin/bash

function checkENV()
{
    condition=${1}
    if [[ "${ONLY_CONFIG}" == [tT][rR][uU][eE] ]];then
        ps -ef | grep "jar" | grep "configservice" | grep "${condition}" > /dev/null || exit 1
        echo "Only ${condition} config service is runing."
    else
        ps -ef | grep "jar" | grep "adminservice" | grep "${condition}" > /dev/null || exit 1
        echo "The ${condition} admin service is runing."
        ps -ef | grep "jar" | grep "configservice" | grep "${condition}" > /dev/null || exit 1
        echo "The ${condition} config service is runing."
    fi
}



# portal
if [[ -n "${PORTAL_DB}" ]];then
    ps -ef |grep jar |grep portal > /dev/null || exit 1
    echo "The portal service is runing."
fi

# dev
if [[ -n "${DEV_DB}" ]];then
    checkENV dev
fi

# fat
if [[ -n "${FAT_DB}" ]];then
    checkENV fat
fi

# uat
if [[ -n "${UAT_DB}" ]];then
    checkENV uat
fi

# pro
if [[ -n "${PRO_DB}" ]];then
    checkENV pro
fi