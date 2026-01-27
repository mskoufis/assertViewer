#!/usr/bin/env python
#-----------------------------------------------------------------------------
# Title      : Script for running live display
#-----------------------------------------------------------------------------
import os
top_level = f'{os.getcwd()}/'
import setupLibPaths
import argparse
import pyrogue.pydm
import sys

from assertViewer import *


parser = argparse.ArgumentParser('Pyrogue Client')

parser.add_argument('--port',
                    type=str,
                    help="Zmq port: 'port''",
                    default='9099')

parser.add_argument('--serverList',
                    type=str,
                    help="Server address: 'host:port' or list of addresses: 'host1:port1,host2:port2'",
                    default='localhost:9099')

parser.add_argument('--dataReceiver',
                    type=str,
                    help='Rogue Data Receiver path string',
                    default=None)

parser.add_argument('--title',
                    type=str,
                    default=None,
                    help='Title of display')

parser.add_argument('cmd',
                    type=str,
                    choices=['event','particle','beam','channel','trajectory'],
                    help='Client command to issue')

parser.add_argument('--sizeY',
                    type=int,
                    default=1000,
                    help='Rows of image')

parser.add_argument('--sizeX',
                    type=int,
                    default=800,
                    help='Columns of image')

args = parser.parse_args()

if args.cmd == 'event':
    runReceiverDisplay(dataReceiver=args.dataReceiver, serverList=args.serverList, title=args.title, sizeY=args.sizeY, sizeX=args.sizeX)
elif args.cmd == 'particle':
    runParticleDisplay(dataReceiver=args.dataReceiver, serverList=args.serverList, title=args.title, sizeY=args.sizeY, sizeX=args.sizeX, port=args.port)
elif args.cmd == 'beam':
    runBeamDisplay(dataReceiver=args.dataReceiver, serverList=args.serverList, title=args.title, sizeY=args.sizeY, sizeX=args.sizeX, port=args.port)
elif args.cmd == 'channel':
    runChannelDisplay(dataReceiver=args.dataReceiver, serverList=args.serverList, title=args.title, sizeY=args.sizeY, sizeX=args.sizeX, port=args.port)
elif args.cmd == 'trajectory':
    pass
