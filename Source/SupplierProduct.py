# @project      Metascrapper
# @copyright    Cale McCollough. All rights reserved.
# @lincense     This project is released under the GNU Public License 3.0 (http://www.gnu.org/licenses/gpl-3.0.html).
# @author       Cale McCollough
# @date         01/15/2015
# @brief        This file contains the SupplierProduct class for Metascrapper
# @description  A SupplierProduct is a type of DesignComponent that adds some functionality, such as pricing and sourcing information.
# component used in DipTrace.
# 
# Metadata Fields
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# The self.metadata fields contain all of the info we are looking for
# 
# Supplier Codes
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Reserved Supplier Codes:
# A = Allied
# a = Arrow
# D = Digi-Key
# F = Farnell
# M = Mouser
# N = Newark
# R = RS-Components
# T = TME

import os
import urllib2
import webbrowser
import urlparse

import DesignComponent
import ComponentSupplier

# @class    SupplierProduct
# @brief    Class that represents a component on an electronics parts supplier's or other store's website.
# @desc     
class SupplierProduct():
    # The name of the supplier
    supplier = ''
    # The instance supply code of this product.
    supplyCode = ''
    # The delineator that separates the supplyCode from the 
    delineator = ''
    # The combined supplyCode + delineator string to speed up stuff a bit.
    supplierString = ''
    # The manufacturer of this product
    manufacturer = ''
    # The Product Unique ID (AKA part "number" (That isn't a number)) of this component.
    puid = ''
    # The URL of the product on the supplier's website
    url = ''
    # The http address of the supplier's website.
    supplierDomain = ''
    # The quantfity in availability string.
    quantity = []
    # The description.
    description = ''
    # A string with the supplier pricing in a comma separated list.
    pricingString = ''
    # A string that contains that packing option for this SupplierProduct.
    packingOption = ''
    # The additional price of this product packaging option (i.e. Digi-Reel cost).
    packingCost = 0
    # A dictionary of metadata about the product.
    metadata = []
    # A list of URLs to product datasheets.

    def __init__(self, supplyCode, delineator, url):
        self.setSupplyCode (supplyCode, delineator)
        self.setURL(url)
    
    def setURL (self, url):
        self.supplierName = SupplierProduct.getSupplierNameFromURL(url)
        self.supplierDomain = urlparse(url).netloc
    
    def setSupplyCode (self, supplyCode, delineator):
        delineatorLength = len(delineator)
        if delineatorLength != 1: # we can only have a one char delineator.
            return
        if ComponentSupplier.codeIsValid(supplyCode) == False:
            return
        self.supplyCode = supplyCode
        self.delineator = delineator
        self.supplierString = supplyCode + delineator
    
    def addMetadata(self, key, value):
        #key = key.strip()   # strip the whitespace
        #if key == '':       # We can't add a entry with no key.
        #    return
        key = self.supplierString + key.strip()  
        print 'Adding metadata entry: [" ', key, ' "], [" ', value, ' "]'
        
        if len(self.metadata) == 0: # We have to create a dictionary
            self.metadata = { key: value }
            return
        if ' URL' in key and value.startswith('/'): # Then add the supplier web address to the link.
            value = Scrapper.fixShortURL(self.supplierDomain + value)
            print '###Found short URL: ', value
            print '###self.supplierDomain = ', self.supplierDomain
        
        self.metadata[key] = value
    
    #def getBOMCost(self, quanityRequired):
    # We need to scroll through the quanityPrice list to see which price bracket we are in, and do the math.
    #    #for i in quanityPrice:
    #    #    if
    #    return 0
    
    # @brief    Function that returns a String with the PUID, packing option, and quantity in stock.
    # @desc     Used to print out the alternate packing options for an DesignComponent.
    def getPackingString(self):
        returnString = 'Source: [PUID: ' + self.puid + ', Packing: '
        if supplyCode == 'D':
            packingString += self.metadata['Packing']
        returnString += ']'
    
    # Extract supplier name from a url
    @staticmethod
    def getSupplierNameFromURL(url):
        uRLNetLocation = urlparse(url).netloc
        #print 'Extracting Supplier Name from url: ', url, ', uRLNetLocation = ', uRLNetLocation
        if uRLNetLocation == 'www.digikey.com':
            returnString = 'Digi-Key'
        elif uRLNetLocation == 'www.newark.com':
            returnString = 'Newark'
        elif uRLNetLocation == 'www.mouser.com':
            returnString = 'Mouser'
        else:
            returnString = ''
        #print 'SupplierName = ', returnString
        return returnString
    
    def toString(self):
        manufacturerString = 'Manufacturer: ' + self.manufacturer
        puidString = '\nProduct UID: ' + self.puid
        packingCostString = '\nPackaging Cost: ' + str(self.packingCost)
        #quantityAvailableString = '\nQuantity Availible: ' + self.quantityAvailable
        #descriptionString = '\nDescription: ' + self.description
        #pricingString = '\nPricing: ' + self.pricingString
        #packingOptionString = '\nPacking Option: ' + self.packingOption
        
        if len(self.metadata) == 0:
            metadataString = '\nSupply Metadata: None\n'
        else:
            metadataString = '\nSupply Metadata: \n'
            for key, value in self.metadata.iteritems():
                metadataString += '[" '+ key + ' "], [" '+ value + ' "]\n'
        
        returnString = manufacturerString + puidString + packingCostString + metadataString
        
        return returnString
    
    class UnitTest():
        # Function that runs the UnitTest for the SupplierProduct class.
        @staticmethod
        def runUnitTest():
            os.system('cls')
            print 'Running SupplierProduct diagnostics...\n'
            
            print 'Creating testProduct...\n'
            
            testProduct = SupplierProduct('0D', '.', 'http://www.digi-key.com/')
            
            testProduct.puid = 'P0.0GCT-ND'
            testProduct.quantityAvailable = 'Digi-Key Stock: 4,908,771 Can ship immediately'
            testProduct.description = 'RES SMD 0.0 OHM JUMPER 1/10W'
            testProduct.pricingString = '1=0.10000, 50=0.01260, 100=0.00960, 250=0.00716, 500=0.00528, 1000=0.00352, 2500=0.00297'
            testProduct.packingOption = 'Cut Tape (CT)'
            testProduct.packingCost = 0            #< The additional price of this product packaging option (i.e. Digi-Reel cost)
            testProduct.metadata = []      #< A dictionary of metadata about the product.
            
            testProduct.addMetadata('Supplier Key 1', 'Value 1')
            testProduct.addMetadata('Supplier Key 2', 'Value 2')
            testProduct.addMetadata('Supplier Key 3', 'Value 3')
            
            print 'Printing testProduct...\n', testProduct.toString()
            
            print '\nFinished running SupplierProduct diagnostics...'

SupplierProduct.UnitTest.runUnitTest()
