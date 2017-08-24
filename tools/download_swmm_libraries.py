#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Download compiled libraries from libswmm package and update pyswmm package.
"""

# Standard library imports
import json
import subprocess

# Third party imports
import requests


def packages(version, platform=None, channel='conda-forge'):
    """"""
    if platform is None:
        platforms = {'win-32': [], 'win-64': [], 'linux-64': [], 'osx-64': []}
    else:
        platforms = {platform: []}

    for platform in platforms:
        cmd = ['conda', 'search', 'libswmm', '-c', channel, '--json',
               '--platform', platform]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        stdout = stdout.decode()
        stderr = stderr.decode()
        all_data = json.loads(stdout)
        for data in all_data['libswmm']:
            ver = data['version']
            if version == ver:
                url = data['url']
                timestamp = data['timestamp']
                platforms[platform].append((timestamp, url))

    for platform in platforms:
        if 'win' in platform:
            pass
        else:
            platforms[platform] = sorted(platforms[platform])

    return platforms


def download_extract(urls):
    """"""
    for platform in urls:
        pass


if __name__ == '__main__':
    urls = packages('5.2.0.dev0', channel='owa')
    print(urls)
