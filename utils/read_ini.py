import configparser

def loadLastAuto() -> str:
    config = configparser.ConfigParser()
    config.read('server.ini')
    return config.get('CONSULTAS', 'LASTAUTOFISCAL')


def loadConfigServer():
    config = configparser.ConfigParser()
    config.read('server.ini')
    ip= config.get('CONFIG', 'IP')
    puerto= config.get('CONFIG', 'PUERTO')
    query_time= config.get('CONFIG', 'QUERY_TIME')
    series= config.get('CONFIG', 'SERIES')
    return ip, puerto, float(query_time), series.split()

def updateAuto(auto : int) -> bool:
    config = configparser.ConfigParser  
    config.read('server.ini')
    config.set('CONSULTAS', 'LASTAUTOFISCAL', auto)
    with open('server.ini', 'w') as file:
        config.write(file)
    return True    