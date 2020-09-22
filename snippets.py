#!/usr/bin/env python3

# Userscript for qutebrowser which saves some text that can be retomado with the key associated with it.
# The texts are saved on a json in config dir by default

# TODO
# - decidir qual o formato da ajuda

import logging
log = logging.getLogger(__name__)
log.setLevel('DEBUG')

import argparse
import os
import json
from datetime import datetime


# Uncomment this line for debug log
log.addHandler(logging.FileHandler('register.log'))

log.debug('\nStarting execution in {}'.format(datetime.now()))

SAVE_DIR = os.getenv('QUTE_CONFIG_DIR')
# for test purposes
if not SAVE_DIR: SAVE_DIR = 'testdir'

log.debug('SAVE_DIR: '+str(SAVE_DIR))

argument_parser = argparse.ArgumentParser()
argument_parser.add_argument('params', nargs='+')
group = argument_parser.add_mutually_exclusive_group()
group.add_argument('--set', '-s', action='store_true')
group.add_argument('--get', '-g', action='store_true')


def qute_paste_text(text):
    log.debug('qute_paste_text input: '+str(text))
    cmd = 'insert-text {}\n'.format(text)
    with open(os.environ['QUTE_FIFO'], 'w') as fifo:
        fifo.write(cmd)
        fifo.flush()


def qute_show_message(message):
    log.debug('qute_show_message input: '+str(message))
    cmd = 'message-info "{}"\n'.format(message)
    with open(os.environ['QUTE_FIFO'], 'w') as fifo:
        fifo.write(cmd)
        fifo.flush()


def set_text(key, text):
    log.debug('set_text input: '+str((key, text)))
    # Saves a json on save_dir directory with text associated with key
    _file = '{}/{}'.format(SAVE_DIR, 'qute-snippets.json')
    try:
        with open(_file, 'x') as file:
            json.dump({key: text}, file)
    except FileExistsError:
        with open(_file) as file:
            saved = json.load(file)

        saved[key] = text

        with open(_file, 'w') as file:
            json.dump(saved, file)

    qute_show_message('Text saved on key {}'.format(key))


def get_text(key):
    log.debug('get_text input: '+str(key))
    _file = '{}/{}'.format(SAVE_DIR, 'qute-snippets.json')
    # test if _file exists
    with open(_file) as file:
        registers = json.load(file)

    return registers[key]


def main(arguments):
    params = arguments.params
    if len(params) == 2:  # implicit set
        # print('implicit set case')
        set_text(params[0], params[1])
    elif arguments.get:  # explicit get
        # print('explicit get case')
        text = get_text(params[0])
        qute_paste_text(text)
    elif len(params) == 2 and arguments.set:  # explicit set
        # print('explicit set case')
        set_text(params[0], params[1])
    elif len(params) == 1 and not arguments.set:  # implicit get
        # print('implicit get case')
        text = get_text(params[0])
        qute_paste_text(text)
    else:  # wrong usage
        # print('wrong usage case')
        log.debug('Invalid arguments')
        argument_parser.print_help()


if __name__ == '__main__':
    args = argument_parser.parse_args()
    log.debug('args: '+str(args))
    main(args)
