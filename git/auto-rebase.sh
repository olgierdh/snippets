#!/bin/sh
echo "enter name of the branch to merge:"
read branchName

echo "enter master branch name:"
read masterBranchName

echo "enter merging commit name:"
read commitName

git checkout $branchName

export GIT_EDITOR="sed -i '2~1s/^pick/squash/;/^$/d'"
git rebase -i $masterBranchName

export GIT_EDITOR="sed -i '/^[ \t]*$/d;/\#/d;s/^\(.*\)/\t* \1/'"
git commit --amend

export GIT_EDITOR="sed -i '1 i\\$commitName\\'"
git commit --amend

export GIT_EDITOR="sed -i '1 a\\ \\'"
git commit --amend

git checkout 	$masterBranchName
git merge 	$branchName

