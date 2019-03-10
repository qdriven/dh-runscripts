
sudo cp -rv /etc/apt/sources.list /etc/apt/sources.list_bnk
sudo rm /etc/apt/sources.list
sudo cp tuna_source_list  /etc/apt/sources.list

sudo apt-get update