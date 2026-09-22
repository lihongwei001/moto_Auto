import logging
import os
from datetime import datetime

class LogUtil:
    _logger = None
    @classmethod
    def get_logger(cls):
        if cls._logger is None:
            cls._logger = logging.getLogger("autotest")
            cls._logger.setLevel(logging.INFO)
            if not os.path.exists("logs"):
                os.mkdir("logs")
            log_file = os.path.join("logs", f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
            fh = logging.FileHandler(log_file, encoding="utf-8")
            sh = logging.StreamHandler()
            fmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            fh.setFormatter(fmt)
            sh.setFormatter(fmt)
            cls._logger.addHandler(fh)
            cls._logger.addHandler(sh)
        return cls._logger

logger = LogUtil.get_logger()
