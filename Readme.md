# inara.cz updater

The inara updater will fetch your location and credit balance from E:D,
and update your inara.cz profile automatically.

## Usage

### In Windows

Download and run the latest inara_updater.exe from the [releases page](https://github.com/annabunches/inara_updater/releases/latest).


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

Now, just run the script:

    ./update_inara.py
