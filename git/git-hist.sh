#!/bin/bash

OPTIND=1

usage() { echo "Usage: $0 -s <YYYY-MM-DDTHH:MM:SS[TIME ZONE]> [-h (help)] [-u <date until> (By default this is an actual date)]" 1>&2; exit 1;  }

since=""
until=`date +"%Y-%m-%dT%H:%M:%S%z"`

echo $NOW

!(($#)) && usage 

while getopts "h?s:u::" opt; do
    case "$opt" in
    h|\?)
        usage
        exit 0
        ;;
    s) since=$OPTARG
        ;;
    u) until=$OPTARG
        ;;
    *) usage
        ;;
    esac
done

git log --pretty=oneline --merges --first-parent --format="%C(auto) %h %C(green) %an %C(reset) %ad %C(reset) %s" --since="$since" --until="$until"
