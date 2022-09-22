#!/bin/sh

n=$(( $RANDOM % 6 ))

[ $n -eq 0 ] && fortune | cowsay -f tux
[ $n -eq 1 ] && fortune | cowsay -f dragon
[ $n -eq 2 ] && fortune | cowsay -f bud-frogs
[ $n -eq 3 ] && fortune | cowsay -f koala
[ $n -eq 4 ] && fortune | cowsay -f kitty
[ $n -eq 5 ] && fortune | cowsay -f turtle
