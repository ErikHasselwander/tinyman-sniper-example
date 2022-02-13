# tinyman-sniper-example
Here is some example code of how one could implement a tinyman sniper.
This is not to be used in production, it is only an example to give inspiration.

Feel free to star and fork this code as much as you want, idk how to do licenses and shit but this code is free for use by everyone!

# Instructions
1. Clone this repo and install the requirements, `pip install -r requirements.txt`
2. Enter your mnemonic into `private.py`
3. (Optional) Enter an node-info in `config/config.py`. Defaults to algonode.io
4. Create a config file, there is a self-explaining config in `config/TEMPLATE.yaml`.
5. Run the script! Ran by `python3 single_snipe.py TEMPLATE`  for the configuration in set 4. The first argument is the name of the config, without the .yaml. All configs should be .yaml files tho.
    - I just use `py sing...`, but I think python3 is correct? idk? Windows user btw
6. Dont blame me when shit doesnt work! This is just for educational purposes, it is free for everyone to play around with, but I bare no responsibility. Always DYOR and lots and lots of testing!

# Notes
The script automatically opts in to the asset, but not to tinyman. So be sure to do this manually, or just add it into the code, and if you do add it feel free to open a PR!