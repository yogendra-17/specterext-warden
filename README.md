# specterext-warden
Warden as an specter extension

[![GitHub release](https://img.shields.io/github/release/pxsocs/warden.svg)](https://github.com/yogendra-17/specterext-warden/releases/tag/Specterext-warden)
[![Open Source? Yes!](https://badgen.net/badge/Open%20Source%20%3F/Yes%21/blue?icon=github)](https://GitHub.com/pxsocs/warden/releases/)

### Requirements:

> 🐍 Python 3.8 

> [specter-desktop v1.12.0](https://github.com/cryptoadvance/specter-desktop/releases/tag/v1.12.0)

This app was built with a couple of goals:

- Easily track portfolio values in fiat.
- Monitors Wallets and Addresses for activity using your own node and notifies user of activity.
- Track your Bitcoin node status.

# INSTALLATION

```bash
git clone https://github.com/yogendra-17/specterext-warden.git

# we assume that you have cloned specter-desktop in parallel with amp-issuer

cd specter-desktop

# Use the environment from specter-desktop
. ../specter-desktop/.env/bin/activate

#install additional requirements 
pip3.8 install -r requirements.txt 
#install all the compatible packages version using pip installation,if recieve uncompatible package warning.
pip3 install -e .
# Start specter
python3 -m cryptoadvance.specter server --config DevelopmentConfig --debug
```
