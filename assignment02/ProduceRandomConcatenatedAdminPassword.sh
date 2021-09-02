#!/bin/bash
	pswdlist=($(cat xato-net-10-million-passwords-1000.txt))
	length=${#pswdlist[@]}
	RANDOM=$$$(date +%s)
	rand1=$[$RANDOM % length]
	rand2=$[$RANDOM % length]
	pw1=${pswdlist[$rand1]}
	pw2=${pswdlist[$rand2]}
	pswd=$pw1$pw2
	qq=$(echo -n $pswd | md5sum | awk '{print $1}')
	echo Password: $pswd, md5\($pswd\) = $qq