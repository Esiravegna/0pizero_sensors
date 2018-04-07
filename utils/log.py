from twiggy import quick_setup, log, levels
from core.config import settings

setting2level = {
	'CRITICAL': levels.CRITICAL,
	'DEBUG': levels.DEBUG,
	'DISABLED': levels.DISABLED,
	'ERROR': levels.ERROR,
	'INFO': levels.INFO,
	'NOTICE': levels.NOTICE,
	'WARNING': levels.WARNING
}

quick_setup(min_level=setting2level[settings['OPI_ZERO_SENSORS_LOGLEVEL']], file = settings['OPI_ZERO_SENSORS_LOGFILE'])