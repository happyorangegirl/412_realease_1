#!/bin/bash
LOG_FILE=/root/automation/ehc/logs/config.log

if [ $# -eq 7 ]
then

date +"%F %T ">> ${LOG_FILE}
date +"%F %T Taking the backup and Changing the hostname from $(hostname) to $1 ...">> ${LOG_FILE}

sed -i.bk "s/$(hostname)/$1/g" /etc/sysconfig/network

date +"%F %T ">> ${LOG_FILE}
date +"%F %T Backing up & Assigning the Static IP ...">> ${LOG_FILE}
date +"%F %T ">> ${LOG_FILE}

cp /etc/sysconfig/network-scripts/ifcfg-$2 /etc/sysconfig/network-scripts/$2.bk

cat <<EOF > /etc/sysconfig/network-scripts/ifcfg-$2

DEVICE=$2
BOOTPROTO=static
IPADDR=$3
NETMASK=$7
GATEWAY=$4
ONBOOT=yes
DNS1=$5
DNS2=$6
EOF

date +"%F %T Changing the dns ...">> ${LOG_FILE}
date +"%F %T ">> ${LOG_FILE}
cp -n /root/automation/ehc/schema/resolv.conf /etc/resolv.conf
# sed -i.bk "s/nameserver.*/nameserver $5/" /etc/resolv.conf
echo "nameserver "$5 >> /etc/resolv.conf
# sed -i.bk "s/nameserver.*/nameserver $6/" /etc/resolv.conf
echo "nameserver "$6 >> /etc/resolv.conf

date +"%F %T Adding $1 as hostname to the /etc/hosts file ..">> ${LOG_FILE}
date +"%F %T ">> ${LOG_FILE}
cp -n /root/automation/ehc/schema/hosts /etc/hosts
sed -i.bk "/$(hostname)$/d" /etc/hosts
echo "$3 $1" >> /etc/hosts

date +"%F %T Restarting the Network Service, Please connect it using the new IP Address if you are using ssh ...">> ${LOG_FILE}

service network restart
service network restart

else

echo "Usage: ip.sh <hostname> <interface> <ipaddress> <gateway> <dns1> <dns2> <netmask>"
echo "Example: ip.sh testname s 10.10.10.2 10.10.10.2 10.10.10.2 10.10.10.3 255.255.255.0"

fi