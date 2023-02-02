import logging
import sys
from Converter import Converter

logging.basicConfig(filename='logs/system.log', filemode='w', level=logging.DEBUG)

def convert(file, tag, elements):    
    logging.info('Start script converter')
    converter = Converter(file, tag, elements)
    converter.run()
    logging.info('Finish script converter')

file, tag = '', ''
elements = []

if(len(sys.argv) > 1):
    file = sys.argv[1]
    tag = sys.argv[2]
    if len(sys.argv) > 3:
        elements = sys.argv[3].split(',')
        
    convert(file, tag, elements)
else:
    print('Error convert, please choose file and tag')
    print('python3 script.py [file] [tag] [tags separate by comma]')
    
    
# Example: 
# 
# Convert Xml to Prolog
# python3 script.py files/data.xml student
#
# Convert Prolog to Xml file
# python3 script.py files/data.pl student name,surname,age,direction