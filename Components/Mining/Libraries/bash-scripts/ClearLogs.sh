#!/bin/bash
# ClearLogs
# 	Script used to remove excess log files in a mining folder.

# Recursively removes all files starting with 15 [unix timestamp]. More efficient solution later.
rm -rf 15*


# ATTEMPT 1: Possibly deprecate
# * Modeled after: 'find $(find /specificied/directory -d -name "[0-9][0-9][0-9]") -name "[E|P]" -exec rm -i {}''
find -name "[1]*" -exec rm -i {}
