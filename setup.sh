#! /usr/bin/env bash


# Assumes ~/bin is in $PATH 

# Assumes this script is run in same directory as $filename

# Absolute path of this script
ABSOLUTE_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/$(basename "${BASH_SOURCE[0]}")"

# Name of directory where script is
DIR=`dirname $ABSOLUTE_PATH`

TARGET_DIR="$HOME/bin"

#echo `dirname $ABSOLUTE_PATH`


FILENAME="timecard.py"
PROGRAM_NAME="timecard"

SCRIPT_PATH="$DIR/$FILENAME"

chmod +x $SCRIPT_PATH

# Put symlink in $dir

# TODO avoid overwriting if $PROGRAM_NAME already exists in directory

cd $TARGET_DIR
cp -s $SCRIPT_PATH $PROGRAM_NAME

