#!/usr/bin/env bash
######## variable for web ui code path ######
ORIGINAL_WEB_DIR_PATH=/usr/lib/python2.7/site-packages/web/
TARGET_WEB_PATH=/root/automation/web/
########end local arguments##################
echo "Start to update Web UI..."
yes|cp -fr $ORIGINAL_WEB_DIR_PATH $TARGET_WEB_PATH
echo "Done with updating Web UI..."