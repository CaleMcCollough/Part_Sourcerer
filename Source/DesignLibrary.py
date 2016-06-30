# @project      Part-Sourcerer
# @copyright    Blue Storm Engineering, LLC. All rights reserved.
# @lincense     This project is released under the GNU Public License 3.0 (http://www.gnu.org/licenses/gpl-3.0.html).
# @author       Cale McCollough
# @date         01/15/2015
# @brief        This file contains the DesignLibrary class for Part-Sourcerer
# @description  

class DesignLibrary():
        
    # The project directory.
    projectDirectory = '/'
    # The filename of this library.
    filename = 'Untitled.dlib'
    # The list of DesignComponent(s) in this library.
    components = []
    
    def __init__(self, projectDirectory)
        self.setDirecotryPath(projectDirectory)
        
    def setDirecotryPath(url)
        self.projectDirectory = Sourcerer.cleanDirecoryPath(url)

    def optmizeComponentCosts(self):
        print 'Optimizing ComponentLibrary '
    
    def import3DModelsIntoLibrary(self):
        print 'Importing 3D Models from the local ./[Manufacturer]/[PUID] sorted format.'
    
    # Function that downloads the design files for a component from the DesignComponent.metadata.
    def importDesignFiles(self):
        component = self.component
        component3DModelURLs = self.component3DModels
        if component.manufacturer == '' or self.puid == '' or component3DModels == []:
            return
        
        sortedFileDirectory = self.projectDirectory + component.manufacturer + '/' + component + '/'
        for modelURL in component3DModels:
            # First check if the file already exists.
            if not os.path.exists(sortedFileDirectory):
                os.makedirs(sortedFileDirectory)
                
            print 'Downloading 3D models to ', sortedFileDirectory
            # We need to 
            fileName = sortedFileDirectory + parseurl(modelURL).netloc
            fileHandle = open('test.zip', 'rb')
            zipFile = zipfile.ZipFile(fileHandle)
            for name in zipFile.namelist():
                outpath = "C:\\"
                zipFile.extract(name, outpath)
            fileHandle.close()
        
    class UnitTest():
        @staticmethod
        def runUnitTest():
            print 'Running EDALibraryManager.UnitTest...'
            
            print 'Done runing EDALibraryManager.UnitTest'