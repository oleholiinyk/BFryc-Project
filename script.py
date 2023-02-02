import json
import logging
from Converter import Converter

logging.basicConfig(filename='logs/system.log', filemode='w', level=logging.DEBUG)

logging.info('Start script converter')
# converter = Converter('files/data.xml', 'student')
converter = Converter('files/data.pl', 'student', ['name', 'surname', 'age', 'direction'])
converter.run()
logging.info('Finish script converter')