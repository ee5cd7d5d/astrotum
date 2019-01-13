#!/bin/bash

# This file is a wrapper for the tools GNU parallel and ImageMagick convert.
# It takes two arguments: new size like WIDTHxHEIGHT+Xoff+Yoff and target
# directory. It creates new cropped files with the names of the old ones and
# the new geometry.

# Created by: Pedro Rodriguez
# Date modified: 13.01.2019

function check_install() {
    if ! which $1 &> /dev/null; then
        echo -e "Command $1 not found! Install? (y/n) \c"
        read REPLY
        if [ "$REPLY" = "y" ]; then
            sys=$(cat /proc/version)
            case $sys in
                *ubuntu*)
                    sudo apt-get install $1
            esac
            case $sys in
                *arch*)
                    sudo pacman -S $1
            esac
        else
            exit 1
        fi
    fi
}

check_install convert
check_install parallel

parallel convert {} -crop $1 {.}_$1.fits ::: $2/*.fits
