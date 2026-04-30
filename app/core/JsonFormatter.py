import json
import logging


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "level": record.levelname,
            "message": record.msg,
            "logger": record.name,
            "time": self.formatTime(record),
        }
        return json.dumps(log_record)
