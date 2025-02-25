#!/usr/bin/python3

import cnco2
import sys
import sqlite3

user_commands = ['get_version', 'discover_components', 'get_ip']

if __name__ == '__main__':
    cnco2.getAbout()

    try:
        commands = sys.argv[1]
    except IndexError:
        commands = 'help'

    match commands:
        case 'get_version':
            print(cnco2.System.getVersion())
        case 'discover_components':
            cnco2.System.discoverComponents()
        case 'get_ip':
            ip_address = cnco2.System.getIp()
            print(ip_address)
        case _:
            print("Commands")
            for user_command in user_commands:
                print(user_command)
