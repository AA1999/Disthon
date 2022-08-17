import math
from numbers import Integral
import os, sys;

sys.path.append(os.path.abspath("discord"));

from tests import bot

from argparse import ArgumentParser

parser = ArgumentParser(usage = "python3 run_tests.py <test module name> -t <TOKEN>")

parser.add_argument("test", nargs = "*")

parser.add_argument("-token", "-t")

args = parser.parse_args()

for test in args.test:
	exec(f"from tests.{test} import run; run('{args.token}')")