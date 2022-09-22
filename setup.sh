# Need install oh my fish
# To install it exec: curl -L https://get.oh-my.fish | fish

#!/bin/sh

printf "Write the name of the user: "
read -r user
sudo pacman-key --populate archlinux
clear

while true
do
  echo "What do you want to do?"
  select option in "Install nvidia drivers" "Install paru" "Install programs" "Install pip packages" "Install VimPlug" "Setup dotfiles" "Exit"
  do
    case $option in
      "Install nvidia drivers")
        sudo pacman -S nvidia-dkms nvidia-utils lib32-nvidia-utils nvidia-settings vulkan-icd-loader lib32-vulkan-icd-loader
        clear
        break;;
      "Install paru")
        git clone https://aur.archlinux.org/paru.git ~/paru
        cd ~/paru/ && makepkg -si
        rm -rf ~/paru/
        clear
        break;;
      "Install programs")
        sudo pacman -S pacman-contrib picom numlockx pcmanfm vifm ranger firefox tumbler ffmpegthumbnailer xarchiver nitrogen lxappearance-gtk3 rofi zathura zathura-pdf-poppler sxiv xfce4-screenshooter xsel nodejs npm exa neovim jdk8-openjdk alacritty geany python-pip neofetch htop gtop arc-gtk-theme papirus-icon-theme autopep8 mpv figlet bat fd gparted xfce4-power-manager light-locker lxsession ripgrep ttf-joypixels lm_sensors lib32-lm_sensors fzf kitty zsh zsh-autosuggestions zsh-history-substring-search zsh-syntax-highlighting fish pavucontrol pulseaudio stow
        paru -S nerd-fonts-ubuntu-mono etcher-bin breeze-snow-cursor-theme rar brave-bin dtrx librewolf-bin shell-color-scripts tela-circle-icon-theme-git simple-mtpfs nvim-packer-git advcpmv
        clear
        break;;
      "Install pip packages")
        sudo pip install psutil numpy pynvim jedi pylint ueberzug pillow
        clear
        break;;
      "Install VimPlug")
        curl -fLo ~/.config/nvim/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
        clear
        break;;
      "Setup dotfiles")
        curl -fsSL https://starship.rs/install.sh | bash
        git clone https://github.com/rupa/z/ ~/z/
        git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ~/powerlevel10k
        sudo cp -rf 00-keyboard.conf /etc/X11/xorg.conf.d/00-keyboard.conf
        sudo usermod --shell /bin/zsh {$user}
        mkdir ~/.cache/zsh/
        touch ~/.cache/zsh/history
        stow alacritty fish kitty neofetch picom qtile ranger rofi starship zathura zsh
        git clone https://github.com/alexanderjeurissen/ranger_devicons ~/.config/ranger/plugins/ranger_devicons
        clear
        break;;
      "Exit")
        echo "Done!!"
        exit;;
      *)
        echo "Intenta de nuevo"
    esac
  done
done
