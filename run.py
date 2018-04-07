#!/usr/bin/env python
from core.controller import SensorsController
from utils.log import log

import click
from daemonocle.cli import DaemonCLI

log = log.name(__name__)
@click.command(cls=DaemonCLI, daemon_params={'pidfile': '/var/run/opi0sensors.pid'})
def run_daemon():
	log.info("Starting daemon...")
	s = SensorsController()
	s.start()


if __name__ == '__main__':
    run_daemon() 