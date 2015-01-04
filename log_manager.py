import logging

LEVELS = { 'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL}
            
class log_manager:

    log = None
    handler = None
    formatter = None
                    
    def __init__(self, file_path, type="DEBUG"):
        self.log = logging.getLogger("main")
        self.log.setLevel(LEVELS[type])
        
        
        self.handler = logging.FileHandler(file_path,"w")
        self.formatter = logging.Formatter("[%(asctime)s] - %(name)s.%(levelname)s - [%(module)s.%(funcName)s():%(lineno)d] - %(message)s")
        
        self.handler.setFormatter(self.formatter)
        self.handler.setLevel(LEVELS[type])
        
        self.log.addHandler(self.handler)