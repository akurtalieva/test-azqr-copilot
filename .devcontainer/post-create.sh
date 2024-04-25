## CaskaydiaCove Nerd Font
# Uncomment the below to install the CaskaydiaCove Nerd Font
mkdir $HOME/.local
mkdir $HOME/.local/share
mkdir $HOME/.local/share/fonts
wget https://github.com/ryanoasis/nerd-fonts/releases/latest/download/CascadiaCode.zip
unzip CascadiaCode.zip -d $HOME/.local/share/fonts
rm CascadiaCode.zip

## Install Oh-my-posh 
# https://ohmyposh.dev/docs/installation/linux
sudo curl -s https://ohmyposh.dev/install.sh | sudo bash -s

conda init bash
echo "alias ll='ls -alF'" >> ~/.bashrc
echo 'eval "$(oh-my-posh init bash --config /usr/local/share/omp-templates/almeida.omp.json)" ' >> ~/.bashrc
echo "conda activate azureai" >> ~/.bash_profile