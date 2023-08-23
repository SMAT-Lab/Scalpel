#!/usr/bin/env bash
#encoding=utf8

function echo_block() {
    echo "----------------------------"
    echo $1
    echo "----------------------------"
}

function check_installed_pip() {
   ${PYTHON} -m pip > /dev/null
   if [ $? -ne 0 ]; then
        echo_block "Installing Pip for ${PYTHON}"
        curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
        ${PYTHON} get-pip.py
        rm get-pip.py
   fi
}

# Check which python version is installed
function check_installed_python() {
    if [ -n "${VIRTUAL_ENV}" ]; then
        echo "Please deactivate your virtual environment before running setup.sh."
        echo "You can do this by running 'deactivate'."
        exit 2
    fi

    for v in 10 9 8
    do
        PYTHON="python3.${v}"
        which $PYTHON
        if [ $? -eq 0 ]; then
            echo "using ${PYTHON}"
            check_installed_pip
            return
        fi
    done

    echo "No usable python found. Please make sure to have python3.8 or newer installed."
    exit 1
}

function updateenv() {
    echo_block "Updating your virtual env"
    if [ ! -f .env/bin/activate ]; then
        echo "Something went wrong, no virtual environment found."
        exit 1
    fi
    source .env/bin/activate
    SYS_ARCH=$(uname -m)
    echo "pip install in-progress. Please wait..."
    ${PYTHON} -m pip install --upgrade pip wheel setuptools
    REQUIREMENTS=requirements.txt

    ${PYTHON} -m pip install --upgrade -r ${REQUIREMENTS}
    if [ $? -ne 0 ]; then
        echo "Failed installing dependencies"
        exit 1
    fi
    ${PYTHON} -m pip install -e .
    if [ $? -ne 0 ]; then
        echo "Failed installing Scalpel"
        exit 1
    fi

    echo_block "Updating pre_commit scripts"
    ${PYTHON} -m pre_commit install
    if [ $? -ne 0 ]; then
        echo "Failed installing pre-commit"
        exit 1
    fi

    echo "pip install completed"
}

# Install bot Debian_ubuntu
function install_debian() {
    sudo apt-get update
    sudo apt-get install -y gcc build-essential autoconf libtool pkg-config make wget git curl $(echo lib${PYTHON}-dev ${PYTHON}-venv)
}

# Install bot RedHat_CentOS
function install_redhat() {
    sudo yum update
    sudo yum install -y gcc gcc-c++ make autoconf libtool pkg-config wget git $(echo ${PYTHON}-devel | sed 's/\.//g')
}

# Upgrade Scalpel
function update() {
    git pull
    updateenv
}

function check_git_changes() {
    if [ -z "$(git status --porcelain)" ]; then
        echo "No changes in git directory"
        return 1
    else
        echo "Changes in git directory"
        return 0
    fi
}

# Reset Develop or Stable branch
function reset() {
    echo_block "Resetting branch and virtual env"

    if [ "1" == $(git branch -vv |grep -cE "\* develop|\* stable") ]
    then
        if check_git_changes; then
            read -p "Keep your local changes? (Otherwise will remove all changes you made!) [Y/n]? "
            if [[ $REPLY =~ ^[Nn]$ ]]; then

                git fetch -a

                if [ "1" == $(git branch -vv | grep -c "* develop") ]
                then
                    echo "- Hard resetting of 'develop' branch."
                    git reset --hard origin/develop
                elif [ "1" == $(git branch -vv | grep -c "* stable") ]
                then
                    echo "- Hard resetting of 'stable' branch."
                    git reset --hard origin/stable
                fi
            fi
        fi
    else
        echo "Reset ignored because you are not on 'stable' or 'develop'."
    fi

    if [ -d ".env" ]; then
        echo "- Deleting your previous virtual env"
        rm -rf .env
    fi
    echo
    ${PYTHON} -m venv .env
    if [ $? -ne 0 ]; then
        echo "Could not create virtual environment. Leaving now"
        exit 1
    fi
    updateenv
}

function install() {

    echo_block "Installing mandatory dependencies"

    # if [ "$(uname -s)" == "Darwin" ]; then
    #     echo "macOS detected. Setup for this system in-progress"
    #     install_macos
    if [ -x "$(command -v apt-get)" ]; then
        echo "Debian/Ubuntu detected. Setup for this system in-progress"
        install_debian
    # elif [ -x "$(command -v yum)" ]; then
    #     echo "Red Hat/CentOS detected. Setup for this system in-progress"
    #     install_redhat
    else
        echo "This script does not support your OS."
        echo "If you have Python version 3.8 - 3.10, pip, virtualenv you can continue."
        echo "Wait 10 seconds to continue the next install steps or use ctrl+c to interrupt this shell."
        sleep 10
    fi
    echo
    reset
}

function help() {
    echo "usage:"
    echo "	-i,--install    Install Scalpel from scratch"
    echo "	-u,--update     Command git pull to update."
    echo "	-r,--reset      Hard reset your develop/stable branch."
}

# Verify if 3.8+ is installed
check_installed_python

case $* in
--install|-i)
install
;;
--update|-u)
update
;;
--reset|-r)
reset
;;
*)
help
;;
esac
exit 0
