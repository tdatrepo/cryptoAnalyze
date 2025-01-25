import requests
import json
# import time
# import urllib3
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def send_telegram_message(message: str):
    # 7109907833 AN, 7509824859 DAT
    group_id = ['7109907833', '7509824859']
    # chat_id = "7109907833"
    api_key = "7071499815:AAEcmpQ5pW7kMws_KDgb6DQ2tbnTQ4EbwAQ"
    headers = {'Content-Type': 'application/json',
                'Proxy-Authorization': 'Basic base64'}
    for i in group_id:

        data_dict = {'chat_id': i,
                        'text': message,
                        'parse_mode': 'HTML',
                        'disable_notification': True}
        data = json.dumps(data_dict)
        url = f'https://api.telegram.org/bot{api_key}/sendMessage'
        response = requests.post(url,
                                    data=data,
                                    headers=headers,
                                    # proxies=proxies,
                                    # verify=False
                                    )
        print(response)
    
# chat_id = "@Tdat99"



# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
if __name__ == "__main__":
    send_telegram_message("Hello world!!!")
# time.sleep(10)