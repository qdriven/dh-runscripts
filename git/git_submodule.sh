#! /bin/sh

echo "try to add git sub module: to existing project"
git submodule add $1 $2

# echo "remove local"
# git rm --cached <local path>

