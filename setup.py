import subprocess
import sys

import backend.one_time_run.generate_db
import backend.one_time_run.populate_table


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


install("tkcalendar")

backend.one_time_run.generate_db.main()
backend.one_time_run.populate_table.main()
