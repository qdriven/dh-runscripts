FROM python:3.7.2-alpine3.9
# if not work, use MAINAINER instead
LABEL  maintainer="qkits"

# install bash
## Set to alphine repo

## install tools: https://www.mowson.org/karl/2016/2016-05-22_install_ansible_under_alpinelinux/
RUN apk --update add --no-cache openssh bash linux-headers musl-dev\
    gcc git libffi-dev musl-dev openssl-dev perl py-pip python python-dev sshpass\
  && sed -i s/#PermitRootLogin.*/PermitRootLogin\ yes/ /etc/ssh/sshd_config \
  && echo "root:root" | chpasswd \
  && rm -rf /var/cache/apk/*
RUN sed -ie 's/#Port 22/Port 22/g' /etc/ssh/sshd_config
RUN sed -ri 's/#HostKey \/etc\/ssh\/ssh_host_key/HostKey \/etc\/ssh\/ssh_host_key/g' /etc/ssh/sshd_config
RUN sed -ir 's/#HostKey \/etc\/ssh\/ssh_host_rsa_key/HostKey \/etc\/ssh\/ssh_host_rsa_key/g' /etc/ssh/sshd_config
RUN sed -ir 's/#HostKey \/etc\/ssh\/ssh_host_dsa_key/HostKey \/etc\/ssh\/ssh_host_dsa_key/g' /etc/ssh/sshd_config
RUN sed -ir 's/#HostKey \/etc\/ssh\/ssh_host_ecdsa_key/HostKey \/etc\/ssh\/ssh_host_ecdsa_key/g' /etc/ssh/sshd_config
RUN sed -ir 's/#HostKey \/etc\/ssh\/ssh_host_ed25519_key/HostKey \/etc\/ssh\/ssh_host_ed25519_key/g' /etc/ssh/sshd_config
RUN /usr/bin/ssh-keygen -A
RUN ssh-keygen -t rsa -b 4096 -f  /etc/ssh/ssh_host_key

# change to bash
RUN ["/bin/bash", "-c","echo http://mirrors.ustc.edu.cn/alpine/v3.9/main >/etc/apk/repositories"]
RUN ["/bin/bash","-c","echo http://mirrors.ustc.edu.cn/alpine/v3.9/community >> /etc/apk/repositories"]


#Enable ssh login feature
# RUN ssh-keygen -t rsa -f /etc/ssh/ssh_host_rsa_key \
#   && ssh-keygen -t dsa -f /etc/ssh/ssh_host_dsa_key \
#   && ssh-keygen -t ecdsa -f /etc/ssh/ssh_host_ecdsa_key \
#       && ssh-keygen -t ed25519 -f /etc/ssh/ssh_host_ed25519_key \
#   #ssh-keyscan -p7999 code.bkjk.com > /root/.ssh/known_hosts \
#   && echo -e "StrictHostKeyChecking no" >> /etc/ssh/ssh_config \
#   # && chmod -R 600 /root/.ssh/ \
#   && sed -i 's/UsePAM yes/UsePAM no/g' /etc/ssh/sshd_config \
#   && echo 'root:passw0rd' | chpassw

# # install python
# RUN apk add --no-cache python3 && \
#     python3 -m ensurepip && \
#     rm -r /usr/lib/python*/ensurepip && \
#     pip3 install --upgrade pip setuptools && \
#     if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
#     if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
#     rm -r /root/.cache

## Setup Environement
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN ["/bin/bash", "-c","/usr/sbin/sshd -d"]  
# RUN python -v
# RUN sed -i '/^alias/d' /root/.bashrc 

## Setup pip conf in China
RUN mkdir /root/.pip \
	&& echo "[global]" > /root/.pip/pip.conf \
	&& echo "index-url = http://pypi.douban.com/simple" >> /root/.pip/pip.conf \
	&& echo "trusted-host = pypi.douban.com" >> /root/.pip/pip.conf \
	&& echo "disable-pip-version-check = true" >> /root/.pip/pip.conf \
	&& echo "timeout = 120" >>/root/.pip/pip.conf 

# ## install default requirements - default with ansible
# RUN pip install ansible

## Setup workspace for tester
RUN mkdir -p /workspace
WORKDIR /workspace/

# EXPOSE 22
