import ConfigParser
import sys
import os
class BaseConfig(object):
    """
        Generic Config Object.
    """
    def __init__(self):
        config = ConfigParser.RawConfigParser()
        path=os.path.dirname( os.path.realpath(__file__))
        config_path = path + '/../config.ini'
        config.read(config_path)
        self.redis = config.get('configuration','redis')
        self.redisbackend = 'redis://%s/0' % self.redis
        self.redisbroker = 'redis://%s/1' % self.redis
        os.environ['VAGRANT_CWD'] = config.get('configuration', 'vagrantlocation')
