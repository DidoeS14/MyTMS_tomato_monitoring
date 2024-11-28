import configparser


class Config:
    def __init__(self, section: str):
        self.section = section

        try:
            self.config_file = configparser.ConfigParser()
            self.config_file.read('config.ini')
        except Exception as e:
            print(e)
            print('No config.ini file was found!')

    def get(self, key: str, fallback= None):
        return self.config_file.get(self.section, key, fallback=fallback)


class TomatoModelConfig:
    def __init__(self):
        config = Config('model')

        self.size_tomato_model_path: str = config.get('size_model', 'size.pt')
        self.disease_tomato_model_path: str = config.get('disease_model', 'disease.pt')

        self.size_tomato_confidence: float = float(config.get('size_confidence', 0.8))
        self.disease_tomato_confidence: float = float(config.get('disease_confidence', 0.8))

        self.size_tomato_ripened_count: int = int(config.get('size_ripened_count', 10))

        self.input_folder: str = config.get('input', 'test_inputs/')
        self.output_folder: str = config.get('output', 'test_results/')


class EmailConfig:
    def __init__(self):
        config = Config('email')

        self.smtp_server: str = config.get('smtp_server', 'smtp.gmail.com')
        self.port: int = int(config.get('port', 25))
        self.sender: str = config.get('sender', 'me@gmail.com')
        self.receiver: str = config.get('receiver', 'you@gmail.com')
        self.password: str = config.get('password', '123456')


class DatabaseConfig:
    def __init__(self):
        config = Config('database')

        self.username: str = config.get('username', 'root')
        self.host: str = config.get('host', 'localhost')
        self.port: int = int(config.get('port', 3306))
        self.database_name: str = config.get('name', 'tomato')
        self.password: str = config.get('password', '123456')

        self.URL: str = f'mysql+pymysql://{self.username}:{self.password}@{self.host}/{self.database_name}'





tomato_model_config = TomatoModelConfig()
email_config = EmailConfig()
database_config = DatabaseConfig()

if __name__ == '__main__':
    print(tomato_model_config.size_tomato_model_path)
    print(tomato_model_config.disease_tomato_model_path)
    print(tomato_model_config.size_tomato_confidence)
    print(tomato_model_config.size_tomato_ripened_count)
    print(tomato_model_config.disease_tomato_confidence)

    print(database_config)
