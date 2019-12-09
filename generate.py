#!/bin/env python

import os
import re
import uuid
import jinja2

CONFIG_PATH = 'configs'
OUTPUT_PATH = 'output'
TEMPLATE_FILE = 'template.nmconnection'

scriptdir = os.path.dirname(os.path.realpath(__file__))
certpath = os.path.join(scriptdir, CONFIG_PATH, 'ca.rsa.2048.crt')

username = raw_input('username: ')
password = raw_input('password: ')

templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader)
template = templateEnv.get_template(TEMPLATE_FILE)

os.mkdir(OUTPUT_PATH)

ovpn_configs = [f for f in os.listdir(CONFIG_PATH) if 'ovpn' in  f]

for filename in ovpn_configs:
    name = os.path.splitext(filename)[0]
    uuid_str = str(uuid.uuid1())
    fullpath = os.path.join(CONFIG_PATH, filename)
    with open(fullpath) as fp:
        while True:
            line = fp.readline()
            if not line:
                break
            matches = re.match("remote (.+) (\d+)", line)
            if matches:
                host = matches.group(1)
                port = matches.group(2)
    contents = template.render(username=username,
                               password=password,
                               certpath=certpath,
                               name=name,
                               uuid=uuid_str,
                               host=host,
                               port=port)
    filename_out = "{}.nmconnection".format(name)
    fullpath_out = os.path.join(OUTPUT_PATH, filename_out)
    with open(fullpath_out, 'w+') as fpo:
        fpo.write(contents)
