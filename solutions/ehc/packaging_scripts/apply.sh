#!/usr/bin/env bash


########remote mode arguments########
REMOTE_SERVER_IP=$1 #192.168.1.246
REMOTE_PATH_TO_CONFIG=$2 #/root/automation/ehc/config
LOCAL_PATH_TO_CONFIG=$3 #/root/automation/ehc/config
USER_NAME="root"
PASSWORD="pancake"

REMOTE_MODE=false
override_local_config_when_copy_from_remote=false
########end remote mode arguments########

########local arguments########
ORIGINAL_CONFIG_PATH=/usr/lib/python2.7/site-packages/ehc_e2e/conf/
REFERENCE_CONFIG_PATH=/root/automation/ehc/config/
BACKUP_CONFIG_FOLDER=config_backup

ORIGINAL_SCENARIO_CONFIG_PATH=/usr/lib/python2.7/site-packages/ehc_e2e/conf/scenario_conf
REFERENCE_SCENARIO_CONFIG_PATH=/root/automation/ehc/config/scenario_conf
BACKUP_SCENARIO_CONFIG_FOLDER=scenario_config_backup
########end local arguments########

UPDATED_WORKFLOW_YAML_RESULT_PATH=/root/automation/ehc/config/
UPDATED_SCENARIO_YAML_RESULT_PATH=/root/automation/ehc/config/scenario_conf

CONFIG_FILE=/root/automation/ehc/logs/config.cfg
ip_address=`cat ${CONFIG_FILE} | grep -i IP_Address | cut -f2 -d'|'`

function help()
{
    echo "apply.sh has two mode, if you don't specify any parameters, it will run under local mode. if you have three"
    echo "parameters specified, it will run under remote mode."
    echo "remote mode usage:"
    echo "    apply.sh <ip for remote server> <path to config files in remote server> <path to store copied config in local server>"
    echo "example below will copy files from server 192.168.1.245 folder /root/automation/ehc/config to local /root/automation/ehc/config"
    echo "    apply.sh 192.168.1.245 /root/automation/ehc/config /root/automation/ehc/config"
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

function normalize_path()
{
    original_path_str=$1
    if [ "{$original_path_str: :-1}" != "/" ]
    then
        original_path_str="$original_path_str/"
    fi

    echo $original_path_str
}

function copy_from_remote()
{
    user_name=$1
    password=$2
    remote_ip=$3
    remote_path=$4
    remote_path=$(normalize_path "$remote_path")
    local_path=$5
    ensure_command_existence "sshpass"

    # pay attention to scp command parameters. scp -p user@ip:pathname/* will copy the fist level files under pathname.
    echo "Started coping files from $remote_ip:$remote_path TO $local_path"
    echo Start to run command:sshpass -p "$password" scp -p "$user_name"@"$remote_ip":"$remote_path*" "$local_path"
    sshpass -p "$password" scp -p "$user_name"@"$remote_ip":"$remote_path*" "$local_path"
    echo "Completed file copy from $remote_ip:$remote_path."
}

function update_yaml_config()
{
    original_config_path=$1
    reference_config_path=$2
    backup_config_folder=$3
    update_yaml_result_path=$4
    file_catagory=$5
    #yamlupdater will handle the anchor value update during yaml file update.
    echo "Start to update $file_catagory configuration files..."
    echo python /usr/lib/python2.7/site-packages/yamlupdater/yamlupdater.py -o "$original_config_path" -r "$reference_config_path" -b "$backup_config_folder" -u "$update_yaml_result_path"
    python /usr/lib/python2.7/site-packages/yamlupdater/yamlupdater.py -o "$original_config_path" -r "$reference_config_path" -b "$backup_config_folder" -u "$update_yaml_result_path"
    echo "Done with updating $file_catagory configuration files..."
    echo "Checking if there is error occurred during $file_catagory config file update."
    if grep -E "^\[ERROR\]|Error:" log_yamlupdater.log; then
        echo "There is error found during running yamlupdater!"
    else
        echo "No error found during running yamlupdater!"
    fi

    /bin/cp -f log_yamlupdater.log log_yamlupdater_$file_catagory.log
}


if [ "$REMOTE_SERVER_IP" = "" ] || [ "$REMOTE_PATH_TO_CONFIG" = "" ] || [ "$LOCAL_PATH_TO_CONFIG" = "" ]
then
    echo "If you want to upgrade config files based on files from remote server, Please make sure you have correct arguments placed when calling script."
    echo "otherwise apply.sh will be running in local mode."
    help
else
    echo "apply.sh will be running in remote mode."
    remote_mode=true
fi

########update robot files########
rm -f /root/automation/ehc/workflows/Planned_Migration_DR2S.robot
echo "Start to update RP4VM workflows..."
/bin/cp -fr /usr/lib/python2.7/site-packages/ehc_e2e/robot_tests/RP4VM_Workflows.robot /root/automation/ehc/workflows
echo "Done with updating RP4VM workflows..."
echo "Start to update Basic workflows..."
/bin/cp -fr /usr/lib/python2.7/site-packages/ehc_e2e/robot_tests/Basic_Workflows.robot /root/automation/ehc/workflows
echo "Done with updating Basic workflows..."
echo "Start to update Failover workflows..."
/bin/cp -fr /usr/lib/python2.7/site-packages/ehc_e2e/robot_tests/Failover_Workflows.robot /root/automation/ehc/workflows
echo "Done with updating Failover workflows..."
echo "Start to update Planned migration workflows..."
/bin/cp -fr /usr/lib/python2.7/site-packages/ehc_e2e/robot_tests/Planned_Migration_Workflows.robot /root/automation/ehc/workflows
echo "Done with updating Planned migration workflows..."
echo "Start to update robot file for Scenarios..."
/bin/cp -fr /usr/lib/python2.7/site-packages/ehc_e2e/robot_tests/scenarios/Basic_Verification_Scenarios.robot /root/automation/ehc/scenarios
/bin/cp -fr /usr/lib/python2.7/site-packages/ehc_e2e/robot_tests/scenarios/resources/ehc.robot /root/automation/ehc/resources
echo "Done with updating robot file for Scenarios..."

########end update robot files########

########update utility bin########
echo "Start to update autocli command line..."
/bin/cp -fr /usr/lib/python2.7/site-packages/autocli/EHCAutoCLI.py /root/automation/ehc/bin
echo "Done update autocli command line..."
echo "start to update autocli listener..."
/bin/cp -fr /usr/lib/python2.7/site-packages/autocli/EHCAutoCLIListener.py /usr/lib/python2.7/site-packages/
echo "Done update autocli listener EHCAutoCLIListener..."
echo "Start to update dump inspector utility tool..."
if ! grep -q "autodebug" ~/.bashrc ; then
    echo "applying the autodebug tool..."
    echo "alias autodebug='python /root/automation/ehc/bin/dump_inspector.py'" >> ~/.bashrc
fi
/bin/cp -fr /usr/lib/python2.7/site-packages/dumpinspector/dump_inspector.py /root/automation/ehc/bin
echo "Updating web ui..."
/bin/cp -fr /usr/lib/python2.7/site-packages/web/ehc_web/ehc/api /root/automation/web/web/ehc_web/ehc
/bin/cp -fr /usr/lib/python2.7/site-packages/web/ehc_web/ehc/ui /root/automation/web/web/ehc_web/ehc
/bin/cp -fr /root/automation/web/web/ehc_web/ehc/ui/dist/js/dashboard.min.js.template /root/automation/web/web/ehc_web/ehc/ui/dist/js/dashboard.min.js
/bin/cp -fr /root/automation/web/web/ehc_web/ehc/ui/dist/templates/main/Intro.htm.template /root/automation/web/web/ehc_web/ehc/ui/dist/templates/main/Intro.htm
sed -i "s#%ip_address%#${ip_address}#g" /root/automation/web/web/ehc_web/ehc/ui/dist/templates/main/Intro.htm
sed -i "s#%ip_address%#${ip_address}#g" /root/automation/web/web/ehc_web/ehc/ui/dist/js/dashboard.min.js
echo "set IP:" ${ip_address} "to dashboard.min.js"
echo "Done update web ui"
########end update utility bin########

########copy yaml config files from remote server########
if [ "$REMOTE_MODE" = true ]
then
    copy_from_remote "$USER_NAME" "$PASSWORD" "$REMOTE_SERVER_IP" "$REMOTE_PATH_TO_CONFIG" "$LOCAL_PATH_TO_CONFIG"
    if [ "$LOCAL_PATH_TO_CONFIG" = "$REFERENCE_CONFIG_PATH" ]
    then
        override_local_config_when_copy_from_remote=true
    else
        REFERENCE_CONFIG_PATH="$LOCAL_PATH_TO_CONFIG"
    fi
fi
########end copy yaml config files from remote server########

#yamlupdater will handle the anchor value update during yaml file update.
update_yaml_config $ORIGINAL_CONFIG_PATH $REFERENCE_CONFIG_PATH $BACKUP_CONFIG_FOLDER $UPDATED_WORKFLOW_YAML_RESULT_PATH 'Workflow'
update_yaml_config $ORIGINAL_SCENARIO_CONFIG_PATH $REFERENCE_SCENARIO_CONFIG_PATH $BACKUP_SCENARIO_CONFIG_FOLDER $UPDATED_SCENARIO_YAML_RESULT_PATH 'Scenario'

if [ "$remote_mode" = true ]
then
    echo "The apply.sh run completed under remote mode."
    echo "The config files were copied from $REMOTE_SERVER_IP:$REMOTE_PATH_TO_CONFIG to local's $LOCAL_PATH_TO_CONFIG before running yamlupdater.py"
    if [ "$override_local_config_when_copy_from_remote" = true ]
    then
        echo "Copied files from remote server:$REMOTE_SERVER_IP override local files under $REFERENCE_CONFIG_PATH"
    fi
else
    echo "The apply.sh run completed under local mode."
fi

echo "Workflow Yaml config files were updated by referencing values from files under $REFERENCE_CONFIG_PATH and placed under $UPDATED_WORKFLOW_YAML_RESULT_PATH"
echo "Scenario Yaml config files were updated by referencing values from files under $REFERENCE_SCENARIO_CONFIG_PATH and placed under $UPDATED_SCENARIO_YAML_RESULT_PATH"
echo "Update packaging script"
/bin/cp -fr /usr/lib/python2.7/site-packages/packaging_scripts/*.sh /root/automation/ehc/bin
