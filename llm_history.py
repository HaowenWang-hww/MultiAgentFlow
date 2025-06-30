import unicodedata
import requests
import csv

# tokens = ['app-RQsf8l0e3fjsOllal6llT0Uq','app-VAR3t5TiJNVA0gscmK9Gj5PX','app-iExOY32vF6pInMynk48cYmIN']
tokens = ['app-RQsf8l0e3fjsOllal6llT0Uq']
endpoint = 'http://10.30.10.105:8502'
csv_file = '/Users/jnchou/Downloads/llm_dump'

params = {
    'user': 'abc-123',
    'limit': 100,
    'last_id': None
}

c_params = {
    'user': 'abc-123',
    'conversation_id': None
}

for token in tokens:
    headers = {"Authorization": "Bearer " + token}
    output = []
    conversations = []
    has_more = True
    r_params = params
    while has_more is True:
        response = requests.get(endpoint+'/v1/conversations',params=r_params,headers=headers).json()
        #print(response)
        try:
            r_params['last_id'] = response['data'][-1]['id']
        except Exception:
            print(response)
        print(r_params['last_id'])
        try:
            conversations += (response['data'])
            if response['has_more'] is False:
                has_more = False
        except Exception:
            has_more = False
    print('writing')
    with open(csv_file+token+'.csv', 'w+', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for conversation in conversations:
            b_params = c_params
            # print(conversation)
            b_params['conversation_id'] = conversation['id']
            print(b_params['conversation_id'])
            response = requests.get(endpoint+'/v1/messages',params=b_params,headers=headers).json()['data'][0]
            # print(response)
            writer.writerow([response['conversation_id'],
                             unicodedata.normalize('NFC',response['query']),
                             unicodedata.normalize('NFC',response['answer']),
                             response['created_at']])
        
    
