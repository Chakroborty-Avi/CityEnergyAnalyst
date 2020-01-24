"""
Updates CEA and GUI by checking GitHub releases
"""

import os
import re
import sys
import requests
import subprocess
import tempfile
from pyunpack import Archive
from packaging import version

GITHUB_REPO_URL = 'https://github.com/architecture-building-systems/CityEnergyAnalyst'
DOWNLOAD_URL_PREFIX = '{}/releases/latest/download'.format(GITHUB_REPO_URL)
VERSION_REGEX = r'(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:[0-9A-Za-z-]+)?'
DEPENDENCIES = 'Dependencies.7z'
GUI_FILE = 'win-unpacked.7z'  # For windows only


def get_cea_python_path():
    # For windows installed using installer
    # Assuming this script is found in the same directory as `Dependencies` which contains Python
    return os.path.abspath(os.path.join(os.path.dirname(__file__), 'Dependencies', 'Python', 'python'))


def get_gui_path():
    # For windows installed using installer
    # Assuming this script is found in the same directory as `win-unpacked`
    return os.path.abspath(os.path.join(os.path.dirname(__file__), 'win-unpacked'))


# Could also use PyPi API to get latest version on PyPi
# https://pypi.org/pypi/cityenergyanalyst/json
def fetch_online_version():
    """Get online version by extracting version number from GitHub redirect url"""
    r = requests.head("{}/releases/latest".format(GITHUB_REPO_URL))
    url = r.headers['Location']
    online_version = re.search(VERSION_REGEX, url).group(0)
    if not online_version:
        raise Exception('Could not retrieve online version.')
    return online_version


# Ignore for now
def download_dependencies():
    pass


def installed_as_editable(python_path):
    """
    Used to determine if CEA is installed as dev
    Developer version is installed as editable by installer
    """
    # Get site-packages from python path
    site_package = os.path.join(os.path.dirname(python_path), 'Lib', 'site-packages')
    egg_link = os.path.join(site_package, 'cityenergyanalyst' + '.egg-link')
    return os.path.isfile(egg_link)


def update_cea(python_path):
    print("\n### UPDATING CEA ###")
    download_dependencies()
    # Run pip to update CEA from PyPi
    pip_cmd = "{python} -m pip install -U cityenergyanalyst".format(python=python_path)
    print("Running `{}`".format(pip_cmd))
    subprocess.call(pip_cmd.split(" "))


def update_gui(output_directory):
    # Update CEA GUI
    print("\n### UPDATING GUI ###")
    # Get GUI path relative to python path (only true if folder structure holds)
    gui_url = '{}/{}'.format(DOWNLOAD_URL_PREFIX, GUI_FILE)
    temp_path = os.path.join(tempfile.gettempdir(), 'temp.7z')
    sys.stdout.write("Downloading GUI...")
    with open(temp_path, "wb") as f:
        r = requests.get(gui_url, stream=True)
        total_length = r.headers.get('content-length')
        downloaded_length = 0
        if total_length is None:  # no content length header
            f.write(r.content)
        else:
            total_length = int(total_length)
            for chunk in r.iter_content(chunk_size=1024 * 100):
                f.write(chunk)
                downloaded_length += len(chunk)
                sys.stdout.write("\rDownloading GUI... (%.2f%%)" % (100 * downloaded_length / total_length))
            print("\rDownloading GUI... (done!)  ")
    sys.stdout.write("Extracting GUI...")
    Archive(temp_path).extractall(output_directory)
    os.remove(temp_path)  # Cleanup
    print("\rExtracting GUI... (done!)")


def main():
    """
    Update CEA using GitHub latest release tag. CEA will be updated using `pip` and GUI will be downloaded from GitHub
    """

    python_path = get_cea_python_path()
    version_output = subprocess.check_output([python_path, '-m', 'cea.interfaces.cli.cli', '--version'])
    print(version_output)
    local_version = re.search(VERSION_REGEX, version_output).group(0)
    print("Checking latest version available online...")
    online_version = fetch_online_version()
    print("Version {} found.".format(online_version))
    # Check if online version is larger than local version
    if version.parse(online_version) > version.parse(local_version):
        if installed_as_editable(python_path):  # Should not `pip install cityenergyanalyst` if dev version is installed
            print("CEA installed as dev. Will only update CEA GUI. Run `git pull` to update CEA")
        else:
            update_cea(python_path)
        gui_path = get_gui_path()
        update_gui(os.path.dirname(gui_path))
        print("\nCEA updated to version {}".format(online_version))

    else:  # Do not do anything if no update available
        print("\nYou already have the latest version.")


if __name__ == '__main__':
    main()