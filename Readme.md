# Command-line tools for Elite: Dangerous

Currently, this package provides two simple python scripts for Elite: Dangerous.

### elite_info.py

elite_info fetches the user's credit balance and current location from the E:D Companion API,
and prints this information. In the future it will be able to display additional data.

### update_inara.py

update_inara will fetch your location and credit balance from E:D,
and update your inara.cz profile automatically.


## Usage

Run one of the tools to create a blank config file, or copy the provided one into ~/.ed_tools/.
Provide your username and password in the config, then run either script again. It will prompt
you for a verification code. Check your inbox for this code. (you should only have to do this once)
