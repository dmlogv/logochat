import logging


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s:%(levelname)s:%(message)s'
    )


import server


if __name__ == '__main__':
    logging.debug('Try to init new server')
    server = server.Server(host='0.0.0.0', port=30000)
