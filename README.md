# qute-snippets
> Save some text to easily retrieve it when you need it

This script save some text snippet to a keyword and paste it back when called with the same keyword.
It's meant to be used with [qutebrowser](https://qutebrowser.org/).
## Installation
Just copy snippets.py to `~/.local/share/qutebrowser/userscripts` (or $XDG_DATA_HOME) or `/usr/share/qutebrowser/userscripts`.
Or some other directory you save qutebrowser's scripts.
## Usage
To save a snippet to a certain keyword run:

    snippets.py --set <keyword> <text>

To paste a snippet binded to a certain keyword:

    snippets.py --get <keyword>
On qutebrowser you should run, i.e:

    :spawn --userscript snippets.py --set 3 "Test text"
    :spawn --userscript snippets.py --get 3
### Keybinding suggestion
I suggest that you make the following numeric keybindings:

To save a snippet, i.e.:

    :bind --mode insert <Ctrl+Alt+1> spawn --userscript snippets.py --set 1 {primary}

To paste a snippet, i.e.:

    :bind --mode insert <Ctrl+1> spawn --userscript snippets.py --get 1
_See qutebrowser's [help on keybinding](https://github.com/qutebrowser/qutebrowser/blob/master/doc/help/commands.asciidoc#bind) for more information._ 
## Debug log
You can activate debug log uncommenting the marked line in source code.
## Author
Alexandre Sim – [Alexandre do Sim](https://www.linkedin.com/in/alexandre-do-sim-86930414b/) – aledosim@yahoo.com.br

Distributed under the GPL3 license. See `LICENSE` for more information.

[https://github.com/Aledosim](https://github.com/Aledosim)
