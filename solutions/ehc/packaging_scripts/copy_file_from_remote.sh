#!/usr/bin/env bash

REMOTE_SERVER_IP=$1 #192.168.1.246
REMOTE_PATH_TO_CONFIG=$2 #/root/automation/ehc/config
LOCAL_PATH_TO_CONFIG=$3 #/usr/lib/python2.7/site-packages/packaging_scripts/benson

user_name="root"
password="pancake"

function help()
{
    echo "usage:" 
    echo "    copy_file_from_remote.sh <ip for remote server> <path to config files in remote server> <path to store config in local server>"
    echo "example below will copy files from server 192.168.1.245 folder /root/automation/ehc/config to local /root/automation/ehc/config"
    echo "    copy_file_from_remote.sh 192.168.1.245 /root/automation/ehc/config /root/automation/ehc/config"
    echo "By default we use root/pancake as credential to ssh access remote machine."
}

function ensure_command_existence()
{
    command=$1
    echo "checking if command $command installed in local machine."
    if [ ! type -p "$command" &> /dev/null ]
    then
        echo "$command not installed, try using command: yum install $command -q to install it."
        yum install "$command" -q
        echo "$command has been installed into this machine."
    else
        echo "$command" is already installed.
    fi
}

function copy_from_remote()
{
    user_name=$1
    password=$2
    remote_ip=$3
    remote_path=$4
    local_path=$5
    ensure_command_existence "sshpass"
    echo "Started coping files from $remote_ip:$remote_path TO $local_path"
    echo Start to run command:sshpass -p "$password" scp -r "$user_name"@"$remote_ip":"$remote_path" "$local_path"
    sshpass -p "$password" scp -r "$user_name"@"$remote_ip":"$remote_path" "$local_path"
    echo "Completed file copy from $remote_ip:$remote_path."
}


if [ "$REMOTE_SERVER_IP" = "" ] || [ "$REMOTE_PATH_TO_CONFIG" = "" ] || [ "$LOCAL_PATH_TO_CONFIG" = "" ]; then
    echo "Please make sure you have correct arguments placed when calling script."
    help
    exit 1
fi

copy_from_remote "$user_name" "$password" "$REMOTE_SERVER_IP" "$REMOTE_PATH_TO_CONFIG" "$LOCAL_PATH_TO_CONFIG"

echo removing temp folder which only contains dump files
echo run command:rm -rf "$LOCAL_PATH_TO_CONFIG"/temp
rm -rf "$LOCAL_PATH_TO_CONFIG"/temp



