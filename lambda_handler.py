import json
import boto3
import sys
REGION="us-east-1"

def lambda_handler(event, context):
    #attach_tags(event['detail']['responseElements']['vpc']['vpcId'])
    print(event['detail'])
    eventName = event['detail']['eventName']
    resource = ""
    resourceId = ""
    if eventName.startswith('Create'):
        resource = event['detail']['eventName'][6:]
        resource = resource[0].lower() +resource[1:]
        resourceId = resource + "Id"
    else:
        return {
            'statusCode': 500,
            'body': json.dumps('Error in AutoTagger!!')
        }
    if eventName == "CreateVolume":
        attach_tags(event['detail']['responseElements'][resourceId], event['detail']['responseElements'])
    else:
        attach_tags(event['detail']['responseElements'][resource][resourceId], event['detail']['responseElements'][resource])
        
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from AutoTagger!!')
    }
    
def attach_tags(resource_id, responseElements):
    existing_tags = []
    tags = []
    tags.append({"Key": "Org", "Value": "Dev"})

    if 'tagSet' in responseElements:
        if 'items' in responseElements['tagSet']:
            existing_tags = responseElements['tagSet']['items']
            existing_tags = {i['key']: i['value'] for i in existing_tags}
            print(existing_tags)
            if 'Name' in existing_tags and existing_tags['Name']!= "":
                tags.append({"Key": "Name", "Value": existing_tags['Name']})
            elif 'name' in existing_tags and existing_tags['name']!= "":
                tags.append({"Key": "name", "Value": existing_tags['name']})
            else:
                tags.append({"Key": "Name", "Value": resource_id})
        else:
            tags.append({"Key": "Name", "Value": resource_id})
    else:
        tags.append({"Key": "Name", "Value": resource_id})

    ec2 = boto3.client('ec2', region_name=REGION)
    ec2.create_tags(Resources=[resource_id], Tags=tags)
