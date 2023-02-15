
import boto3

class dynamo:
    def __init__(self):
        print("dynamo")
        self.table = boto3.resource('dynamodb', region_name='us-east-1').Table('option-price')

    def record(self, newitem):
        print("--------------record------------------")
        response = self.table.get_item(Key={'id': newitem.get('id')})

        if response.get("Item"): 
            print("upate item")
            item = response.get("Item")
            item["premium"] +=  ", " + newitem["premium"]
            item["date"] +=  ", " + newitem["date"]
            item["price"] +=  ", " + newitem["price"]
        else:
            print("create a new item")
            item = newitem
        
        self.table.put_item(Item= item)

if __name__ == '__main__':
    newItem = { 'expirationDate': '2023-02-16',
                'date': '2023-02-15 11:28:05',
                'note': '',
                'optionType': 'put',
                'premium': '2',
                'symbol': 'spy',
                'price': '411.78',
                'id': 'SPY20230216P41999'
                }
    dynamo().record(newItem)