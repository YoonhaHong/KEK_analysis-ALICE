#!/usr/bin/env python3

import os
import glob
import sys
import re
import pathlib
import subprocess
import ROOT
import json5
import pandas as pd
import numpy as np
import argparse
import requests

from matplotlib import pyplot as plt
from matplotlib import style as style
from datetime import date, datetime


def send_mattermost_alert(webhook_url, message):
    payload = {
        "text": message
    }
    requests.post(webhook_url, json=payload)
