import os
import sys
import argparse
from modules import logger
from modules import configuration
from pathlib import Path
from modules.CustomConfigParser import CustomConfigParser
from modules.TerraformController import TerraformController

# need to set this ENV var due to a OSX High Sierra forking bug
# see this discussion for more details: https://github.com/ansible/ansible/issues/34056#issuecomment-352862252
os.environ['OBJC_DISABLE_INITIALIZE_FORK_SAFETY'] = 'YES'

VERSION = 1


def init(args):
    config = args.config
    print("""

  _________             .__                      _____   __    __                 __     __________                               
 /   _____/ ____ ______ |  |__   ____  ______   /  _  \_/  |__/  |______    ____ |  | __ \______   \_____    ____    ____   ____  
 \_____  \ /  _ \\____ \|  |  \ /  _ \/  ___/  /  /_\  \   __\   __\__  \ _/ ___\|  |/ /  |       _/\__  \  /    \  / ___\_/ __ \ 
 /        (  <_> )  |_> >   Y  (  <_> )___ \  /    |    \  |  |  |  / __ \\  \___|    <   |    |   \ / __ \|   |  \/ /_/  >  ___/ 
/_______  /\____/|   __/|___|  /\____/____  > \____|__  /__|  |__| (____  /\___  >__|_ \  |____|_  /(____  /___|  /\___  / \___  >
        \/       |__|        \/           \/          \/                \/     \/     \/         \/      \/     \//_____/      \/ 

    """)

    # parse config
    attack_range_config = Path(config)
    if attack_range_config.is_file():
        print("attack_range is using config at path {0}".format(
            attack_range_config))
        configpath = str(attack_range_config)
    else:
        print("ERROR: attack_range failed to find a config file")
        sys.exit(1)
    
    # parse config
    parser = CustomConfigParser()
    config = parser.load_conf(configpath)

    log = logger.setup_logging(config['log_path'], config['log_level'])
    log.info("INIT - attack_range v" + str(VERSION))

    if config['cloud_provider'] == 'azure':
        os.environ["AZURE_SUBSCRIPTION_ID"] = config['azure_subscription_id']

    if config['attack_range_password'] == 'Ch@nG3_m3!':
        log.error('ERROR: please change attack_range_password in attack_range.conf')
        sys.exit(1)

    if config['cloud_provider'] == 'azure' and config['zeek_sensor'] == '1':
        log.error('ERROR: zeek sensor only available for aws in the moment. Plase change zeek_sensor to 0 and try again.')
        sys.exit(1)

    if config['cloud_provider'] == 'aws' and config['windows_client'] == '1':
        log.error('ERROR: windows client is only support for Azure.')
        sys.exit(1)
    
    if config['cloud_provider'] == 'vsphere' and config['vsphere_server'] == 'vcenter.contoso.local':
        log.error('ERROR: vcenter configuration is missing! Please re-run sophos_attack_range.py configure to configure vcenter.')
        sys.exit(1)

    return TerraformController(config, log), config, log