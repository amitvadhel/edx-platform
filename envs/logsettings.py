import os
import os.path
import platform
import sys

def get_logger_config(log_dir, 
                      logging_env="no_env", 
                      tracking_filename=None,
                      syslog_addr=None,
                      debug=False):
    """Return the appropriate logging config dictionary. You should assign the
    result of this to the LOGGING var in your settings. The reason it's done 
    this way instead of registering directly is because I didn't want to worry
    about resetting the logging state if this is called multiple times when 
    settings are extended."""

    # If we're given an explicit place to put tracking logs, we do that (say for
    # debugging). However, logging is not safe for multiple processes hitting 
    # the same file. So if it's left blank, we dynamically create the filename
    # based on the PID of this worker process.
    if tracking_filename:
        tracking_file_loc = os.path.join(log_dir, tracking_filename)
    else:
        pid = os.getpid() # So we can log which process is creating the log
        tracking_file_loc = os.path.join(log_dir, "tracking_{0}.log".format(pid))

    hostname = platform.node().split(".")[0]
    syslog_format = ("[%(name)s][env:{logging_env}] %(levelname)s [{hostname} " +
                     " %(process)d] [%(filename)s:%(lineno)d] - %(message)s").format(
                        logging_env=logging_env, hostname=hostname)

    handlers = ['console'] if debug else ['console', 'syslogger']

    return {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters' : {
            'standard' : {
                'format' : '%(asctime)s %(levelname)s %(process)d [%(name)s] %(filename)s:%(lineno)d - %(message)s',
            },
            'syslog_format' : { 'format' : syslog_format },
            'raw' : { 'format' : '%(message)s' },
        },
        'handlers' : {
            'console' : {
                'level' : 'DEBUG' if debug else 'INFO',
                'class' : 'logging.StreamHandler',
                'formatter' : 'standard',
                'stream' : sys.stdout,
            },
            'syslogger' : {
                'level' : 'INFO',
                'class' : 'logging.handlers.SysLogHandler',
                'address' : syslog_addr,
                'formatter' : 'syslog_format',
            },
            'tracking' : {
                'level' : 'DEBUG',
                'class' : 'logging.handlers.WatchedFileHandler',
                'filename' : tracking_file_loc,
                'formatter' : 'raw',
            },
        },
        'loggers' : {
            'django' : {
                'handlers' : handlers,
                'propagate' : True,
                'level' : 'INFO'
            },
            'tracking' : {
                'handlers' : ['tracking'],
                'level' : 'DEBUG',
                'propagate' : False,
            },
            'root' : {
                'handlers' : handlers,
                'level' : 'DEBUG',
                'propagate' : False
            },
            'mitx' : {
                'handlers' : handlers,
                'level' : 'DEBUG',
                'propagate' : False
            },
            'keyedcache' : {
                'handlers' : handlers,
                'level' : 'DEBUG',
                'propagate' : False
            },
        }
    }
