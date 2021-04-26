import json
import boto3
import sys
REGION="us-east-1"

def lambda_handler(event, context):
    bucketName = event['detail']['requestParameters']['bucketName']
    attach_tags(bucketName)
        
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from AutoTagger!!')
    }
    
def attach_tags(bucketName):
    s3 = boto3.client('s3')
    tags = []
    tags.append({"Key": "Org", "Value": "Dev"})

    try:
        existing = s3.get_bucket_tagging(Bucket=bucketName)
        existing_tags = {i['Key']: i['Value'] for i in existing['TagSet']}
        tags = {i['Key']: i['Value'] for i in tags}
        existing_tags.update(tags)
        if 'Name' in existing_tags and existing_tags['Name']!= "":
            existing_tags['Name'] = existing_tags['Name']
        elif 'name' in existing_tags and existing_tags['name']!= "":
            existing_tags['name'] = existing_tags['name']
        else:
            existing_tags["Name"] = bucketName
        response = s3.put_bucket_tagging(
            Bucket=bucketName,
            Tagging={
                'TagSet': [{'Key': str(k), 'Value': str(v)} for k, v in existing_tags.items()]
            }
        )
    except Exception as e:
        print("No Existing Tags Found")
        tags.append({"Key": "Name", "Value": bucketName})
        tags = {i['Key']: i['Value'] for i in tags}
        response = s3.put_bucket_tagging(
            Bucket=bucketName,
            Tagging={
                'TagSet': [{'Key': str(k), 'Value': str(v)} for k, v in tags.items()]
            }
        )
    
    
