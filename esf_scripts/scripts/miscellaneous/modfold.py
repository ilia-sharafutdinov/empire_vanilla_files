import argparse
import os
import pandas as pd

from ..lib import *



def modfold(campaign_dir: str, campaign_map_dir: str, campaign_maps_dir: str = 'campaign_maps'):
    '''
    example:
        modfold('tgg_1830', 'tgg_global_map')
    '''

    # Reassigning map location in campaign model

    campaign_model = CampaignModel(os.path.join(OUTPUT_DIR, 'campaign_env', 'campaign_model.xml'))

    campaign_model.set_map_location(f"{campaign_maps_dir}/{campaign_map_dir}")
    campaign_model.set_map_name(campaign_map_dir)

    # Reassigning campaign name in campaign setup

    campaign_setup = CampaignSetup(os.path.join(OUTPUT_DIR, 'campaign_env', Env(os.path.join(OUTPUT_DIR, 'campaign_env', 'env.xml')).get_campaign_setup()))

    campaign_setup.set_campaign_name(campaign_dir)

    # Reassigning campaign name and map location in preopen map info

    preopen_map_info = PreopenMapInfo(os.path.join(OUTPUT_DIR, 'preopen_map_info', Esf(os.path.join(OUTPUT_DIR, 'esf.xml')).get_preopen_map_info()))

    preopen_map_info.set_campaign_name(campaign_dir)
    preopen_map_info.set_campaign_map(campaign_map_dir)

    # Applying changes

    campaign_model.write_xml()

    campaign_setup.write_xml()

    preopen_map_info.write_xml()



if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description='',
        epilog='example:\n' +
        '  python modfold.py tgg_1830 tgg_global_map')
    parser.add_argument('campaign_dir', type=str, help='')
    parser.add_argument('campaign_map_dir', type=str, help='')
    parser.add_argument('-m', '--campaign_maps_dir', type=str, default='campaign_maps', help='')
    args = parser.parse_args()

    campaign_dir = args.campaign_dir
    campaign_map_dir = args.campaign_map_dir
    campaign_maps_dir = args.campaign_maps_dir

    modfold(campaign_dir, campaign_map_dir, campaign_maps_dir)
