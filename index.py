import locker
import fingerscan
import dbservice
import sms
from flask import Flask,request
from flask import jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
@app.route('/')
def index():
    return 'elocker is running.'

@app.route('/open')
def open():    
    no = request.args.get('no')
    locker.openBox(int(no))
    return jsonify(no)

@app.route('/openall')
def openall():
    locker.openAll()
    return 'openall'

@app.route('/settime')
def settime():
    return 'settime'

@app.route('/fsearch')
def fsearch():
    templateNo = fingerscan.search()
    if templateNo >= 0 :
        lockerid = dbservice.searchLockerByFingerprintTemplate(templateNo)
        return jsonify(lockerid)
    else :
        return jsonify(-1)

#Edit 09/10/2018
@app.route('/fenroll')
def fenroll():
    templateNo = fingerscan.enroll()
    if templateNo >= 0 :
        lockerid = dbservice.reserveLockerByFingerprintTemplate(templateNo)
        return jsonify(lockerid)
    else :
        return jsonify(-1)

@app.route('/fdelete')
def fdelete():
    templateno = request.args.get('no')
    result = fingerscan.delete(int(templateno))
    return jsonify(result)

@app.route('/lockeravailable')
def lockeravailable():
    result = dbservice.countLockerAvailable()
    return jsonify(result)


@app.route('/openLockerId')
def openLockerId():
    lockerId = request.args.get('id')
    boxno = dbservice.getBoxNoByLockerID(int(lockerId))
    if boxno > 0 :
        locker.openBox(boxno)
        return jsonify(boxno)
    else :
        return jsonify(-1)

@app.route('/openAndReleaseLockerId')
def openAndReleaseLockerId():
    lockerId = request.args.get('id')
    boxno = dbservice.getBoxNoByLockerID(int(lockerId))
    if boxno > 0 :
        #1. open locker
        locker.openBox(boxno)
        
        #2. delete fingerprint template
        template = dbservice.getfingerprintTemplateByLockerID(int(lockerId))
        if template >= 0 :
            fingerscan.delete(template) 
            #3. update database
            dbservice.releaseLockerByLockerID(int(lockerId))       

        return jsonify(boxno)
    else :
        return jsonify(-1)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
    
    
    
    
    
    
#Add New 09/10/2018
@app.route('/checkTelephoneNumber')
def reserveLocker():
    telNo = request.args.get('telNo')
    status = dbservice.checkTelephoneNumber(telNo)
    #  1 Success
    # -1 Error
    return jsonify(status)

#Add New 09/10/2018
@app.route('/checkTelephoneNumberForReleaseLocker')
def checkTelephoneNumberForReleaseLocker():
    telNo = request.args.get('telNo')
    otp = dbservice.checkTelephoneNumberForReleaseLocker(telNo)
    #  not -1 Success
    # -1 Error
    return jsonify(otp)

#Edit 09/10/2018
@app.route('/fenroll2')
def fenroll2():
    telNo = request.args.get('telNo')
    templateNo = fingerscan.enroll()
    if templateNo >= 0 :
        lockerid = dbservice.reserveLockerByFingerprintTemplateAndTelNo(templateNo, telNo)
        return jsonify(lockerid)
    else :
        return jsonify(-1)

    
#Add New 09/10/2018
@app.route('/releaseLockerByOTP')
def releaseLockerByOTP(): 
    telNo = request.args.get('telNo')
    OTP = request.args.get('OTP')
    result = dbservice.releaseLockerByOTP(telNo, OTP)
    return jsonify(result)
