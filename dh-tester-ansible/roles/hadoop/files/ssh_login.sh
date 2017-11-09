#! /bin/sh

# make sure the share network is enabled in MACOS

# setup passphraseless ssh
# ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 0600 ~/.ssh/authorized_keys