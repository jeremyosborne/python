"""
Attempt to make life easy by exporting boolean variables which determines
which OS we're on.
"""

# TODO: Test that whenever this is run that only one variable is set
# to true. It should never be possible to be on two different OSes at
# runtime.

import platform

if any(platform.mac_ver()):
    is_mac = True
else:
    is_mac = False

if any(platform.win32_ver()):
    is_win = True
else:
    is_win = False

if any(platform.linux_distribution()):
    is_linux = True
else:
    is_linux = False