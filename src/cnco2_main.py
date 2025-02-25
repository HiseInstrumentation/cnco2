import cnco2
import sys
import sqlite3

user_commands = ['get_version', 'discover_components', 'get_ip']

if __name__ == '__main__':
    cnco2.getAbout()

    commands = sys.argv[1]

    match commands:
        case 'get_version':
            print("1.0")
        case 'discover_components':
            cnco2.System.discoverComponents()
        case 'get_ip':
            ip_address = cnco2.System.getIp()
            print(ip_address)
        case _:
            print("Commands")
            print(user_commands)
