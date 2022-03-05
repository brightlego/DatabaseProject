"""Run this to setup the database"""

import subprocess
import sys

import backend.one_time_run.generate_db
import backend.one_time_run.populate_table


def install(package):
    """Installs a package through pip"""
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


# The dependancies
install("tkcalendar")

# Generate the database
backend.one_time_run.generate_db.main()

# Populate that database with data
backend.one_time_run.populate_table.main()
