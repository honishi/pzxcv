#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import ConfigParser
import random


MINIMUM_CHARACTERS_LENGTH = 5
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

    default_characters = config.get('pzxcv', 'characters')
    current_characters = default_characters

    total_input_count = 0

    exit_count = 50     # character input count per 1 character set
    if len(sys.argv) == 2:
        exit_count = int(sys.argv[1])

    should_exit = False
    getch = _Getch()

    while True:
        input_count = 0
        previours_character = None
        reserved_character = None
        missed_characters = {}

        while input_count < exit_count:
            target_character = None
            if reserved_character:
                target_character = reserved_character
                reserved_character = None
            else:
                index = random.randint(0, len(current_characters) - 1)
                target_character = current_characters[index]
                if target_character == previours_character:
                    continue
                previours_character = target_character

            sys.stdout.write(str(total_input_count + 1) + ": " + target_character + " ")
            input_character = getch()
            sys.stdout.write(input_character + "\n")

            if input_character == 'q':
                should_exit = True
                break
            elif target_character != input_character:
                sys.stdout.write("\a")
                if not target_character in missed_characters:
                    missed_characters[target_character] = 0
                missed_characters[target_character] += 1
                reserved_character = target_character
            elif target_character == input_character:
                total_input_count += 1
                input_count += 1

        # report_missed_characters(missed_characters)

        if should_exit:
            break

        candidate_characters = renew_characters(default_characters, missed_characters)
        if current_characters != candidate_characters:
            current_characters = candidate_characters
            print("character set changed. < " + current_characters + " >")


def report_missed_characters(missed_characters):
    sorted_missed_characters = sorted(missed_characters.items(), key=lambda x:x[1], reverse=True)

    if 0 == len(sorted_missed_characters):
        print("no missed input.")
    else:
        print("missed {} input(s).".format(len(sorted_missed_characters)))
        print("-----")
        for character, missed_count in sorted_missed_characters:
            print(character + ": " + str(missed_count))
        print("-----")


def renew_characters(default_characters, missed_characters):
    failure_characters = ""
    sorted_missed_characters = sorted(missed_characters.items(), key=lambda x:x[1])

    for character, missed_count in sorted_missed_characters:
        if 1 < missed_count:
            failure_characters += character

    renewed_characters = default_characters

    if 0 < len(failure_characters):
        renewed_characters = failure_characters
        while len(renewed_characters) < MINIMUM_CHARACTERS_LENGTH:
            index = random.randint(0, len(default_characters) - 1)
            renewed_characters  += default_characters[index]

    return renewed_characters


if __name__ == "__main__":
    main()
