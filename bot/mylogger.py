import logging


class MyLogger(logging.Logger):
    def __init__(self, name='noname',
                 filename=None, dir_logs='./logs/',
                 levels=(logging.DEBUG, logging.INFO)
                 ):
        self.name = name
        super().__init__(name)
        formats = logging.Formatter(
            '[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%dT%H:%M:%S')
        self.setLevel(logging.DEBUG)
        c_handler = logging.StreamHandler()
        c_handler.setLevel(levels[0])
        c_handler.setFormatter(formats)
        self.addHandler(c_handler)
        if not filename is None:
            self.filename = dir_logs+'/'+filename
            f_handler = logging.FileHandler(self.filename)
            f_handler.setLevel(levels[1])
            f_handler.setFormatter(formats)
            self.addHandler(f_handler)
