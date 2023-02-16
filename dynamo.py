
import boto3
from boto3.dynamodb.conditions import Key, Attr

class dynamo:
    def __init__(self):
        print("dynamo")
        self.table = boto3.resource('dynamodb', region_name='us-east-1').Table('option-price')

    def query(self, date):
        print("--------------query------------------")
        response = self.table.scan(FilterExpression=Attr('active').eq('True'))
        items = response['Items']
        itemsActive = []
        for item in items:
            print(date)
            if date > item['expirationDate']:
                print(item['expirationDate'], "is expired")
                item['active'] = "False"
                self.put(item)
                return None
            else:
                print(item['expirationDate'],  "not expired")
                itemsActive.append(item)
        return itemsActive

    def put(self, newitem):
        print("--------------put------------------")
        self.table.put_item(Item= newitem)

    def update(self, newitem):
        print("--------------update------------------")
        print(newitem)
        response = self.table.get_item(Key={
            'id': newitem.get('id'), 
            })
        print(response)
        if response.get("Item"): 
            print("update item")
            item = response.get("Item")
            item["premium"] +=  ", " + newitem["premium"]
            item["date"] +=  ", " + newitem["date"]
            item["price"] +=  ", " + newitem["price"]
        else:
            print("create a new item")
            item = newitem
        
        self.table.put_item(Item= item)

if __name__ == '__main__':
    # newItem = { 'expirationDate': '2023-02-16',
    #             'date': '2023-02-15 11:28:05',
    #             'note': '',
    #             'optionType': 'put',
    #             'premium': '2',
    #             'symbol': 'spy',
    #             'strike': '413',
    #             'id': 'SPY20230216C413'
    #             }
    # dynamo().record(newItem)
    dynamo().query()