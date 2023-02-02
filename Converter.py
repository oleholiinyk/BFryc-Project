import os
import time
import logging
import xml.etree.ElementTree as ET
from xml.dom import minidom
import pyparsing as pp

class Converter:
    
    XML_EXTENTION = '.xml'
    PROLOG_EXTENTION = '.pl'
    
    def __init__(self, file, tag, elements = []):
        self.file = file
        self.tag = tag
        self.elements = elements
        if elements:
            self.rootXml = minidom.Document()
        self.fileName = ''
        self.fileExtention = ''

        
    def setFileInfo(self):
        split_tup = os.path.splitext(self.file)
        self.fileName = split_tup[0]
        self.fileExtention = split_tup[1]
        
    def run(self):
        self.setFileInfo()
        
        logging.info('Check file extention...')
        if self.fileExtention == self.XML_EXTENTION:
            logging.info('File extention is "' + self.fileExtention +'"')
            logging.info('Lets start convert XML to Prolog')
            self.xml2Prolog()
            logging.info('Xml converted to prolog successful')
        elif self.fileExtention == self.PROLOG_EXTENTION:
            logging.info('file extention is "' + self.fileExtention +'"')
            logging.info('Lets start convert Prolog to Xml')
            self.prolog2Xml()
            logging.info('Prolog converted to Xml.')
        else:
            print('Wrong extention file')
        
        
        
    def xml2Prolog(self):
        tree = ET.parse(self.file)
        root = tree.getroot()
        prologContent = ''
        prologRow = ''
        logging.info('Start build prolog content...')
        for item in root.findall(self.tag):
            prologRow += item.tag + '('
            
            for index, child in enumerate(item):
                prologRow += child.text
                
                if index != len(item) - 1:
                    prologRow += ', '
                    
                
            prologRow += ').\n'
            logging.info('Process...')
            logging.info('Insert row: ' + prologRow)
            prologContent = prologRow
            logging.info('Row inserted successful\n')

        logging.info('Finish build prolog content...')
        logging.info('Insert prolog content to file...\n')
        with open(self.fileName +'.pl', 'w') as file:
            file.write(prologContent)
            logging.info('\n' + prologContent)
            logging.info('Content inserted successfull')
            
    def parserProlog(self):
        relationship = pp.Word(pp.alphas).setResultsName('relationship')

        number = pp.Word(pp.nums + '.')
        variable = pp.Word(pp.alphas)
        # an argument to a relationship can be either a number or a variable
        argument = number | variable
        arguments= (pp.Suppress('(') + pp.delimitedList(argument) +
                    pp.Suppress(')')).setResultsName('arguments')
        fact = (relationship + arguments).setResultsName('facts', listAllMatches=True)

        # a sentence is a fact plus a period
        sentence = fact + pp.Suppress('.')

        # self explanatory
        prolog_sentences = pp.OneOrMore(sentence)
        return prolog_sentences
                
                
    
    def prolog2Xml(self):
        logging.info('Open Xml file and get content...')
        file = open(self.fileName +self.PROLOG_EXTENTION, "r")
        content = file.readlines()
        parseProlog = self.parserProlog()
        
        logging.info('Create XML Tree Structure.')
        xml = self.xmlTree()
        logging.info('Start iteration prolog rows content.')
        for greet_string in content:
            logging.info('Try to parse prolog row:')
            logging.info(greet_string)
            try:
                result = parseProlog.parseString(greet_string)
                logging.info(result.relationship)
                logging.info(result.arguments)
                logging.info('Start fill Xml data:')
                self.fillXmlData(xml, result.arguments, result.relationship)
                logging.info('Finished fill data.')
            except ValueError:
                logging.error(ValueError)
            

        xml_str = self.rootXml.toprettyxml(encoding="UTF-8")
        
        newFileName = self.fileName + self.XML_EXTENTION
        with open(newFileName, "wb") as f:
            f.write(xml_str)
            
    def fillXmlData(self, xml, list, rootElement):
        xmlElement = self.rootXml.createElement(rootElement)
        xml.appendChild(xmlElement)
        
        for el, value in enumerate(list):        
            element = self.rootXml.createElement(self.elements[el])
            element.appendChild(self.rootXml.createTextNode(value))
            xmlElement.appendChild(element)
            logging.info('Data: ' + self.elements[el] + ": " + value)
            
    def xmlTree(self):        
        xml = self.rootXml.createElement('metadata')
        self.rootXml.appendChild(xml)
        return xml
    