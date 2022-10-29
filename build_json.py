#!/usr/bin/env python3
import argparse
import os
import yaml
import logging
import sys
from project_urls import project_urls
from git_utils import fetch_file_from_git


def build_json(number, git_url):
    info = fetch_file_from_git(git_url, 'info.yaml')
    if info is None:
        logging.error("file not found in repo")
        return None

    # parse the yaml
    try:
        yaml_data = (yaml.safe_load(info))
        # only bother trying if the author field has been filled in
        author = yaml_data['project']['author']
        if author == '':
            logging.info("yaml is the default - skipping")
            return None
    except yaml.YAMLError as exc:
        logging.error(exc)
        return None

    yaml_data['project']['wokwi_id'] = str(yaml_data['project']['wokwi_id'])
    yaml_data['project']['git_url'] = git_url
    return yaml_data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="TT docs")

    parser.add_argument('--debug', help="debug logging", action="store_const", dest="loglevel", const=logging.DEBUG, default=logging.INFO)
    parser.add_argument('--limit', help="stop after this number of projects", type=int, default=0)
    args = parser.parse_args()
    # setup log
    log_format = logging.Formatter('%(asctime)s - %(module)-10s - %(levelname)-8s - %(message)s')
    # configure the client logging
    log = logging.getLogger('')
    # has to be set to debug as is the root logger
    log.setLevel(args.loglevel)

    # create console handler and set level to info
    ch = logging.StreamHandler(sys.stdout)
    # create formatter for console
    ch.setFormatter(log_format)
    log.addHandler(ch)

    success = 0
    designs = []
    for number, project_url in enumerate(project_urls):
        # some problematic ones
        if project_url in ["https://github.com/ElectricPotato/tinytapeout-hello-world-uart"]:
            logging.warning("skipping # {} : {}".format(number, project_url))
            continue
        logging.info("fetching yaml for project # {} : {}".format(number, project_url))
        design = build_json(number, project_url)
        if design is not None:
            designs.append(design)

        if args.limit != 0 and number > args.limit:
            break

    import json

    with open("designs.json", "w") as fh:
        fh.write(json.dumps(designs, indent=4))
    logging.info("{} of {} fetched OK!".format(success, number))
