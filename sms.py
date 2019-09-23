import requests


def sendOTP(tel,otp):
    url = "http://203.146.186.186/molink_otp_service/sms.asmx/OTPSend"

    msg = "OTP Code = " + otp
    payload = "{\n\t\"username\":\"tong9977\",\n\t\"password\":\"Sinetong9977\",\n\t\"txtSMS\":\""+ msg +" [Ref SkyRunningLocker-A0023-${code}]\",\n\t\"sender\":\"OTPPasscode\",\n\t\"txtMobile\":\""+tel+"\"\n}"
    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'Postman-Token': "5f20aea0-d1fc-47aa-acb4-faae5fc3ca72"
        }

    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)