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

# we assume that you have cloned specter-desktop in parallel with specterext-warden

cd specterext-warden

# Use the environment from specter-desktop
. ../specter-desktop/.env/bin/activate

#install additional requirements 
pip3.8 install -r requirements.txt 
#install all the compatible packages version using pip installation,if recieve uncompatible package warning.
pip3 install -e .

```
## Run server
``` bash
# Start specter
python3 -m cryptoadvance.specter server --config DevelopmentConfig --debug

```
## Screenshot
![Screenshot](https://user-images.githubusercontent.com/54116506/193618081-0f442b96-0636-49d6-8641-1df1ca4b3137.png)
![image](https://user-images.githubusercontent.com/54116506/193618327-63dcff08-e0e2-4747-b04b-8b19f4fa3139.png)
![Screenshot from 2022-08-26 13-34-56](https://user-images.githubusercontent.com/54116506/193618448-95f8bd72-fc59-494d-992a-ba8c74be3062.png)

## Contribution

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

We believe Open Source is the future of development for bitcoin. There is no other way when transparency and privacy are critical.

The code is not compiled and it can be easily audited. It can also be modified and distributed as anyone wishes.


