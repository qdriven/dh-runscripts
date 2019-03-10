# Configure Golang
mkdir ~/go
grep -q -F 'GOPATH' ~/.bashrc || echo 'export GOPATH="/home/$(whoami)/go"' >> ~/.bashrc


# Enable Fish by Default
grep -q -F 'fish' ~/.bashrc || echo 'exec fish' >> ~/.bashrc


sudo update-alternatives --install /usr/bin/vi vi /usr/bin/nvim 60
sudo update-alternatives --config vi
sudo update-alternatives --install /usr/bin/vim vim /usr/bin/nvim 60
sudo update-alternatives --config vim
sudo update-alternatives --install /usr/bin/editor editor /usr/bin/nvim 60
sudo update-alternatives --config editor



# Install dotfiles
echo "Installing dotfiles..."
mkdir -p ~/.config/fish
mkdir -p ~/.config/nvim
cp -rv fish/config.fish ~/.config/fish/config.fish
cp -rv nvim/init.vim  ~/.config/nvim/init.vim
cp -rv tmux/tmux.conf ~/.tmux.conf

## Install Tmux Plugin Manager
git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm



## Configuring Vim
echo "Configuring NeoVim..."
mkdir -p ~/.vim
cd ~/.vim
mkdir -p tmp
cd tmp/
mkdir -p swap
mkdir -p undo
mkdir -p backup
cd

# install neovim python support
pip install pynvim

# install vundle
git clone https://github.com/gmarik/vundle.git ~/.vim/bundle/vundle
vim +BundleInstall

# install YCM
cd ~/.vim/bundle/YouCompleteMe && python3 install.py && cd
#python3 install.py --gocode-completer --clang-completer

# install js autocompletion (if you need newer node.js, install nvm instead)
#sudo apt install nodejs npm -y
#cd ~/.vim/bundle/tern_for_vim/
#npm install
#sudo npm install -g jshint
echo "All Done."