import configparser


try:
    config_file = configparser.ConfigParser()
    config_file.read('config.ini')
except Exception as e:
    print(e)
    print('No config.ini file was found!')


class Config:
    def __init__(self, section: str):
        self.section = section

    def get(self, key: str, fallback=None, type: str = ''):
        if type == 'bool':
            return config_file.getboolean(self.section, key, fallback=fallback)
        if type == 'int':
            return config_file.getint(self.section, key, fallback=fallback)
        if type == 'float':
            return config_file.getfloat(self.section, key, fallback=fallback)
        else:
            return config_file.get(self.section, key, fallback=fallback)


class TomatoModelConfig:
    def __init__(self):
        config = Config('model')

        self.size_tomato_model_path: str = config.get('size_model', 'size.pt')
        self.disease_tomato_model_path: str = config.get('disease_model', 'disease.pt')

        self.size_tomato_confidence: float = config.get('size_confidence', 0.8, type='float')
        self.disease_tomato_confidence: float = config.get('disease_confidence', 0.8, type='float')

        self.size_tomato_ripened_count: int = config.get('size_ripened_count', 10, type='int')

        self.source: str = config.get('input', 'test_inputs/')
        self.output_folder: str = config.get('output', 'test_results/')

        self.show_stream: bool = config.get('show_stream', True, type='bool')
        self.save_images: bool = config.get('save_images', True, type='bool')


class ChartConfig:
    def __init__(self):
        config = Config('chart')

        self.output: str = config.get('output', 'test_results/')
        self.subdir: str = config.get('subdir', 'chart/')
        self.save: bool = config.get('save', False, type='bool')

class EmailConfig:
    def __init__(self):
        config = Config('email')

        self.smtp_server: str = config.get('smtp_server', 'smtp.gmail.com')
        self.port: int = config.get('port', 25, type='int')
        self.sender: str = config.get('sender', 'me@gmail.com')
        self.receiver: str = config.get('receiver', 'you@gmail.com')
        self.password: str = config.get('password', '123456')


class DatabaseConfig:
    def __init__(self):
        config = Config('database')

        self.username: str = config.get('username', 'root')
        self.host: str = config.get('host', 'localhost')
        self.port: int = config.get('port', 3306, type='int')
        self.database_name: str = config.get('name', 'tomato')
        self.password: str = config.get('password', '123456')

        self.URL: str = f'mysql+pymysql://{self.username}:{self.password}@{self.host}/{self.database_name}'





tomato_model_config = TomatoModelConfig()
chart_config = ChartConfig()
email_config = EmailConfig()
database_config = DatabaseConfig()

if __name__ == '__main__':

    print(tomato_model_config.save_images)
    print(tomato_model_config.show_stream)


    print(database_config)

    print(chart_config.subdir)
