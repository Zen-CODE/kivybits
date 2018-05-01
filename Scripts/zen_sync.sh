#! /bin/bash
SOURCE="./"
DEST='/media/richard/RICSTICK/My Documents/'

echo " ======================"
echo " = Zen Sync Documents ="
echo " ======================"
echo "Enter the source ($SOURCE) >"
read input_source
if [ "$input_source" = "" ];
then
    echo "Using default..."
else
    SOURCE=$input_source  
fi

echo "Enter the destination ($DEST) >"
read input_dest
if [ "$input_dest" = "" ];
then
    echo "Using default..."
else
    DEST=$input_dest 
fi

echo "Pushing from '$SOURCE' to '$DEST'"

echo "Flush file missing from the source (y/n)? >"
read FLUSH

if [ "$FLUSH" = "y" ];
then
    echo "Syncing and wiping...."
    ARGS="-ruv --no-perms --no-owner --no-group --delete"
else
    echo "Synching..."
    ARGS="-ruv --no-perms --no-owner --no-group"
fi
rsync $ARGS "$SOURCE" "$DEST"
