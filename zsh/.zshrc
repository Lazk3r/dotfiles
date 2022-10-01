# Enable Powerlevel10k instant prompt. Should stay close to the top of ~/.zshrc.
# Initialization code that may require console input (password prompts, [y/n]
# confirmations, etc.) must go above this block; everything else may go below.
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

source ~/powerlevel10k/powerlevel10k.zsh-theme

# To customize prompt, run `p10k configure` or edit ~/.p10k.zsh.
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh

# History
HISTSIZE=10000000
SAVEHIST=10000000
HISTFILE=~/.cache/zsh/history

# Ignore case
zstyle ':completion:*' matcher-list '' 'm:{a-z}={A-Z}' '+m:{A-Z}={a-z}'

# # Basic auto/tab complete:
autoload -U compinit && compinit
zstyle ':completion:*' menu select
zmodload zsh/complist
compinit
_comp_options+=(globdots)		# Include hidden files.

source /usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh
source /usr/share/zsh/plugins/zsh-history-substring-search/zsh-history-substring-search.zsh
source /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh

source /usr/share/fzf/completion.zsh
source /usr/share/fzf/key-bindings.zsh

zstyle ':autocomplete:*' min-input 1

# key for history substring search
bindkey '^[[A' history-substring-search-up
bindkey '^[[B' history-substring-search-down
bindkey '^P' history-substring-search-up
bindkey '^N' history-substring-search-down

# Aliases
alias ..='cd ..'
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'
alias .....='cd ../../../..'
alias ......='cd ../../../../..'
alias cp='cp -i'
alias mv='mv -i'
alias rm='rm -i'
alias ls='exa -al --color=always --group-directories-first --icons' # preferred listing
alias la='exa -a --color=always --group-directories-first'  # all files and dirs
alias ll='exa -l --color=always --group-directories-first'  # long format
alias lt='exa -aT --color=always --group-directories-first' # tree listing
alias cl='clear'
alias grubupdate='sudo grub-mkconfig -o /boot/grub/grub.cfg' # Update Grub
alias v='~/.local/bin/lvim'
alias py='python'
alias fm='ranger'
alias bestmirrors='sudo reflector --latest 5 --country "United States",Canada --sort rate --save /etc/pacman.d/mirrorlist --protocol https --download-timeout 15'
alias react='npx create-react-app'
#   Pacman / Paru
alias pacs='sudo pacman -S'
alias pacr='sudo pacman -R'
alias y='paru'
alias ys='paru -S'
alias yss='paru -Ss'
alias fixpacman="sudo rm /var/lib/pacman/db.lck"
#   GIT
alias gs='git status'
alias gck='git checkout'
alias gbr='git branch'
alias ga='git add'
alias gcm='git commit -m'
alias gps='git push'
alias gpl='git pull'
alias gr='git restore'
alias lg='lazygit' # Lazygit

alias ssh='kitty +kitten ssh'
alias server='ssh myserveruser@192.168.1.100'

alias cp='cpg -g'
alias mv='mvg -g'

. ~/z/z.sh
