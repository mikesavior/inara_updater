# Tools and scripts

This package provides a collection of scripts I have found useful for Elite: Dangerous.

### update_inara.py

update_inara will fetch your location and credit balance from E:D,
and update your inara.cz profile automatically. There is also a Windows binary available. (soon)


### elite_info.py

elite_info fetches the user's credit balance and current location from the E:D Companion API,
and prints this information. With --dump, it will print *everything* returned by the Companion API.


### FreePIE

This directory contains scripts used with the FreePIE software. See FreePIE/Readme.md for details.


## Using the Python Scripts

### In Linux

First, make sure you have the git submodules and the required python tools:

    git submodule init
    git submodule update
    pip install -r requirements.txt
    pip install -r inara/requirements.txt

Now, just run the script:

    ./update_inara.py

### In Windows

Download and run update_inara.exe. (coming soon)
