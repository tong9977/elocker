import config
import time
from pyfingerprint.pyfingerprint import PyFingerprint

def enroll():
    print('start enroll')
    port = config.figerScanPort
    f = PyFingerprint(port, 57600, 0xFFFFFFFF, 0x00000000)

    ## Gets some sensor information
    print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

    ## Tries to enroll new finger
    try:
        print('Waiting for finger...')

        ## Wait that finger is read
        while ( f.readImage() == False ):
            pass
        ## Converts read image to characteristics and stores it in charbuffer 1
        f.convertImage(0x01)

        ## Checks if finger is already enrolled
        result = f.searchTemplate()
        positionNumber = result[0]

        if ( positionNumber >= 0 ):
            print('Template already exists at position #' + str(positionNumber))
            return -1

        f.createTemplate()

        ## Saves template at new position number
        positionNumber = f.storeTemplate()
        print('Finger enrolled successfully!')
        print('New template position #' + str(positionNumber))
        return positionNumber
    
    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        return -2

def search():
    port = config.figerScanPort
    f = PyFingerprint(port, 57600, 0xFFFFFFFF, 0x00000000)
    ## Tries to search the finger and calculate hash
    try:
        print('Waiting for finger...')

        ## Wait that finger is read
        while ( f.readImage() == False ):
            pass

        ## Converts read image to characteristics and stores it in charbuffer 1
        f.convertImage(0x01)

        ## Searchs template
        result = f.searchTemplate()

        positionNumber = result[0]
        accuracyScore = result[1]

        if ( positionNumber == -1 ):
            print('No match found!')
            return -1
        else:
            print('Found template at position #' + str(positionNumber))
            print('The accuracy score is: ' + str(accuracyScore))
            return positionNumber
            
    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        return -1

def delete(positionNumber):
    port = config.figerScanPort
    f = PyFingerprint(port, 57600, 0xFFFFFFFF, 0x00000000)
    try:
        if ( f.deleteTemplate(positionNumber) == True ):
            print('Template deleted!' + str(positionNumber))
            return 1
    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        return -1

    

    



