from .client.Token import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--access', action="store_true")
args = parser.parse_args()
if args.access:
  print(access_token())
