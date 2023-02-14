import boto3

class dynamo:

    def insert(self):

        boto3.setup_default_session(profile_name="taixingbi")

        dynamo_client  =  boto3.client(
              service_name = 'dynamodb',
              region_name = 'us-east-1',
              aws_access_key_id = '',
              aws_secret_access_key = ''
              )

        table_name = "option-test"
        # response = dynamo_client.put_item(
        #     TableName=table_name,
        #     Item={
        #         "order_id": {"S": "ord1234"},
        #         "order_date": {"S": "2022-08-03"},
        #         "user_email": {"S": "test@example.com"},
        #         "amount": {"N": "120"},
        #     },
        # )
        # print(response)

if __name__ == '__main__':
    print("dynamo")
    dynamo().insert()
    print("done")