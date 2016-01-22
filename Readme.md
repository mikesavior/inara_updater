# Tools and scripts for Elite: Dangerous

This package provides a collection of scripts I have found useful for Elite: Dangerous.

### update_inara.py

The most useful tool here! update_inara will fetch your location and credit balance from E:D,
and update your inara.cz profile automatically.


### elite_info.py

elite_info fetches the user's credit balance and current location from the E:D Companion API,
and prints this information. With --dump, it will print *everything* returned by the Companion API.


### FreePIE

This directory contains scripts used with the FreePIE software. See FreePIE/Readme.md for details.


## Using the Python Scripts

### In Windows

Download and run the latest update_inara.exe from the [releases page](https://github.com/annabunches/ed_tools/releases/latest).


### In Linux

First, make sure you have the git submodules and the required python tools:

    git submodule init
    git submodule update
    cd elite_api
    git submodule init
    git submodule update
    cd ..
    pip install -r requirements.txt
    pip install -r elite_api/requirements.txt

Now, just run the scripts:

    ./update_inara.py
    ./elite_info.py
