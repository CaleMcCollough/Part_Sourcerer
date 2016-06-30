# @project      Part-Sourcerer
# @copyright    Blue Storm Engineering, LLC. All rights reserved.
# @lincense     This project is released under the GNU Public License 3.0 (http://www.gnu.org/licenses/gpl-3.0.html).
# @author       Cale McCollough
# @date         01/15/2015
# @brief        This file contains the ComponentSourcerer class for Part-Sourcerer
# @description  ComponentSourcerer is an app that assists in sourcing electronics products from parts suppliers.
# 
#
# Minimal vs Verbose Metadata Importing Modes
# -----------------------------------------------------------------------------------------------------------------------------
# Users might not want a bunch of extra metadata fields clouding up the BOM export columns in 
# Becuase most part variants will share the same metadata, only fields that are different, are .
# Part-Sourcerer will soon feature its own BOM export tool that 
# 
# Importing Supplier Information:
# 
# In order to import the supplier component, The user specifies the URL to the part on digi-key using a metadata link with a field name of '[Supplier Code] Supplier URL'.
# Examples
# '0DK, 'http://www.digikey.com/product-detail/en/MCT06030C1002FP500/MCT0603-10.0K-CFTR-ND/1850440'
# The user then exports the library, runs the scripts, and all of the metadata for the part is now imported into the component library.

import abc
import os
import sys
import urllib2
import urlparse
import zipfile

import HTMLParser

from Sourcerer import Sourcerer
from SupplierProduct import SupplierProduct
from ComponentSupplier import ComponentSupplier
#from DigiKeySourcerer import DigiKeySourcerer

class ComponentSourcerer(object, HTMLParser):
    __metaclass__  = abc.ABCMeta
    
    # The current state of the parser.
    state = 0
    # The counter for the current state.
    counter = 0
    # The current item being recorded.
    index = 0
    # The current key being recorded.
    currentKey = ''
    # The current value being recorded.
    currentValue = ''
    # The current URL being recorded.
    currentURL = ''
    # The current pricing string being concatenated. 
    dataBuffer = ''
    # The project directory.
    projectDirectory = '/'
    # The current product being sourced.
    product =  SupplierProduct('', '', '')

    def __init__(self, projectDirectory):
        HTMLParser.__init__(self)
        self.projectDirectory = Sourcerer.cleanDirecoryPath(projectDirectory)
    
    # Abstract function that does some processing of the HTML document from the supplier's website.
    @abc.abstractmethod
    def processSupplierWebsiteHTML(self, htmlDoc):
        raise NotImplementedError
    
    @abc.abstractmethod
    def handleStartTag(self, tag, attrs):
        raise NotImplementedError
    
    @abc.abstractmethod
    def handleEndTag(self, tag):
        raise NotImplementedError
    
    @abc.abstractmethod
    def handleData(self, data):
        raise NotImplementedError
    
    # @brief    A function to be overridden by a subclass that handles the start of an HTML tag.
    # @desc     This is a state based reader. The parser enters the state in this function, logic is dealth with via a series 
    # of if then elif blocks that handle the logic for the various states. Each supplier website and ordering system is 
    # different, so the states will be different for each website, .
    def handle_starttag(self, tag, attrs):
        self.handleStartTag(tag, attrs) # Wrap to abstract function.
    
    # @brief    A function to be overridden by a subclass that handles the end of an HTML tag.
    # @desc     This is a state based reader. The parser enters the state in this function, logic is dealth with via a series 
    # of if then elif blocks that handle the logic for the various states.
    def handle_endtag(self, tag):
        self.handleEndTag(tag) # Wrap to abstract function.
    
    # @brief    A function to be overridden by a subclass that handles the data in an HTML tag.
    # @desc     This is a state based reader. The parser enters the state in this function, logic is dealth with via a series 
    # of if then elif blocks that handle the logic for the various states.
    def handle_data(self, data):
        self.handleData(data) # Wrap to abstract function.
    
    def recordURL(self, url):
        if 'javascript' in url: # Don't record javascript links.
            print '%%%Throwing out javascript link.'
            return
        
        if url.startswith('/'): # Then insert the http address of the supplier.
            self.currentURL = self.product.supplierDomain + url
        else:
            self.currentURL = url
        #print '%%% Recorded URL: ', self.currentURL
    
    # @brief    Function that opens and returns a HTML document from from a URL
    def loadFromFile(self, supplyCode, delineator, filename, url):
        #print 'Loading  ', filename
        file = open(filename, 'r')
        htmlDoc = file.read()
        file.close()
        
        fileURL = 'file:///' + filename
        
        self.loadFromHTML(supplyCode, delineator, htmlDoc, fileURL)
    
    def loadFromURL(self, supplyCode, delineator, url):
        htmlDoc = Sourcerer.loadContentFromURL(url)
        self.loadFromHTML(supplyCode, delineator, htmlDoc, url)
    
    # @brief    Function that loads a SupplierProduct from the htmlDoc.
    def loadFromHTML(self, supplyCode, delineator, htmlDoc, url):
        print 'Loading ', supplyCode, 'from URL:', url, '\nFilesize: ',len(htmlDoc)/1000, '(KB)'
        #print 'Printing htmlDoc...\n', htmlDoc
        #print '*************************************************************************************************\n'
        newComponent = SupplierProduct(supplyCode, delineator, url)
        self.changeState(0)
        self.product = newComponent
        
        
        htmlDoc = self.processSupplierWebsiteHTML(htmlDoc)
        
        self.feed(htmlDoc)
        
    def changeState(self, newState):
        print '\nLeaving State ', self.state, ', entering State ', newState
        self.state = newState
        self.printParams()
    
    def printParams(self):
        print '*************************************Parameter Dump **********************************************'
        print 'self.counter: ', self.counter
        print 'self.index: ', self.index
        print 'self.currentKey: ', self.currentKey
        print 'self.currentValue: ', self.currentValue
        print 'self.currentURL: ', self.currentURL
        print 'self.dataBuffer: ', self.dataBuffer
        print 'self.counter: ', self.counter
        print '*************************************************************************************************\n'
    
    # @brief    Function sources an EDAProduct from a specified URL.
    # @return   Returns 
    @staticmethod
    def sourceProductFromURL(self, manufactureringCode, delineator, url, supplierName):
        sourcerer = ComponentSourcerer('/')
        sourcerer.loadFromURL(supplyCode, delineator, url)
        return self.product
    
    class UnitTest():
        # @brief    Function that tag
        # @param    supplierProduct SupplierProduct
        @staticmethod
        def testImportEDAFiles(supplierProduct):
            metadata = supplierProduct.metadata
            for dataItem in metadata:
                
        
        # @brief    Function that runs diagnostics on the ComponentSourcerer class
        @staticmethod
        def runUnitTest():
            os.system('cls')
            print 'Running ComponentSourcerer diagnostics...\n'
            
            print 'Creating test DigiKeySourcerer...'
            #sourcerer = DigiKeySourcerer()
            
            print '\nDone running ComponentSourcerer diagnostics.\n'

ComponentSourcerer.UnitTest.runUnitTest()
