#!/usr/bin/env python3

"""
Userscript for qutebrowser which saves some text that can be retrieved with the key associated with it.
The texts are saved on a json in config dir by default
"""

#     Copyright Alexandre Costa do Sim (aledosim) <aledosim@yahoo.com.br>
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.

import logging
log = logging.getLogger(__name__)
log.setLevel('DEBUG')

# --------------------------------------------------------
# Uncomment this line for debug log
#log.addHandler(logging.FileHandler('qute-snippets.log'))
# --------------------------------------------------------

from datetime import datetime
log.debug('\nStarting execution in {}'.format(datetime.now()))

import argparse
import os
import json

SAVE_DIR = os.getenv('QUTE_CONFIG_DIR')

# for test purposes
if not SAVE_DIR: SAVE_DIR = 'testdir'

log.debug('SAVE_DIR: '+str(SAVE_DIR))

USAGE = """snippets.py [-h] [--set | --get] params

This script save some text snippet to a keyword and paste it back when called with the same keyword.
It's meant to be used with qutebrowser (see https://qutebrowser.org/).

   To save a snippet to a certain keyword:
      snippets.py --set <keyword> <text>

   To paste a snippet binded to a certain keyword:
      snippets.py --get <keyword>

   To use it with qutebrowser:
      :spawn --userscript snippets.py [--set | --get] params

I suggest that you make the following keybinds:

   To save a snippet, i.e.:
      :bind --mode insert <Ctrl+Alt+1> spawn --userscript snippets.py --set 1 {primary}

   To paste a snippet, i.e.:
      :bind --mode insert <Ctrl+1> spawn --userscript snippets.py --get 1"""

EPILOG = """The snippets are saved on a json in the qutebrowser's configuration folder.
For debug log, uncomment the respective line in source."""

argument_parser = argparse.ArgumentParser(usage=USAGE, epilog=EPILOG)
argument_parser.add_argument('params', nargs='+', help='<keyword> <text> to use set option or\
                                                        <keyword> to use get option')
group = argument_parser.add_mutually_exclusive_group()
group.add_argument('--set', '-s', action='store_true', help='set a text to a certain keyword')
group.add_argument('--get', '-g', action='store_true', help='get a text saved to a keyword')


def qute_paste_text(text):
    # Paste text on browser
    log.debug('qute_paste_text input: '+str(text))

    cmd = 'insert-text {}\n'.format(text)
    with open(os.environ['QUTE_FIFO'], 'w') as fifo:
        fifo.write(cmd)
        fifo.flush()


def qute_show_message(message):
    # Show message on browser
    log.debug('qute_show_message input: '+str(message))

    cmd = 'message-info "{}"\n'.format(message)
    with open(os.environ['QUTE_FIFO'], 'w') as fifo:
        fifo.write(cmd)
        fifo.flush()


def set_text(key, text):
    # Saves a json on SAVE_DIR directory with text associated with key
    log.debug('set_text input: '+str((key, text)))

    json_file = '{}/{}'.format(SAVE_DIR, 'snippets.json')
    try:
        with open(json_file, 'x') as snippets:
            json.dump({key: text}, snippets)

    except FileExistsError:
        with open(json_file) as snippets:
            saved = json.load(snippets)

        saved[key] = text

        with open(json_file, 'w') as snippets:
            json.dump(saved, snippets)

    qute_show_message('Text saved on key {}'.format(key))


def get_text(key):
    # Retrieves text from json saved on SAVE_DIR with key
    log.debug('get_text input: '+str(key))

    json_file = '{}/{}'.format(SAVE_DIR, 'snippets.json')
    with open(json_file) as snippets:
        registers = json.load(snippets)

    return registers[key]


def main(arguments):
    params = arguments.params
    if len(params) == 2:  # implicit set
        set_text(params[0], params[1])
    elif arguments.get:  # explicit get
        text = get_text(params[0])
        qute_paste_text(text)
    elif len(params) == 2 and arguments.set:  # explicit set
        set_text(params[0], params[1])
    elif len(params) == 1 and not arguments.set:  # implicit get
        text = get_text(params[0])
        qute_paste_text(text)
    else:  # wrong usage or help
        log.debug('Invalid arguments')
        argument_parser.print_help()


if __name__ == '__main__':
    args = argument_parser.parse_args()
    log.debug('args: '+str(args))
    main(args)
