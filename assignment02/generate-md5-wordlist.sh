#!/bin/bash

pswdlist=($(cat xato-net-10-million-passwords-1000.txt))
length=${#pswdlist[@]}

outfile="megalist.txt"
outfile_md5="megalist_md5.txt"
echo -n "" > $outfile

for i in $( seq 0 $length ); do
    for j in $( seq 0 $length ); do
        pw1=${pswdlist[$i]}
        pw2=${pswdlist[$j]}
        pswd=$pw1$pw2
        qq=$(echo -n $pswd | md5sum | awk '{print $1}')
        echo Password: $pswd, md5\($pswd\) = $qq >> $outfile
        echo $qq >> $outfile_md5
    done
done
