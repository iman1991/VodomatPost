#!/usr/bin/python3.5
# -*- coding: utf-8 -*-
import os
import argparse


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', nargs='*')
    parser.add_argument('--server', nargs='?')
    parser.add_argument('--login', nargs='?')
    parser.add_argument('--password', nargs='?')
    parser.add_argument('--dir', nargs='?')
    return parser

if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args()

    os.system(r"\Проекты\project\forbot\pscp.exe -pw 230896 -r  C:\Users\Lion\Google Диск\VodomatPost   lio@194.67.217.180:/home/lio/srv")
