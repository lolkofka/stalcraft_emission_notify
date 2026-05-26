import collections
import json
import logging
import os
import os.path
import shutil

import assets

config_file = 'data/config.json'

config = assets.config


def update(d, u):
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = update(d.get(k, {}), v)
        else:
            d[k] = v
    return d


def reload():
    global config

    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            user_config = json.load(f)
            config = update(config, user_config)
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=True, sort_keys=True, indent=4)
    else:
        shutil.copyfile('assets/default_config.json', config_file)
        logging.error('Config was created, restart needed')
        exit(0)

    mongo_host = os.getenv('MONGO_HOST')
    mongo_port = os.getenv('MONGO_PORT', '27017')
    mongo_db = os.getenv('MONGO_DB')

    if mongo_host:
        config['bot']['mongo'] = f'mongodb://{mongo_host}:{mongo_port}/'
    if mongo_db:
        config['bot']['database'] = mongo_db


reload()
