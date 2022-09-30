#!/usr/bin/env python3
import argparse
import yaml
import logging
import sys
from project_urls import project_urls
from git_utils import fetch_file_from_git

markdown_doc = 'tt01.md'


def build_header():
    with open("header.txt") as fh:
        doc_header = fh.read()
    with open(markdown_doc, 'w') as fh:
        fh.write(doc_header)


def build_doc(number, git_url):
    info = fetch_file_from_git(git_url, 'info.yaml')
    if info is None:
        logging.error("file not found in repo")
        return

    # parse the yaml
    try:
        yaml_data = (yaml.safe_load(info))
        # only bother trying if the author field has been filled in
        author = yaml_data['project']['author']
        if author == '':
            logging.info("yaml is the default - skipping")
            return
    except yaml.YAMLError as exc:
        logging.error(exc)
        return

    with open("template.md") as fh:
        doc_string = fh.read()

    with open(markdown_doc, 'a') as fh:
        # build up some new elements in the dict
        yaml_data['project']['picture_link'] = ''

        # handle pictures
        if yaml_data['project']['picture']:
            # skip SVG for now, not supported by pandoc
            picture_name = yaml_data['project']['picture']
            if 'svg' not in picture_name:
                # fetch the file
                picture_data = fetch_file_from_git(git_url, picture_name)
                picture_filename = '{}{}'.format(number, picture_name)
                with open(picture_filename , 'wb') as fpic:
                    fpic.write(picture_data)
                yaml_data['project']['picture_link'] = '![picture]({})'.format(picture_filename)

        yaml_data['project']['wokwi_url'] = 'https://wokwi.com/projects/' + str(yaml_data['project']['wokwi_id'])

        # get git url
        yaml_data['project']['git_url'] = git_url

        # now build the doc & print it
        try:
            doc = doc_string.format(**yaml_data['project'])
            fh.write(doc)
            fh.write("\n\pagebreak\n")
        except IndexError as e:
            logging.error(e)
            return

        return True


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

    build_header()
    success = 0
    for number, project_url in enumerate(project_urls):
        # some problematic ones
        if project_url in ["https://github.com/ElectricPotato/tinytapeout-hello-world-uart"]:
            logging.warning("skipping # {} : {}".format(number, project_url))
            continue
        logging.info("building docs for project # {} : {}".format(number, project_url))
        build_ok = build_doc(number, project_url)
        if build_ok is not None:
            success += 1

        if args.limit != 0 and number > args.limit:
            break

    logging.info("{} of {} built OK!".format(success, number))
