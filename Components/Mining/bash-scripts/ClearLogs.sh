#!/bin/bash
# ClearLogs
# 	Script used to remove excess log files in a mining folder.
# * Modeled after: 'find $(find /specificied/directory -d -name "[0-9][0-9][0-9]") -name "[E|P]" -exec rm -i {}''
find -name "[1]*" -exec rm -i {}