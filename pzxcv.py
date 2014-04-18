#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import ConfigParser
import random


CONFIG_FILE = NICOBBS_CONFIG = os.path.dirname(os.path.abspath(__file__)) + '/pzxcv.config'


# code taken from http://azwoo.hatenablog.com/entry/2014/01/07/185413
class _Getch:
    def __call__(self):
        import tty
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


def main():
    config = ConfigParser.ConfigParser()
    config.read(CONFIG_FILE)

    characters = config.get('pzxcv', 'characters')

    input_count = 0
    previours_character = None
    reserved_character = None
    getch = _Getch()

    while True:
        target_character = None
        if reserved_character:
            target_character = reserved_character
            reserved_character = None
        else:
            index = random.randint(0, len(characters) - 1)
            target_character = characters[index]
            if target_character == previours_character:
                continue
            previours_character = target_character

        sys.stdout.write(str(input_count) + ": " + target_character + " ")
        input_character = getch()
        sys.stdout.write(input_character + "\n")

        if input_character == 'q':
            break
        elif target_character != input_character:
            sys.stdout.write("\a")
            reserved_character = target_character
        elif target_character == input_character:
            input_count += 1


if __name__ == "__main__":
    main()
