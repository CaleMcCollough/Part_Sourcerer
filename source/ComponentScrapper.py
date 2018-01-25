# @project      Part-Tools
# @copyright    Cale McCollough. All rights reserved.
# @lincense     This project is released under the GNU Public License 3.0 (http://www.gnu.org/licenses/gpl-3.0.html).
# @author       Cale McCollough
# @date         01/15/2015
# @brief        This file contains the EDAScrapper class for EDA-Tools
# @description  EDAScrapper is an app that assists in sourcing electronics components from parts suppliers.
# 

import sys
import requests
import urllib2
import os
import re
import urlparse
import zipfile

from HTMLParser import HTMLParser

from SupplierProduct import SupplierProduct
from ComponentSupplier import ComponentSupplier

class EDAScrapper(HTMLParser):
    # The current state of the parser.
    state = 0
    # The counter for the current state.
    counter = 0
    # The current item being recorded.
    itemNumber = 0
    # The current key being recorded.
    currentKey = ''
    # The current value being recorded.
    currentValue = ''
    # The current URL being recorded.
    currentURL = ''
    # The current pricing string being concatenated. 
    recordingString = ''
    # The project directory.
    projectDirectory = '/'
    # The current component being loaded.
    component =  SupplierProduct('', '', '')
    # A list of URLs with the
    component3DModels = []
    
    edaFileExtentions = { '.pdf', '.zip', '.stp', '.iges' }

    def __init__(self, projectDirectory):
        HTMLParser.__init__(self)
        self.projectDirectory = self.cleanDirecoryPath(projectDirectory)
    
    def cleanDirecoryPath(self, directoryPath):
        if os.path.isdir(directoryPath):
            return directoryPath
        return '/'
    
    def sourceComponent(self, url):
        newComponent = EDAComponent()
    
    def recordURL(self, url):
        if 'javascript' in url: # Don't record javascript links.
            print '%%%Throwing out javascript link.'
            return
            
        if url.startswith('/'): # Then insert the http address of the supplier.
            self.currentURL = self.component.supplierDomain + url
        else:
            self.currentURL = url
        #print '%%% Recorded URL: ', self.currentURL
    
    # @brief    Function that opens and returns a HTML document from from a URL
    def loadFromFile(self, supplyCode, delineator, filename, url):
        #print '###filename = ', filename
        file = open(filename, 'r')
        htmlDoc = file.read()
        file.close()
        
        fileURL = 'file:///' + filename
        
        self.loadFromHTML(supplyCode, delineator, htmlDoc, fileURL)
        #self.loadFromHTML(supplyCode, delineator, htmlDoc, url)
    
    def loadFromURL(self, supplyCode, delineator, url):
        htmlDoc = EDAScrapper.loadContentFromURL(url)
        self.loadFromHTML(supplyCode, delineator, htmlDoc, url)
        
    def loadFromHTML(self, supplyCode, delineator, htmlDoc, url):
        print 'Loading ', supplyCode, 'from URL:', url, '\nFilesize: ',len(htmlDoc)/1000, '(KB)'
        #print 'Printing htmlDoc...\n', htmlDoc
        #print '*************************************************************************************************\n'
        newComponent = SupplierProduct(supplyCode, delineator, url)
        
        if '<CS=0><RF=141>' in htmlDoc:
            print '$$$ Found <CS=0><RF=141> in htmlDoc'
        
        htmlDoc = htmlDoc.replace('<CS=0><RF=141>', '') # Some weird funky non-standard junk in the HTML code.
        self.changeState(0)
        self.component = newComponent
        self.feed(htmlDoc)
        
    def changeState(self, newState):
        print '\nLeaving State ', self.state, ', entering State ', newState
        self.state = newState
        self.printParams()
        
    def printParams(self):
        print '*************************************Parameter Dump **********************************************'
        print 'self.counter: ', self.counter
        print 'self.itemNumber: ', self.itemNumber
        print 'self.currentKey: ', self.currentKey
        print 'self.currentValue: ', self.currentValue
        print 'self.currentURL: ', self.currentURL
        print 'self.recordingString: ', self.recordingString
        print 'self.counter: ', self.counter
        print '*************************************************************************************************\n'
        
    # @brief    This function handles the start of an HTML tag.
    # @desc     This is a state based reader. The parser enters the state in this function, and leaves in the handle_endttag 
    # function. This function also handles the counters that step between the table columns. Each state will use a different 
    # counter.
    def handle_starttag(self, tag, attrs):    
        component = self.component      # Create local reference
        # We are really only concerned with three tags: The <TABLE>, <TH>, <TD>, and <A> tags.
        
        currentState = self.state
        
        if currentState == 0: # Do Nothing State.
            # Look for state switching conditions
            if tag == 'table':
                for name, value in attrs:
                    if name == 'class':
                        if value == 'product-details': # Go to state 1
                            self.changeState(1)
                        elif value == 'product-additional-info':
                            self.changeState(3)
                            return
                        elif value == 'more-expander product-details-alternate-packaging':
                            self.counter = 7 # The counter gets pre-incremented
                            self.itemNumber = 1 # Set the current item number being processed to 1
                            self.currentKey = 'Alternate Packing ' # Prep the currentKey string
                            self.changeState(5)
                        return
        elif currentState == 1: # Recording TH-TD formatted metadata.
            if tag == 'th': # Start recording the TH.
                print '<TH>'
                self.currentKey = ''
                self.counter = 1
            elif tag == 'td': # Start recording the TD.
                print '<TD>'
                self.currentValue = ''
                self.counter = 2
            elif tag == 'table':
                for name, value in attrs:
                    if name == 'id' and value == 'pricing':   # Go to State 2 to start recording pricing
                        print '<table id="pricing">'
                        self.changeState(2)
                        self.counter = 3 # We want the counter to be at 3 because it gets preincremented later.
                        self.recordingString = ''
                    elif name == 'class' and value == 'more-expander product-details-alternate-packaging': # Go to State 3 to start recording additional product info.
                        print '<table class="more-expander product-details-alternate-packaging">'
                        self.changeState(3)
        elif currentState == 2:
            if tag == 'td': # Combine the price table to one string by iterating through the 3 columns.
                print '<TD>'
                self.currentValue = ''
                if self.counter == 1:
                    self.counter = 2
                elif self.counter == 2:
                    self.counter = 3
                elif self.counter == 3:
                    self.counter = 1
                    return
        elif currentState == 3: # Recording TH-TD formatted metadata.
            if tag == 'th': # Start recording the TH.
                print '<TH>'
                self.currentKey = ''
                self.counter = 1
            elif tag == 'td': # Start recording the TD.
                print '<TD>'
                self.currentValue = ''
                self.counter = 2
            elif tag == 'a': # Then go to State 4 to parse the link(s)
                for key, value in attrs:
                   if key == "href":
                        self.recordURL(value)
                self.itemNumber = 1
                self.changeState(4)
        elif currentState == 4: # Recording Additional Product Details Links
            if tag == 'a': # Then we need to record one of multiple links
                linkKey = self.currentValue + ' ' + str(self.itemNumber)
                self.currentValue = ''
                self.currentURL = ''
        elif currentState == 5: # Parsing alternate packaging
            if tag == 'td': # Increment loop counter
                self.currentValue = ''
                self.counter += 1
                if self.counter > 7: # Then reset the counter and the recording String
                    self.counter = 1
                    self.recordingString = '' # Reset the value string we are recording to.
                    # Delete me!
                    #self.itemNumber += 1
                    #self.currentKey = 'Alternate Package ' + str(self.itemNumber)
                print "counter = ", self.counter
            if tag == 'a':
                if self.counter == 1: # We only need to record the URL on the first TD.
                    for key, value in attrs:
                        if key == 'href':
                            self.recordURL(value)
            return
    
    def handle_endtag(self, tag):
        curretState = self.state
        component = self.component
        if curretState == 0:
            return
        elif curretState == 1: # Add TH-TD formated metadata
            if tag == 'td': # The metadata isn't added till we import both the TH, and the TD fields
                if self.currentKey != '': # We can't add a key with no name!!!
                    component.addMetadata(self.currentKey, self.currentValue)
                    if self.currentKey == 'Manufacturer':
                        component.manufacturer = self.currentValue
                    elif self.currentKey == 'Manufacturer Part Number':
                        component.puid = self.currentValue
            elif tag == 'th': # Debugging only
                print self.currentKey, '\n</TH>' # Debugging only
            elif tag == 'table':
                self.changeState(0) #
        elif curretState == 2: # The add the supplier pricing info to the metadata
            if tag == 'table':
                # Remove the final comma from the recordingString
                recordingString = self.recordingString[0:len(self.recordingString)-2]
                component.addMetadata('Pricing', recordingString)
                
                print '\n</table>\n'
                self.currentKey = ''
                self.changeState(1)
        elif curretState == 3:
            if tag == 'td': # The metadata isn't added till we import both the TH, and the TD fields
                tempKey = self.currentKey
                tempValue = self.currentValue
                if tempKey != '': # We can't add a key with no name!!! 
                    component.addMetadata(tempKey, tempValue)
            elif tag == 'th': # Debugging only
                print self.currentKey, '\n</TH>' # Debugging only
            elif tag == 'table':
                self.changeState(0)
                print '\n\n</table> (product-additional-info table)'
        elif curretState == 4: # Parsing links
            if tag == 'a': # Then parse a link
                #if not bool():
                #    return
                linkKey = self.currentKey
                if self.itemNumber > 1: # If there are more than one links, add a number to the end of the string
                    linkKey += ' ' + str(self.itemNumber)
                print 'self.currentValue = ', self.currentValue, ', self.itemNumber = ', self.itemNumber, ', linkKey = ', linkKey
                component.addMetadata(linkKey, self.currentValue)
                component.addMetadata(linkKey + ' URL', self.currentURL)
                if self.currentKey == '3D Model':
                    self.component3DModels += self.currentURL
                self.changeState(3)
        elif curretState == 5:
            if tag == 'td':
                self.recordingString += self.currentValue + ', '
                #print '$$$ self.recordingString = ', self.recordingString
                if self.counter == 7:
                    print '@@@ Reached end of TR'
                    component.addMetadata(self.currentKey, self.recordingString)
                    self.recordingString = '' # Reset the recordingString
                    #self.currentValue = ''
                    if self.currentURL != '':
                        newFiledTitle = self.currentKey + ' URL'
                        component.addMetadata(newFiledTitle, self.currentURL)
                        
                        if currentKey == '3D Model':
                            self.component3DModels += self.currentURL
                            
                elif self.counter == 4: # Then this is the packing option text
                    self.currentKey = 'Alternate Package: ' + self.currentValue
                    print 'Found Packing Title: ', self.currentKey
            elif tag == 'a': # Done parsing link
                self.recordURL(self.currentURL)
                self.itemNumber -= 1
            elif tag == 'table':
                self.changeState(0); # go back to the do nothing state.
    
    def handle_data(self, data):
        component = self.component
        currentState = self.state
        
        if currentState == 0:
            return
        data = data.strip()             # strip out around string
        data = data.replace('\n', '')   # remove NL chars
        data = re.sub(' +',' ', data)   # remove extra whitespaces by magic :-)
        if currentState == 1 or currentState == 3:
            if self.counter == 1: 
                self.currentKey += data
                #print 'currentKey = ', self.currentKey
            elif self.counter == 2:
                self.currentValue += data + ' '
                #print 'currentValue = ', self.currentValue
        elif currentState == 2: # Recording pricing
            data = data.strip() # Strip all white space from the data.
            if len(data) == 0 or data[0].isalpha (): # Then its the TH, so skip.
                return
            data = data.replace(',', '') # Converting a number with a comma casuses error.
            counterValue = self.counter
            if counterValue == 1: # Add the pricing quanitiy with the data
                print 'Found pricing quanitiy: ', data
                self.recordingString += data
                self.recordingString += '='
            elif counterValue == 2: # Add the recordingString with the data
                print 'Found quanitiy price: ', data
                self.recordingString += data
                self.recordingString += ', '
        elif currentState == 4: # Then store the URL link name
            self.currentValue += data
        elif currentState == 5: # Parsing alternative packaging options.
            self.currentValue += data
    
    def downloadFileSilently(self, url):
        response = urllib2.urlopen(url)
        html = response.read()
    
    def downloadFile(self, url):
        file_name = url.split('/')[-1]
        u = urllib2.urlopen(url)
        f = open(file_name, 'wb')
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        print "Downloading: %s Bytes: %s" % (file_name, file_size)

        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)
            status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
            status = status + chr(8)*(len(status)+1)
            print status,

        f.close()
    
    # Returns True if the url contains a known EDA file extension
    def urlContainsEDAFile(self, url):
        for fileType in self.edaFileExtentions:
            if fileType in url:
                return True
        return False
    
    def downloadEDAFiles(self):
        for key, value in self.metadata:
            if currentKeyendswith(' URL') and urlContainsEDAFile(value):
                self.downloadFile(value)
    
    def downloadEDAFilesSilently(self):
        for key, value in self.metadata:
            if ' URL' in currentKey and urlContainsEDAFile(value):
                self.downloadFileSilently(value)
    
    # @brief    Function sources an EDAProduct from a specified URL.
    # @return   Returns 
    @staticmethod
    def sourceProductFromURL(self, manufactureringCode, delineator, url, supplierName):
        sourcerer = EDAScrapper('/')
        sourcerer.loadFromURL(supplyCode, delineator, url)
        return self.component
    
    @staticmethod
    def testFromURLList():
        print "Running testFromURLList()...\n"
        
        testURLList = { 'http://www.digikey.com/product-detail/en/5035480620/WM4639TR-ND/2573768', \
                        'http://www.digikey.com/product-detail/en/5015911011/WM6837TR-ND/3045238', \
                        'http://www.digikey.com/product-detail/en/0781560001/WM7358-ND/2046754', \
                        'http://www.digikey.com/product-detail/en/0879180001/WM2066-ND/1643335', \
                        'http://www.digikey.com/product-detail/en/640454-4/A19431-ND/258986', \
                        'http://www.digikey.com/product-detail/en/1565917-4/A97498TR-ND/1619799', \
                        'http://www.digikey.com/product-detail/en/1612618-4/A114913-ND/2187770', \
                        'http://www.digikey.com/product-detail/en/SJ-2523-SMT-TR/CP-2523SJTR-ND/281300', \
                      }
    
        for url in testURLList:
            EDAScrapper.testFromURL (url)
    
        print '\nDone running testFromURLList().\n'
        
    @staticmethod
    def testFromFile():
        print "Testing import from file...\n"
        
        sourcerer = EDAScrapper('')
        #sourcerer.loadFromFile('0D', '.', 'DigiKeyTestFiles/DigiKeyPriceTable.html', 'http://www.digikey.com/test/')
        #sourcerer.loadFromFile('0D', '.', 'DigiKeyTestFiles/DigiKeyProductInfoTable.html', 'http://www.digikey.com/test/')
        #sourcerer.loadFromFile('0D', '.', 'DigiKeyTestFiles/DigiKeyAdditionalInfoTable.html', 'http://www.digikey.com/test/')
        #sourcerer.loadFromFile('0D', '.', 'DigiKeyTestFiles/DigiKeyMetadataTest.html', 'http://www.digikey.com/test/')
        sourcerer.loadFromFile('0D', '.', 'DigiKeyTestFiles/DigiKeyTest.html', 'http://www.digikey.com/test/')
        
        print '\n**********************************************************'
        print 'Printing imported SupplierComponent...\n'
        
        print 'Done testingFromFile()\n'
        print sourcerer.component.toString()
        
    @staticmethod
    def loadContentFromURL(url):
        print 'Loading conent from URL: ', url
        htmlDoc = requests.get(url).content
        #response = urllib2.urlopen(url)
        #htmlDoc = response.read()
        return htmlDoc
        
    @staticmethod
    def saveDataToFile(data, filename):
        print 'Saving data to file: ', filename
        try:
            open(filename, 'w').close()
            os.unlink(filename)
            print('filename is valid.')
        except OSError:
            print('Error: filename not valid: ', filename)
            return
        
        file = open(filename, 'w')
        file.write(data)
        file.close
    
    @staticmethod
    def testFromURL(url):
        print '\nRunning testFromURL("', url, '")...\n'
        
        #EDAScrapper.saveDataToFile(EDAScrapper.loadContentFromURL(url), 'DigiKeyTestFiles/DigiKeyOnlineTest.html')
        
        sourcerer = EDAScrapper('/')
        sourcerer.loadFromURL('0D', '.', url)
        print sourcerer.component.toString()
        
        print 'Downloading 3D Models to: '<
    
        print '\nDone running testFromURL.\n'
    
    # @brief    function that runs diagonistics on the EDAScrapper class
    @staticmethod
    def runDiagnostics():
        os.system('cls')
        print 'Running EDAScrapper tests...\n'
        
        #EDAScrapper.testFromFile()
        EDAScrapper.testFromURL('http://www.digikey.com/product-detail/en/0879180001/WM2066-ND/1643335')
        #EDAScrapper.testFromURLList ()
        
        print '\nDone runningEDAScrapper tests.\n'

EDAScrapper.runDiagnostics()
