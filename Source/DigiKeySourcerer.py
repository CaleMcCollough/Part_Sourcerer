# @project      Part-Sourcerer
# @copyright    Blue Storm Engineering, LLC. All rights reserved.
# @lincense     This project is released under the GNU Public License 3.0 (http://www.gnu.org/licenses/gpl-3.0.html).
# @author       Cale McCollough
# @date         01/15/2015
# @brief        This file contains the DigiKeySourcerer class for Part-Sourcerer
# @description  DigiKeySourcerer is an app that assists in sourcing electronics products from parts suppliers.
# 
# Digi-Key Website Format: 
# -----------------------------------------------------------------------------------------------------------------------------
# All products on the Digi-key website have the same basic format and a single script can parse the metadata from any page. 
# 
# Digi-key.com Wesite Format
# 
# First er have to parse the product-details table. Here is the basic layout of the cells we want to extract.
# <body>
#   ...
#   <table class="product-details">
#       <tr><th>Digi-Key Part Number</TH><TD>Value</td></tr>
#       <tr><td>
#           <table id="pricing>
#               <tr><td>Quantity 1</td><td>Price 1</td><td>Externded Price 1</td>
#                   <td>Quantity 2<td><td>Price 2</td><td>Externded Price 2</td>
#                   <td>Quantity 3<td><td>Price 2</td><td>Externded Price 3</td>
#                   ...
#                   <td>Quantity N</td><td>Price N</td><td>Externded Price N</td>
#               </tr>
#           </table>
#       </td><td></td></tr>
#       <tr><th>Quantity Available</TH><TD>Value</td></tr>
#       <tr><th>Manufacturer</TH><TD>Value</td></tr>
#       <tr><th>Manufacturer Part Number</TH><TD>Value</td></tr>
#       <tr><th>Description</TH><TD>Value</td></tr>
#       <tr><th>Lead Free Status / RoHS Status</TH><TD>Value</td></tr>
#   </table>
#   ...
#   <table class="product-details-table">
#       <table>
#           <tr><th>Property/Link 1</TH><TD>Value/URL</td></tr>
#           <tr><th>Property/Link 2</TH><TD>Value/URL</td></tr>
#           <tr><th>Property/Link 3</TH><TD>Value/URL</td></tr>
#           ...
#           <tr><th>Property/Link N</TH><TD>Value/URL</td></tr>
#       </table>
#   </table>
#   ...
#   <table class="more-expander product-details-alternate-packaging">
#       <tr>
#           <th>Digi-Key Part Number</th>
#           <th>Manufacturer Part Number</th>
#           <th>Manufacturer</th>
#           <th>Packaging</th>
#           <th>Quantity Available</th>
#           <th>Unit Price</th>
#           <th>Minimum Quantity</th>
#       </tr>
#       <tr><td>Alt Digi-Key Part # 1</td><td></td><td></td><td></td><td></td></tr>
#       <tr><td>Alt Digi-Key Part # 1</td><td></td><td></td><td></td><td></td></tr>
#       ...
#       <tr><td>Alt Digi-Key Part # 1</td><td></td><td></td><td></td><td></td></tr>
#   </table>
#   ...
# </body>
#
# The coder for parsing the product-details table is the exact same as the code to parse the product-details-table, with the 
# exeption of some additional logic to handle the unnamed nested table.
# 
# State List
# State 0: Do Nothing
# Description: State does nothing waiting for entry conditions to other states
# Entry Condition: Initial State and exits from states 1, 3, and 5
# Exit Condition: End of document
# 
# State 1: Parse product-details table
# Description: State parses the table with the supplier part number/PUID, pricing information, etc
# Entry Condition: <table class="product-details">
# Exit Condition: </table>
# 
# State 2: Parse pricing table
# Description: 
# Entry Condition: <table id="pricing">
# Exit Condition: </table>
# 
# State 3: Parse additional-product-details table
# Description: 
# Entry Condition: <table class="additional-product-details">
# Exit Condition: </table>
# 
# State 4: Parse additional-product-details table link
# Description: 
# Entry Condition: <a>
# Exit Condition: </a>
# 
# State 5: Parse Alternative Packaging Options.
# Description: 
# Entry Condition: <table class="more-expander product-details-alternate-packaging">
# Exit Condition: </table>
#
# State Diagram
#  t=0 ->
#           ---------------------------------------------------------------
# (Start)->|                           State 0                             | ->(Exit)
#           ---------------------------------------------------------------
#              ^                          ^                          ^
#              |                          |                          |
#              v                          v                          v
#          ---------     ---------    ---------     ---------    ---------
#         | State 1 |<->| State 2 |  | State 3 |<->| State 4 |  | State 5 |
#          ---------     ---------    ---------     ---------    ---------
#

import os
import re

from ComponentSourcerer import ComponentSourcerer

class DigiKeySourcerer(ComponentSourcerer):
    #__metaclass__ = ComponentSourcerer
    
    def __init__(self, projectDirectory):
        ComponentSourcerer.__init__(self, projectDirectory)
        
    # Function that removes some junk HTML data from the htmlDoc that messes up the parser.
    def processSupplierWebsiteHTML(self, htmlDoc):
        if '<CS=0><RF=141>' in htmlDoc:
            print '$$$ Found <CS=0><RF=141> in htmlDoc'
        htmlDoc = htmlDoc.replace('<CS=0><RF=141>', '') # Some weird funky non-standard junk in the HTML code.
        return htmlDoc
    
    def handleStartTag(self, tag, attrs):    
        product = self.product      # Create local reference
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
                            self.index = 1 # Set the current item number being processed to 1
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
                        self.dataBuffer = ''
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
                self.index = 1
                self.changeState(4)
        elif currentState == 4: # Recording Additional Product Details Links
            if tag == 'a': # Then we need to record one of multiple links
                linkKey = self.currentValue + ' ' + str(self.index)
                self.currentValue = ''
                self.currentURL = ''
        elif currentState == 5: # Parsing alternate packaging
            if tag == 'td': # Increment loop counter
                self.currentValue = ''
                self.counter += 1
                if self.counter > 7: # Then reset the counter and the recording String
                    self.counter = 1
                    self.dataBuffer = '' # Reset the value string we are recording to.
                    # Delete me!
                    #self.index += 1
                    #self.currentKey = 'Alternate Package ' + str(self.index)
                print "counter = ", self.counter
            if tag == 'a':
                if self.counter == 1: # We only need to record the URL on the first TD.
                    for key, value in attrs:
                        if key == 'href':
                            self.recordURL(value)
            return
    
    def handleEndTag(self, tag):
        curretState = self.state
        product = self.product
        if curretState == 0:
            return
        elif curretState == 1: # Add TH-TD formated metadata
            if tag == 'td': # The metadata isn't added till we import both the TH, and the TD fields
                if self.currentKey != '': # We can't add a key with no name!!!
                    product.addMetadata(self.currentKey, self.currentValue)
                    if self.currentKey == 'Manufacturer':
                        product.manufacturer = self.currentValue
                    elif self.currentKey == 'Manufacturer Part Number':
                        product.puid = self.currentValue
            elif tag == 'th': # Debugging only
                print self.currentKey, '\n</TH>' # Debugging only
            elif tag == 'table':
                self.changeState(0) #
        elif curretState == 2: # The add the supplier pricing info to the metadata
            if tag == 'table':
                # Remove the final comma from the dataBuffer
                dataBuffer = self.dataBuffer[0:len(self.dataBuffer)-2]
                product.addMetadata('Pricing', dataBuffer)
                
                print '\n</table>\n'
                self.currentKey = ''
                self.changeState(1)
        elif curretState == 3:
            if tag == 'td': # The metadata isn't added till we import both the TH, and the TD fields
                tempKey = self.currentKey
                tempValue = self.currentValue
                if tempKey != '': # We can't add a key with no name!!! 
                    product.addMetadata(tempKey, tempValue)
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
                if self.index > 1: # If there are more than one links, add a number to the end of the string
                    linkKey += ' ' + str(self.index)
                print 'self.currentValue = ', self.currentValue, ', self.index = ', self.index, ', linkKey = ', linkKey
                product.addMetadata(linkKey, self.currentValue)
                product.addMetadata(linkKey + ' URL', self.currentURL)
                if self.currentKey == '3D Model':
                    self.product3DModels += self.currentURL
                self.changeState(3)
        elif curretState == 5:
            if tag == 'td':
                self.dataBuffer += self.currentValue + ', '
                #print '$$$ self.dataBuffer = ', self.dataBuffer
                if self.counter == 7:
                    print '@@@ Reached end of TR'
                    product.addMetadata(self.currentKey, self.dataBuffer)
                    self.dataBuffer = '' # Reset the dataBuffer
                    #self.currentValue = ''
                    if self.currentURL != '':
                        newFiledTitle = self.currentKey + ' URL'
                        product.addMetadata(newFiledTitle, self.currentURL)
                        
                        if currentKey == '3D Model':
                            self.product3DModels += self.currentURL
                            
                elif self.counter == 4: # Then this is the packing option text
                    self.currentKey = 'Alternate Package: ' + self.currentValue
                    print 'Found Packing Title: ', self.currentKey
            elif tag == 'a': # Done parsing link
                self.recordURL(self.currentURL)
                self.index -= 1
            elif tag == 'table':
                self.changeState(0); # go back to the do nothing state.
    
    def handleData(self, data):
        product = self.product
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
                self.dataBuffer += data
                self.dataBuffer += '='
            elif counterValue == 2: # Add the dataBuffer with the data
                print 'Found quanitiy price: ', data
                self.dataBuffer += data
                self.dataBuffer += ', '
        elif currentState == 4: # Then store the URL link name
            self.currentValue += data
        elif currentState == 5: # Parsing alternative packaging options.
            self.currentValue += data

    class UnitTest():
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
                DigiKeySourcerer.testFromURL (url)
        
            print '\nDone running testFromURLList().\n'
            
        @staticmethod
        def testFromFile():
            print "Testing import from file...\n"
            
            sourcerer = DigiKeySourcerer('')
            #sourcerer.loadFromFile('0D', '.', 'DigiKeyTestFiles/DigiKeyPriceTable.html', 'http://www.digikey.com/test/')
            #sourcerer.loadFromFile('0D', '.', 'DigiKeyTestFiles/DigiKeyProductInfoTable.html', 'http://www.digikey.com/test/')
            #sourcerer.loadFromFile('0D', '.', 'DigiKeyTestFiles/DigiKeyAdditionalInfoTable.html', 'http://www.digikey.com/test/')
            #sourcerer.loadFromFile('0D', '.', 'DigiKeyTestFiles/DigiKeyMetadataTest.html', 'http://www.digikey.com/test/')
            sourcerer.loadFromFile('0D', '.', 'DigiKeyTestFiles/DigiKeyTest.html', 'http://www.digikey.com/test/')
            
            print '\n**********************************************************'
            print 'Printing imported SupplierComponent...\n'
            
            print 'Finished running testingFromFile()\n'
            print sourcerer.product.toString()
        
        @staticmethod
        def testFromURL(url):
            print '\nRunning testFromURL("', url, '")...\n'
            
            #Sourcerer.saveDataToFile(DigiKeySourcerer.loadContentFromURL(url), 'DigiKeyTestFiles/DigiKeyOnlineTest.html')
            
            sourcerer = DigiKeySourcerer('/')
            sourcerer.loadFromURL('0D', '.', url)
            print sourcerer.product.toString()
            
            
            
        
            print '\nFinished running testFromURL.\n'
        
        # @brief    function that runs diagonistics on the DigiKeySourcerer class
        @staticmethod
        def runUnitTest():
            os.system('cls')
            print 'Running DigiKeySourcerer diagnostics...\n'
            
            #DigiKeySourcerer.UnitTest.testFromFile()
            DigiKeySourcerer.UnitTest.testFromURL('http://www.digikey.com/product-detail/en/0879180001/WM2066-ND/1643335')
            #DigiKeySourcerer.UnitTest.testFromURLList ()
            
            print '\nFinished running DigiKeySourcerer diagnostics.\n'

DigiKeySourcerer.UnitTest.runUnitTest()