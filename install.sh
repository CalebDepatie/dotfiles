#!/bin/bash
# Initial setup before the terminal based installer can run

# Check if script is root
if [[ $EUID -ne 0 ]]; then
  echo "Installer must be run as root!"
  exit 1
fi

# Check OS to use the proper install
if [[ "$OSTYPE" == 'linux-gnu' ]]; then
  INSTALLER=apt
else
  echo "Undefined OS. Please update installer."
fi

# Initial setup commands to ensure everything will work
$INSTALLER update
$INSTALLER upgrade
$INSTALLER install python3

# Run python installer script
python3 installer.py
