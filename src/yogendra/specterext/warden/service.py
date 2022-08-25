# print(f"WARDD: {dir(app.warden_specter)=}\n\n")
# WARDD: what's app.warden_specter used for and where's it defined?
# is it called specter just to keep variables in the namespace?
# or does the specter object has methods and all
import cryptoadvance
from yaspin import yaspin
#wdd: temporarility for debugging
import inspect
import logging
import subprocess
import configparser
import os
import sys
import atexit
import warnings
import socket
import emoji
import time
import sqlite3
import requests



from cryptoadvance.specter.services.service import Service, devstatus_alpha, devstatus_prod, devstatus_beta
# A SpecterError can be raised and will be shown to the user as a red banner
from cryptoadvance.specter.specter_error import SpecterError
from flask import current_app as app
from cryptoadvance.specter.wallet import Wallet
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager, current_user
from .diags import internet_connected
from .ansi_management import (warning, success, error, info, clear_screen,
                             muted, yellow, blue)
from packaging import version


logger = logging.getLogger(__name__)



def check_cryptocompare():
    from .utils import pickle_it

    with yaspin(text="Testing price grab from Cryptocompare",
                color="green") as spinner:
        data = {'Response': 'Error', 'Message': None}
        try:
            api_key = pickle_it('load', 'cryptocompare_api.pkl')
            if api_key != 'file not found':
                baseURL = (
                    "https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC"
                    + "&tsyms=USD&api_key=" + api_key)
                req = requests.get(baseURL)
                data = req.json()
                btc_price = (data['DISPLAY']['BTC']['USD']['PRICE'])
                spinner.text = (success(f"BTC price is: {btc_price}"))
                spinner.ok("✅ ")
                pickle_it('save', 'cryptocompare_api.pkl', api_key)
                return
            else:
                data = {'Response': 'Error', 'Message': 'No API Key is set'}
        except Exception as e:
            data = {'Response': 'Error', 'Message': str(e)}
            logging.error(data)

        try:
            if data['Response'] == 'Error':
                spinner.color = 'yellow'
                spinner.text = "CryptoCompare Returned an error " + data[
                    'Message']
                # ++++++++++++++++++++++++++
                #  Load Legacy
                # ++++++++++++++++++++++++++
                try:
                    # Let's try to use one of the
                    # legacy api keys stored under cryptocompare_api.keys file
                    # You can add as many as you'd like there
                    filename = 'warden/static/cryptocompare_api.keys'
                    file = open(filename, 'r')
                    for line in file:
                        legacy_key = str(line)

                        spinner.text = (
                            warning(f"Trying different API Keys..."))

                        baseURL = (
                            "https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC"
                            + "&tsyms=USD&api_key=" + legacy_key)

                        try:
                            data = None
                            logging.debug(f"Trying API Key {legacy_key}")
                            request = requests.get(baseURL)
                            data = request.json()
                            btc_price = (
                                data['DISPLAY']['BTC']['USD']['PRICE'])
                            spinner.text = (
                                success(f"BTC price is: {btc_price}"))
                            spinner.ok("✅ ")
                            logging.debug(f"API Key {legacy_key} Success")
                            pickle_it('save', 'cryptocompare_api.pkl',
                                      legacy_key)
                            return
                        except Exception as e:
                            logging.debug(f"API Key {legacy_key} ERROR: {e}")
                            logging.debug(
                                f"API Key {legacy_key} Returned: {data}")
                            spinner.text = "Didn't work... Trying another."
                except Exception:
                    pass
                spinner.text = (error("Failed to get API Key - read below."))
                spinner.fail("[!]")
                print(
                    '    -----------------------------------------------------------------'
                )
                print(yellow("    Looks like you need to get an API Key. "))
                print(yellow("    The WARden comes with a shared key that"))
                print(yellow("    eventually gets to the call limit."))
                print(
                    '    -----------------------------------------------------------------'
                )
                print(
                    yellow(
                        '    Go to: https://www.cryptocompare.com/cryptopian/api-keys'
                    ))
                print(
                    yellow(
                        '    To get an API Key. Keys from cryptocompare are free.'
                    ))
                print(
                    yellow(
                        '    [Tip] Get a disposable email to signup and protect privacy.'
                    ))
                print(
                    yellow(
                        '    Services like https://temp-mail.org/en/ work well.'
                    ))

                print(muted("    Current API:"))
                print(f"    {api_key}")
                new_key = input('    Enter new API key (Q to quit): ')
                if new_key == 'Q' or new_key == 'q':
                    exit()
                pickle_it('save', 'cryptocompare_api.pkl', new_key)
                check_cryptocompare()
        except KeyError:
            try:
                btc_price = (data['DISPLAY']['BTC']['USD']['PRICE'])
                spinner.ok("✅ ")
                spinner.write(success(f"BTC price is: {btc_price}"))
                pickle_it('save', 'cryptocompare_api.pkl', api_key)
                return
            except Exception:
                spinner.text = (
                    warning("CryptoCompare Returned an UNKNOWN error"))
                spinner.fail("💥 ")
        return (data)


#line 232-further
def newFun2() :

    with app.app_context():
        from .specter_importer import Specter
        app.specter = Specter()
        app.specter.refresh_txs(load=True)
        app.downloading = False
    from .utils import (create_config, runningInDocker)
    with app.app_context():
        app.runningInDocker = runningInDocker()

    # # with app.app_context():
    # #     app.tor = create_tor()

    # # Check if home folder exists, if not create
    # from pathlib import Path
    # home = str(Path.home())
    # home_path = os.path.join(home, 'warden/')
    # try:
    #     os.makedirs(os.path.dirname(home_path))
    # except Exception:
    #     pass

    # Start Schedulers
    from .backgroundjobs import (background_settings_update,
                                background_specter_update,
                                background_scan_network,
                                background_specter_health,
                                background_mempool_seeker)


    from apscheduler.schedulers.background import BackgroundScheduler
    def bk_su():
        # with app.app_context():
            background_specter_update()

    def bk_stu():
        # with app.app_context():
            background_settings_update()

    def bk_scan():
        # with app.app_context():
            background_scan_network()

    def bk_specter_health():
        # with app.app_context():
            background_specter_health()

    def bk_mempool_health():
        # with app.app_context():
            background_mempool_seeker()

    app.scheduler = BackgroundScheduler()
    app.scheduler.add_job(bk_su, 'interval', seconds=1)
    app.scheduler.add_job(bk_stu, 'interval', seconds=1)
    app.scheduler.add_job(bk_scan, 'interval', seconds=1)
    app.scheduler.add_job(bk_specter_health, 'interval', seconds=1)
    app.scheduler.add_job(bk_mempool_health, 'interval', seconds=1)
    # with app.app_context():
    app.scheduler.start()
    print(success("✅ Background jobs running"))
    print("")
    app.app_context().push()

    print(success("✅ Application startup is complete"))




def initWarden():
    

    #WARDD
    # here we do everything that main.py did for warden, one by one
    unedited_app = dir(app)

    #wdd: setting up config (hardcoding it here as errors show up, instead of separate config file)
    # need to take care because names might collide with specter
    # speter doesn't have app.settings so we're good there

    settings_dict = {
        'SPECTER':{
            'specter_url':"http://127.0.0.1:25441",
            'specter_login':'bitcoin',
            'specter_password':'secret'
        },
        'PORTFOLIO' : {
            'base_fx': 'USD',
            'divisor' : '1',
        }
    }

    app.settings = settings_dict



    
    from .ansi_management import (warning, success, error)
    from .utils import (create_config, runningInDocker)
    from .config import Config
    from .connections import tor_request
    warnings.filterwarnings('ignore')

    config_file = Config.config_file
    app.warden_status = {}

    # Check for internet connection
    internet_ok = internet_connected()
    if internet_ok is True:
        print(success("✅ Internet Connection"))
    else:
        print(
            error(
                "[!] WARden needs internet connection. Check your connection.")
        )
        print(warning("[!] Exiting"))
        exit()

    # Config
    config_settings = configparser.ConfigParser()
    if os.path.isfile(config_file):
        config_settings.read(config_file)
        app.warden_status['initial_setup'] = False
        print(
            success(
                "✅ Config Loaded from config.ini - edit it for customization"))
    else:
        print(
            error(
                "  Config File could not be loaded, created a new one with default values..."
            ))
        create_config(config_file)
        config_settings.read(config_file)
        app.warden_status['initial_setup'] = True

    table_error = False
    try:
        # create empty instance of LoginManager
        app.login_manager = LoginManager()
    except sqlite3.OperationalError:
        table_error = True

    # Create empty instance of SQLAlchemy


    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///warden.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    ###
    app.db = SQLAlchemy()
    app.db.init_app(app)
    # Import models so tables are created
    from .models import Trades, User, AccountInfo, TickerInfo, SpecterInfo
    app.db.create_all()
    
    #  There was an initial error on getting users
    #  probably because tables were not created yet.
    # The above create_all should have solved it so try again.
    if table_error:
        # create empty instance of LoginManager
        app.login_manager = LoginManager()

    # If login required - go to login:
    app.login_manager.login_view = "warden.routes.login"
    # To display messages - info class (Bootstrap)
    app.login_manager.login_message_category = "secondary"
    app.login_manager.init_app(app)

    # Create empty instance of messagehandler
    from .message_handler import MessageHandler
    app.message_handler = MessageHandler()
    app.message_handler.clean_all()

    # Get Version
    print("")
    try:
        version_file = Config.version_file
        with open(version_file, 'r') as file:
            current_version = file.read().replace('\n', '')
    except Exception:
        current_version = 'unknown'
    with app.app_context():
        app.version = current_version

    # Check if there are any users on database, if not, needs initial setup
    users = User.query.all()

    if users == []:
        app.warden_status['initial_setup'] = True

    # Check for Cryptocompare API Keys
    print("")
    check_cryptocompare()
    print("")

    print(f"[i] Running WARden version: {current_version}")
    app.warden_status['running_version'] = current_version

    # CHECK FOR UPGRADE
    repo_url = 'https://api.github.com/repos/pxsocs/warden/releases'
    try:
        github_version = tor_request(repo_url).json()[0]['tag_name']
    except Exception:
        github_version = None

    app.warden_status['github_version'] = github_version

    if github_version:
        print(f"[i] Newest WARden version available: {github_version}")
        parsed_github = version.parse(github_version)
        parsed_version = version.parse(current_version)

        app.warden_status['needs_upgrade'] = False
        if parsed_github > parsed_version:
            print(warning("  [i] Upgrade Available"))
            app.warden_status['needs_upgrade'] = True
        if parsed_github == parsed_version:
            print(success("✅ You are running the latest version"))
    else:
        print(warning("[!] Could not check GitHub for updates"))

    print("")
    # Check if config.ini exists
    with app.app_context():
        app.settings = config_settings
    with app.app_context():
        try:
            from .utils import fxsymbol
            app.fx = fxsymbol(config_settings['PORTFOLIO']['base_fx'], 'all')
        except KeyError:  # Problem with this config, reset
            print(error("  [!] Config File needs to be rebuilt"))
            print("")
            create_config(config_file)

    # newFun2()




initWarden()



class WardenService(Service):
    id = "warden"
    name = "Warden Service"
    icon = ""
    logo = ""
    desc = "Where a warden grows bigger."
    has_blueprint = True
    blueprint_modules = {"default": "yogendra.specterext.warden.newcontroller",
                        "routes": "yogendra.specterext.warden.routes",
    
                        
                         "api":"yogendra.specterext.warden.api.routes",
                         
                         "csv_routes": "yogendra.specterext.warden.csv_routes.routes",
                         "user_routes":"yogendra.specterext.warden.user_routes.routes"}
    devstatus = devstatus_alpha
    isolated_client = False

    # TODO: As more Services are integrated, we'll want more robust categorization and sorting logic
    sort_priority = 2

    # ServiceEncryptedStorage field names for this service
    # Those will end up as keys in a json-file
    SPECTER_WALLET_ALIAS = "wallet"

    def callback_after_serverpy_init_app(self, scheduler: APScheduler):
        # with app.app_context():
        from .specter_importer import Specter
        #WARDD: changed app.warden_specter to app.warden_specter 
        app.warden_specter = Specter()
        app.warden_specter.refresh_txs(load=True)
        app.downloading = False
        




    @classmethod
    def get_associated_wallet(cls) -> Wallet:
        """Get the Specter `Wallet` that is currently associated with this service"""
        service_data = cls.get_current_user_service_data()
        if not service_data or cls.SPECTER_WALLET_ALIAS not in service_data:
            # Service is not initialized; nothing to do
            return
        try:
            return app.warden_specter.wallet_manager.get_by_alias(
                service_data[cls.SPECTER_WALLET_ALIAS]
            )
        except SpecterError as e:
            logger.debug(e)
            # Referenced an unknown wallet
            # TODO: keep ignoring or remove the unknown wallet from service_data?
            return

    @classmethod
    def set_associated_wallet(cls, wallet: Wallet):
        """Set the Specter `Wallet` that is currently associated with this Service"""
        cls.update_current_user_service_data({cls.SPECTER_WALLET_ALIAS: wallet.alias})
