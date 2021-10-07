import logging

class MyLogger(logging.Logger):
    def __init__(self, name='noname',
                 filename=None, dir_logs='./logs/',
                 levels=(logging.DEBUG, logging.INFO)
                 ):
        self.name = name
        super().__init__(name)
        #super().getLogger(self.name)
        formats = logging.Formatter(
            '[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%dT%H:%M:%S')
        self.setLevel(logging.DEBUG)
        self.c_handler = logging.StreamHandler()
        self.c_handler.setLevel(levels[0])
        self.c_handler.setFormatter(formats)
        self.addHandler(self.c_handler)
        if not filename is None:
            self.filename = dir_logs+'/'+filename
            self.f_handler = logging.FileHandler(self.filename)
            self.f_handler.setLevel(levels[1])
            self.f_handler.setFormatter(formats)
            self.addHandler(self.f_handler)
