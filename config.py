import yaml

class Config:
    def __init__(self, path):
        with open(path,'r') as yaml_file:
            self.config = yaml.load(yaml_file,Loader=yaml.FullLoader)

    def get_config(self, application):
        return self.config.get(application)