#!/bin/bash
filetype=$2
if [ "$1" = "test" ]; then
    working_dir="$(pwd)/test"
else
    working_dir=$(pwd)
fi
subs=$(find $working_dir -type f -regex ".*S[0-9][0-9].*E[0-9][0-9].*$filetype$")
mov=$(find $working_dir -regex ".*S[0-9][0-9].*E[0-9][0-9].*[^$filetype]")

IFS=$'\n' subs=($(sort <<<"${subs[*]}"))
IFS=$'\n' mov=($(sort <<<"${mov[*]}"))
unset IFS

# Iterate over mov array
counter=0
for m in "${mov[@]}"; do
    echo "Renaming ${subs[counter]} to $m.srt"
    mv "${subs[counter]}" "$m.srt"
    counter=$((counter+1))
done
