import logging


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s:%(levelname)s:%(message)s'
    )


import client.gui


if __name__ == '__main__':
    logging.debug('Try to init new client')
    gui = client.gui.Gui(host='127.0.0.1', port=30000)
