import time

class Scraper(object):
    """base class for matrimeter scrapers"""
    def __init__(self):        
        self.last_run = None
    
    def _run(self):
        self.last_run = time.time()
    
    def run(self):
        """run the scraper. this method should be overridden by inheriting classes."""
        value = 0xFF # return a byte indicating the range of the result, 0-255
        timeout = 60 # how many seconds should the system wait until the next call?
        return (value, timeout)
        