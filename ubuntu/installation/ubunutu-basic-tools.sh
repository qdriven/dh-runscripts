
sudo apt-get install software-properties-common

sudo apt-get install git
sudo apt-get install wget
sudo apt-get install scala
sudo add-apt-repository ppa:longsleep/golang-backports
sudo apt-get update
sudo apt-get install golang-go
sudo apt install -y tree curl wget htop ufw \
gufw cryptsetup \
encfs jq net-tools

curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
sudo apt-get install nodejs -y

# curl -sL https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
# echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
# sudo apt-get update && sudo apt-get install yarn



sudo apt-get install -y cmake build-essential silversearcher-ag exuberant-ctag
sudo apt install -y fish neovim tmux autojump


