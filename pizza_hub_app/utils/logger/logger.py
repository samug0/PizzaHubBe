import logging
import os
from datetime import datetime
from pizza_hub.settings import BASE_DIR


log_directory = os.path.join(BASE_DIR, 'log', 'app', datetime.now().strftime('%Y'), datetime.now().strftime('%m'), datetime.now().strftime('%d'))
os.makedirs(log_directory, exist_ok=True)

class AppLogger:

    def __init__(self, name : str, level=logging.INFO) -> None:
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        # Definizione del path del file di log
        log_filename = os.path.join(log_directory, f'app-log-{datetime.now().strftime('%Y-%m-%d')}.log')
        # Creazione e configurazione dell'handler
        handler = logging.FileHandler(log_filename, mode='a', encoding='utf-8')
        formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(name)-15s [PID:%(process)d TID:%(thread)d] %(message)s')
        handler.setFormatter(formatter)
        
        # Aggiunta dell'handler al logger
        self.logger.addHandler(handler)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)

    






