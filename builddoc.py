#!/usr/bin/env python3
import glob
import yaml
import os
import subprocess
from project_urls import project_urls

infos = glob.glob('./*/info.yaml')

doc_string = """
# {title}

{picture_link}

* Author {author}
* Description {description}
* [GitHub project]({git_url})
* [Wokwi project]({wokwi_url})
* [Extra docs]({doc_link})
* Clock {clock_hz} Hz
* External hardware {external_hw}

## How it works

{how_it_works}

## How to test

{how_to_test}

## IO

| # | Input        | Output       |
|---|--------------|--------------|
| 0 | {inputs[0]}  | {outputs[0]} |
| 1 | {inputs[1]}  | {outputs[1]} |
| 2 | {inputs[2]}  | {outputs[2]} |
| 3 | {inputs[3]}  | {outputs[3]} |
| 4 | {inputs[4]}  | {outputs[4]} |
| 5 | {inputs[5]}  | {outputs[5]} |
| 6 | {inputs[6]}  | {outputs[6]} |
| 7 | {inputs[7]}  | {outputs[7]} |

"""

print("""---
  header-includes:
    - \hypersetup{colorlinks=false,
              allbordercolors={0 0 0},
              pdfborderstyle={/S/U/W 1}}
  ---""")

for info in infos:
    with open(info, "r") as stream:
        try:
            data = (yaml.safe_load(stream))
            author = data['project']['author']
            if author != '':
                # build up some new elements in the dict
                data['project']['picture_link'] = ''
                if data['project']['picture']:
                    if 'svg' not in data['project']['picture']:
                        data['project']['picture_link'] = '![picture]({})'.format(os.path.join(os.path.dirname(info), data['project']['picture']))
                data['project']['wokwi_url'] = 'https://wokwi.com/projects/' + str(data['project']['wokwi_id'])

                # get git url
                repo_name = os.path.dirname(info)
                remote = subprocess.check_output("git -C {} config --get remote.origin.url".format(repo_name), shell=True).decode('utf-8')
                data['project']['git_url'] = remote
                

                # now build the doc & print it
                try:
                    doc = doc_string.format(**data['project'])
                    print(doc)
                except IndexError as e:
                    pass

        except yaml.YAMLError as exc:
            print(exc)
