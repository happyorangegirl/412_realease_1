#!/usr/bin/env bash
# Script used to read Property File
XML_FILE=/root/automation/ehc/logs/config.xml
XSL_FILE=/root/automation/ehc/schema/config.xsl
FILE_NAME=/root/automation/ehc/logs/config.cfg
NETWORK_SH=/root/automation/ehc/bin/network_setting.sh
LOG_FILE=/root/automation/ehc/logs/config.log
AUTO_CONFIG_FILE=/root/automation/ehc/config/generic.yaml
AUTO_CONFIG_FILE_TEMPLATE=/root/automation/ehc/config/config.yaml.template
ETHERNET_FILE=/etc/sysconfig/network-scripts/ifcfg-eno16777984
FIRST_LAUNCH_FILE=/root/automation/ehc/logs/old
if [ -f ${FIRST_LAUNCH_FILE} ]; then
   echo "Not first launch, no need to run this scrip again."
   exit
fi
rm -f ${LOG_FILE}
# Get vApp properties
date +"%F %T Getting vApp properties..." >> ${LOG_FILE}
vmtoolsd --cmd "info-get guestinfo.ovfEnv">${XML_FILE}
# Parse xml file to cfg file
date +"%F %T Converting xml file to cfg file..." >> ${LOG_FILE}
/usr/bin/xsltproc ${XSL_FILE} ${XML_FILE} > ${FILE_NAME}
# IP address 
ip_address=`cat ${FILE_NAME} | grep -i IP_Address | cut -f2 -d'|'`
date +"%F %T Setting IP address to "${ip_address}  >> ${LOG_FILE}
echo "IP:"${ip_address}
# Gateway
gateway=`cat ${FILE_NAME} | grep -i Gateway | cut -f2 -d'|'`
date +"%F %T Setting gateway to "${gateway} >> ${LOG_FILE}
# Network mask
netmask=`cat ${FILE_NAME} | grep -i Network_Mask | cut -f2 -d'|'`
date +"%F %T Setting network mask to "${netmask} >> ${LOG_FILE}
# Primary DNS
dns1=`cat ${FILE_NAME} | grep -i Primary_DNS_Server | cut -f2 -d'|'`
date +"%F %T Setting primary DNS to "${dns1} >> ${LOG_FILE}
# Secondary DNS
dns2=`cat ${FILE_NAME} | grep -i Secondary_DNS_Server | cut -f2 -d'|'`
date +"%F %T Setting secondary DNS to "${dns2} >> ${LOG_FILE}
date +"%F %T apply the setting to machine..." >> ${LOG_FILE}
inte=`ip ntable | grep dev |sort|uniq|sed -e 's/^.*dev //;/^lo/d'`
echo ${inte}
date +"%F %T Getting the interface name "${inte}>>${LOG_FILE}
if [ -e "$ETHERNET_FILE" ]; then
  mv $ETHERNET_FILE /etc/sysconfig/network-scripts/ifcfg-${inte}
  service network restart
fi
${NETWORK_SH} ehc_automation ${inte} ${ip_address} ${gateway} ${dns1} ${dns2} ${netmask}
date +"%F %T configure vRA in automation..."
vra_address=`cat ${FILE_NAME} | grep -i vRA_IP/FQDN | cut -f2 -d'|'`
vra_username=`cat ${FILE_NAME} | grep -i vRA_Username | cut -f2 -d'|'`
vra_password=`cat ${FILE_NAME} | grep -i vRA_Password | cut -f2 -d'|'`
date +"%F %T configure vRO in automation..."
vro_address=`cat ${FILE_NAME} | grep -i vRO_IP/FQDN | cut -f2 -d'|'`
vro_username=`cat ${FILE_NAME} | grep -i vRO_Username | cut -f2 -d'|'`
vro_password=`cat ${FILE_NAME} | grep -i vRO_Password | cut -f2 -d'|'`
date +"%F %T configure tenant in automation..."
tenant=`cat ${FILE_NAME} | grep -i Tenant | cut -f2 -d'|'`
business_group=`cat ${FILE_NAME} | grep -i Business_Group | cut -f2 -d'|'`
domain=`cat ${FILE_NAME} | grep -i Domain | cut -f2 -d'|'`
date +"%F %T Reset configuration file..."
yes|cp -rf ${AUTO_CONFIG_FILE_TEMPLATE} ${AUTO_CONFIG_FILE}
date +"%F %T Setting vRA address to "${vra_address} >> ${LOG_FILE}
sed -i "s#%vra_address%#${vra_address}#g" ${AUTO_CONFIG_FILE}
date +"%F %T Setting vRA username to "${vra_username} >> ${LOG_FILE}
sed -i "s#%vra_username%#${vra_username}#g" ${AUTO_CONFIG_FILE}
date +"%F %T Setting vRA user password to "${vra_password} >> ${LOG_FILE}
sed -i "s#%vra_password%#${vra_password}#g" ${AUTO_CONFIG_FILE}

date +"%F %T Setting vRO address to "${vro_address} >> ${LOG_FILE}
sed -i "s#%vro_address%#${vro_address}#g" ${AUTO_CONFIG_FILE}
date +"%F %T Setting vRO username to "${vro_username} >> ${LOG_FILE}
sed -i "s#%vro_username%#${vro_username}#g" ${AUTO_CONFIG_FILE}
date +"%F %T Setting vRO user password to "${vro_password} >> ${LOG_FILE}
sed -i "s#%vro_password%#${vro_password}#g" ${AUTO_CONFIG_FILE}

date +"%F %T Setting Tenant to "${tenant} >> ${LOG_FILE}
sed -i "s#%tenant%#${tenant}#g" ${AUTO_CONFIG_FILE}
date +"%F %T Setting Business Group to "${business_group} >> ${LOG_FILE}
sed -i "s#%business_group%#${business_group}#g" ${AUTO_CONFIG_FILE}
date +"%F %T Setting Domain to "${domain} >> ${LOG_FILE}
sed -i "s#%domain%#${domain}#g" ${AUTO_CONFIG_FILE}
echo -n "" > ${FIRST_LAUNCH_FILE}
date +"%F %T done" >> ${LOG_FILE}