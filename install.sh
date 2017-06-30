#!/bin/bash
DIR=$( dirname "${BASH_SOURCE[0]}" )
cd $DIR

function checkerror() {
  if [ $? -ne 0 ]; then
    echo "ERROR - Something is wrong - $1"
    exit 1
  fi
}

echo "detecting OS..."
if ! echo $OSTYPE | grep -i linux; then
  echo "this program only works in a linux system"
  exit 1
fi

echo "ok..."

if [ $UID -ne 0 ]; then
  echo "This program needs root privileges"
  exit 1
fi

echo "Checking if python3 is installed..."
if ! /usr/bin/env python3 --version; then
  distro=$(cat /etc/os-release) &> /dev/null
  if (echo $distro | egrep -i "(ubuntu|debian)" &> /dev/null); then
    echo "python3 not found"
    echo "Trying to install python3"
    apt update &> /dev/null && apt install -y python3 &> /dev/null
    checkerror
  else
    echo "This operative system don't looks an ubuntu or debian and don't have python3 installed"
    echo "You must install python3 manually before install this program"
    exit 1
  fi
else
  echo "ok... python3 installed"
fi

echo "trying to install optional dependencies"
if ! which pip3; then
  distro=$(cat /etc/os-release)
  if (echo $distro | egrep -i "(ubuntu|debian)" &> /dev/null); then
    echo "trying to install pip"
    apt update &> /dev/null && apt install -y python3-pip qt5-default libqt5webkit5-dev \
    build-essential python-lxml xvfb &> /dev/null
    checkerror
  else
    echo "this operative system don't looks an ubuntu or debian"
    echo "you must install dryscrape library from pip manually before install this program"
  fi
fi
pip3 install dryscrape &> /dev/null
if [ $? -ne 0 ]; then echo "WARNING - Instalation of dryscrape library failed"; fi


if which ace; then
  while true; do
      read -p "ace program exists, do you want overwrite it? (y/n)" yn
      case $yn in
          [Yy]* ) cp ace.py /usr/bin/ace; echo "install complete"; exit 0;;
          [Nn]* ) exit 0;;
          * ) echo "Please answer yes or no.";;
      esac
  done
else
  echo "installing ace..."
  mkdir -p /etc/ace
  checkerror
  cp ./ace.py /usr/bin/ace
  checkerror
  if [ ! -f /etc/ace/default.cfg ]; then
    cp ./default.cfg /etc/ace/default.cfg
    checkerror
  fi
  echo "install complete" && exit 0;
fi
