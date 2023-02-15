import boto3

class dynamo:
    def __init__(self):
        print("dynamo")
        
    def insert(self):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table("option-test")
        table.put_item(Item= {'fruitName': 'Banana'})

if __name__ == '__main__':
    print("dynamo")
    dynamo().insert()
    print("done")