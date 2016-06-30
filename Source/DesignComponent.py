# @project      Part-Sourcerer
# @copyright    Blue Storm Engineering, LLC. All rights reserved.
# @lincense     This project is released under the GNU Public License 3.0 (http://www.gnu.org/licenses/gpl-3.0.html).
# @author       Cale McCollough
# @date         01/15/2015
# @brief        This file contains the DesignComponent class for Part-Sourcerer
# @description  
#
# Metadata Fields
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Metadata fileds in Part-Sourcerer are stored in a dictionary of 3 strings.
# ['Field Name'], ['Field Value'], ['Fieled URL']
# If a metadata field does not have a link, the Field URL is left blank.
# Sometimes, a product might havr multiple datasheets, packaging, or lifecycle documents. When this happens, the fileds are added
#
# @object   DesignComponent
# @brief    
# @desc     An DesignComponent (Electronics Design Automation Component) contains all of the design information for a 
# component used in DipTrace. An DesignComponent might have multiple suppliers, with multiple different Product numbers for 
# different packing options. The DesignComponent contains a list of SuplierComponent objects.
#
# The main info we need to properly sort components is the manufacturer name, and the name of the product. This method is similar 
# to the way that Apple's iTunes sorts music by artist name and album.
#
# Shared Metadata fields
# -----------------------------------------------------------------------------------------------------------------------------
# In order to minimize the number of metadata fields, Part-Sourcerer minimizes the number of fields by only displaying fields that are 
# different. For example say the reel of resistors you need ran out, and you need an identical substitute. All of the metadata 
# is identical but the part number, manufacturer, quantity in stock, etc.

import os

from Sourcerer import Sourcerer

class DesignComponent():
    ''' Static Variables '''
    # A list of common EDA, CAD, CAM, and documenation file types to download.
    designFileTypes = { '.stp', '.step', '.iges', '.zip' }
    # A list of common document file formats
    documentTypes = { '.pdf', '.xls', '.xlsx', '.docx', '.doc' }
    
    ''' Instance Variables '''
    # The name of this component/product.
    name = ''
    # The component/product manufacturer.
    manufacturer = ''
    # URL to datasheet to download to project datasheet directory.
    datasheetURL = ''
    # A dictionary of metadata values.
    metadata = []
    # A list of SupplierComponet sources.
    sources = []
    # The URL to the directory this DesignComponent is located in.
    directory = ''
    # A list of documenation filenames cached files, such as .pdf, xlsx, and .docx files.
    documentFiles = []
    # A list of uncompressed CAD and CAM files stored locally, sucvh as .step and .dxf files.
    designFiles = []
    
    def __init__(self, manufacturer, name, projectDirecotry):
        self.setManufacturer(manufacturer)
        self.setName(name)
        self.setDirectory(projectDirecotry)
    
    def setManufacturer(self, manufacturer):
        properName = Sourcerer.fixFilename(manufacturer)
        if properName == '': # The name was not valid.
            return
        self.manufacturer = manufacturer
    
    def setName(self, name):
        properName = Sourcerer.fixFilename(name)
        if properName == '': # The name was not valid.
            return
        self.name = name
    
    def setDirectory(self, projectDirecotry):
        if not os.path.exists(projectDirecotry): # The project directory must already exist
            return False
        
        self.directory = self.directory + self.manufacturer + self.name
        return True
    
    @staticmethod
    def directoryPath(projectDirecotry, manufacturer, name):
        if manufacturer == '' or name == '' or os.path.exists(projectDirecotry):
            return
        direcotryPath = projectDirecotry + manufacturer + name
        return direcotryPath
    
    def addMetadata(self, key, value):
        key = key.strip()
        if key == '': # We can't add a entry with no key.
            return
        
        if key.endswith(' URL'):
            value = Sourcerer.fixShortURL(value)
        
        #print 'Adding metadata: ', key, ', ', value
        print 'Adding metadata entry: [" ', key, ' "], [" ', value, ' "]'
        
        if len(self.metadata) == 0: # We have to create a dictionary
            self.metadata = { key: value }
            return

        self.metadata[key] = value
        
    def removeKey(self, key):
        del self.metadata[key]
    
    # @brief    Function that adds a a SupplierComponet to this DesignComponent.
    # @desc     
    def addSupply(self, newComponent):
        sources += newComponent
    
    # @brief    Function that attaches a SupplierComponet to this DesignComponent.
    # @desc     
    def removeComponent(self, oldComponent):
        pass
        #for key, value in self.source:
        #    if self.name == oldComponent.name and self.manufacturer == oldComponent.manufacturer:
        #        del source[i]
        #    i = i + 1

    # Downloads all of the design files and documents to this component's sorted directory.
    def downloadDesignFiles(self):
        directory = self.directory
        Sourcerer.checkPathOrCreate(direcotry)
        Sourcerer.downloadFile(self.datasheetURL, directory)
        
        metadata = self.metadata
        for key in metadata:
            if key.endswith(' URL'):
                self.downloadDesignFile(metadata[key])
                self.downloadDocument(metadata[key])
        
        for source in self.sources:
            for key, value in source.metadata:
                if ' URL' in key:
                    self.downloadDesignFile(value)
                    self.downloadDocument(value)
    
    def downloadDesignFile(self, url):
        if not DesignComponent.isDesignDocument(url):
            return
        Sourcerer.downloadFile(url, DesignComponent.designFileTypes)
    
    def downloadDocument(self, url):
        if not DesignComponent.isDesignFile(url):
            return
            DesignComponent.downloadDesignFile(source.metadata, DesignComponent.documentTypes)
    
    def toString(self):
        returnString = 'DesignComponent:'
        
        nameString = 'Name: ' + self.name
        manufacturerString =  '\nManufacturer: ' + self.manufacturer
        datasteetString =  '\nDatasheet URL: ' + self.datasheetURL
        directoryString = '\nDirectory: ' + self.directory
        
        if len(self.metadata) == 0:
            metadataString = '\nMetadata: None\n'
        else:
            metadataString = '\nMetadata: \n'
            for key, value in self.metadata.iteritems():
                metadataString += '[" '+ key + ' "], [" '+ value + ' "]\n'
        
        
        if len(self.sources) == 0:
            sourceString = 'Sources: None\n'
        else:
            sourceString = 'Sources: \n'
            i = 1
            for source in self.source:
                returnString += '\nSource ' + i + ': '
                i = i + 1
        
        returnString = (nameString + manufacturerString + datasteetString + directoryString + metadataString + sourceString)
        return returnString
    
    @staticmethod
    def isDesignFile(url):
        filetype = Sourcerer.getFiletype(url)
        if filetype == '':
            return
        if filetype in DesignComponent.designFileTypes:
            return True
        return False
    
    @staticmethod
    def isDesignDocument(url):
        filetype = Sourcerer.getFiletype(url)
        if filetype == '':
            return
        if filetype in DesignComponent.documentTypes:
            return True
        return False
    
    class UnitTest():
        @staticmethod
        def generateTestComponent(manufacturer, name, directory):
            print 'Generating test DesignComponent...("', name, ', ', manufacturer, ', ', directory, ')\n'
            
            component = DesignComponent(manufacturer, name, directory)
            component.datasheetURL = Sourcerer.fixShortURL('www.genericmanufacturer.com/test/1/2/3/datasheet.pdf')
            
            component.addMetadata('3D Model URL', 'http://www.molex.com/pdm_docs/stp/87918-0001_stp.zip')
            component.addMetadata('Datasheet 1 URL', 'http://www.molex.com/pdm_docs/sd/879180001_sd.pdf')
            component.addMetadata('3D Model 2 URL', 'http://www.te.com/commerce/DocumentDelivery/DDEController?Action=srchrtrv&DocNm=640454-4&DocType=Customer+View+Model&DocLang=English')
            component.addMetadata('Datasheets 2 URL', 'http://www.te.com/commerce/DocumentDelivery/DDEController?Action=srchrtrv&DocNm=640454&DocType=Customer+Drawing&DocLang=English')
            component.addMetadata('Online Catalog URL', 'http://www.digikey.com/catalog/en/partgroup/mta-100-series/9332?mpart=640454-4&vendor=17&WT.z_ref_page_type=PS&WT.z_ref_page_sub_type=PD&WT.z_ref_page_id=PD&WT.z_ref_page_event=DC_Link_Table')
            component.addMetadata('Product Photos URL', 'http://media.digikey.com/photos/Tyco%20Amp%20Photos/640456-4,%20640454-4.jpg')
            component.addMetadata('Featured Product URL', 'http://www.digikey.com/product-highlights/us/en/te-connectivity-mta-connectors/2307')
            component.addMetadata('Series URL', 'http://www.digikey.com/product-search/en?FV=ffec1142')
            
            return component
            
        @staticmethod
        def testGenerateDesignComponent():
            
            print '\nRunning testGenerateDesignComponent diagnostics...'
            Sourcerer.printLine('-')
            
            testDirectoryName = 'D:\Workspace\eda-sourcerer\source\Test' # already existing folder on D: drive
            
            component = DesignComponent.UnitTest.generateTestComponent('TestComponent', 'Generic', testDirectoryName)
            
            Sourcerer.printLine('-')
            print '\n', component.toString()
            Sourcerer.printLine('-')
            
            badFolderName = 'B:\ad\direcotry' # Folder that does not exist
            component = DesignComponent.UnitTest.generateTestComponent('TestComponent', 'Generic', badFolderName)
            
            Sourcerer.printLine('-')
            print '\n', component.toString()
            Sourcerer.printLine('-')
            
            component.downloadDesignFiles()
            
            Sourcerer.printLine('-')
            print 'Finished running testGenerateDesignComponent diagnostics.\n'
            
        @staticmethod
        def testDownloadDesignFiles():
            print '\nRunning DesignComponent diagnostics...'
            Sourcerer.printLine('-')

            testDirectoryName = 'D:\Workspace\eda-sourcerer\source\Test' # already existing folder on D: drive
            component = DesignComponent.UnitTest.generateTestComponent('TestComponent', 'Generic', testDirectoryName)
            print component.toString()
            
            Sourcerer.printLine('-');
            print '\nDownloading test files...'
            component.downloadDesignFiles()
            
            Sourcerer.printLine('-')
            print 'Finished running DesignComponent diagnostics.\n'
            
        
        @staticmethod
        def runUnitTest ():
            os.system('cls')
            print 'Running DesignComponent.UnitTest...\n'
            Sourcerer.printLine('-')

            DesignComponent.UnitTest.testDownloadDesignFiles()
            
            Sourcerer.printLine('-')
            print 'Finished running DesignComponent.UnitTest.'

DesignComponent.UnitTest.runUnitTest()