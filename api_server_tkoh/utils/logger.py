import logging
import logging.config
import logging.handlers
import os
import sys


class Logger:
    _logging_config_load_flag = False
    _logger = None
    _logfile_prefix = None

    @classmethod
    def run(cls, logger_name='ust_flask_api_server'):
        if not Logger._logging_config_load_flag:
            top_level_dir = os.path.dirname(sys.argv[0])
            print(top_level_dir)
            Logger._logger = logging.getLogger(logger_name)
            Logger._logger.setLevel(logging.INFO)

            # log file output setting
            os.makedirs(os.path.join(top_level_dir, 'logs/'), exist_ok=True)
            Logger._logfile_prefix = os.path.join(top_level_dir, 'logs/') + logger_name
            log_file_name = Logger._logfile_prefix + '.log'
            log_file_handler = logging.handlers.TimedRotatingFileHandler(log_file_name, when='D', encoding='utf-8')
            log_file_handler.setLevel(logging.INFO)
            bugs_formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')
            log_file_handler.setFormatter(bugs_formatter)
            Logger._logger.addHandler(log_file_handler)

            # console output setting
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.ERROR)
            console_formatter = logging.Formatter("[%(levelname)s] %(message)s")
            console_handler.setFormatter(console_formatter)
            Logger._logger.addHandler(console_handler)

            Logger._logging_config_load_flag = True

    @classmethod
    def warning(cls, msg):
        Logger.run()
        Logger._logger.warning(msg)

    @classmethod
    def debug(cls, msg):
        Logger.run()
        Logger._logger.debug(msg)

    @classmethod
    def error(cls, msg):
        Logger.run()
        Logger._logger.error(msg)

    @classmethod
    def info(cls, msg):
        Logger.run()
        Logger._logger.info(msg)

    @classmethod
    def critical(cls, msg):
        Logger.run()
        Logger._logger.critical(msg)
