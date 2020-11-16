#!/bin/bash

usage() {
	echo "usage: -i raw data directory"
	exit 1
}

if [ $# -ne 1 ]
then
	usage
fi


for file in $1/*
do 
	grep -E -i 'biden|trump' "$file" >> ../data/processed/out.json
done
