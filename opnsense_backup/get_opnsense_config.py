"""Script used in conjunction with the os-api-backup plugin on OPNsense.

File: get_opnsense_config.py
Author: Josh Alexander

"""
import logging
import argparse
from pathlib import Path
import defusedxml.ElementTree as ET
from datetime import datetime

import requests


def main():
    """Main function for retrieving an OPNSense configuration."""
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO)
    logger = logging.getLogger("OPNsense Backup")

    parser = argparse.ArgumentParser(description='Backup OPNSense Configuration.')
    parser.add_argument('--key', '-k', type=str, help='OPNSense Key', required=True)
    parser.add_argument('--secret', '-s', type=str, help='OPNSense Secret', required=True)
    parser.add_argument('--host', type=str, help='OPNSense host address (use IP or FQDN)', required=True)
    parser.add_argument('--path', '-p', type=str, help='Path to save configuration file to', default=".", required=False)

    args = parser.parse_args()

    try:
        request = requests.get(f"{args.host}/api/backup/backup/download", auth=(args.key, args.secret), verify=False)

    except Exception as error:
        logger.error(f"An error occurred when attempting to access OPNSense API at {args.host}/api/backup/backup/download: {error}")
        exit(1)

    else:
        tree = ET.XML(request.text)

        config_file_name = f"opnsense-config-{datetime.now().strftime('%Y-%m-%d')}.xml"
        config_file_path = Path(args.path) / config_file_name
        with open(config_file_path, "wb") as f:
            f.write(ET.tostring(tree))

        logger.info(f"Successfully retrieved OPNsense configuration, saved to {str(config_file_path)}")


if __name__ == '__main__':
    """Entry point for OPNSense configuration backup."""
    main()
