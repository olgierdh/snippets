#!/bin/bash

tag_name=$(echo "$1" | sed -e 's/^\([a-z]*\)-\(.*\)/\1\/\2/g')

echo "checkout to $1..."
git fetch origin
git checkout $1
echo "pulling changes..."
git pull origin $1
echo "tagging the branch with the name $tag_name..."
git tag $tag_name
echo "checkouting the master..."
git checkout master
echo "delete local branch..."
git branch -D $1
echo "delete remote branch..."
git push origin :$1
echo "push tags..."
git push --tags
echo "done"

