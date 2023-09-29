#!/usr/bin/env python3

import sys
import os
import argparse

def main():
    praser = argparse.ArgumentParser(description="ESP32 partition table reader")

    praser.add_argument('--table-type','-t',help='Name of table to get data <nvs,otadata,app0,app1,spiffs,coredump>')
    praser.add_argument('--field','-f',help='Column to get data <Type,SubType,Offset,Size,Flags>')
    praser.add_argument('input',help='Path of "partitions.csv" or CSV fiel')

    args = praser.parse_args()

    if not args.table_type or not args.field or not args.input:
        praser.print_help()
        sys.exit(0)
    
    if os.path.exists(args.input):
        table = {}
        with open(args.input) as fp:
            for l in fp.readlines():
                key,_type,sub_type,offset,size,flags = (i.strip() for i in l.split(','))
                table[key] = {'type':_type ,'subtype':sub_type ,'offset':offset, 'size':size, 'flags':flags}
        if args.table_type.lower() in table.keys():
            if args.field.lower() in table[args.table_type.lower()].keys():
                print(table[args.table_type.lower()][args.field.lower()])
            else:
                print(f'"{args.field}" field not exist <{table[args.table_type.lower()].keys()}>.')
        else:
            print(f'"{args.table_type}" type not exist <{table.keys}>.')

    else:
        print(f'"{args.input}" not exists.')

class InputError(RuntimeError):
    def __init__(self, e):
        super(InputError, self).__init__(e)

if __name__ == '__main__':
    try:
        main()
    except InputError as e:
        print(e, file=sys.stderr)
        sys.exit(2)

