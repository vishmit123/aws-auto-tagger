
import json
import boto3
import sys
REGION="us-east-1"

def lambda_handler(event, context):
    #attach_tags(event['detail']['responseElements']['vpc']['vpcId'])
    #print(event['detail'])
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
    
    attach_tags(event['detail']['responseElements'][resource][resourceId], event['detail']['responseElements'], resource)
        
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from AutoTagger!!')
    }
    
def attach_tags(resource_id, responseElements, resource):
    existing_tags = []
    tags = []
    tags.append({"Key": "Adobe.ArchPath", "Value": "ACP-CS.service.asset-events"})
    tags.append({"Key": "Adobe.CostCenter", "Value": "101391"})
    tags.append({"Key": "Adobe.DataClassification", "Value": "Internal"})
    tags.append({"Key": "Adobe.Environment", "Value": "Stage"})
    tags.append({"Key": "Adobe.Owner", "Value": "Adobe Cloud Platform - asset-events"})
    tags.append({"Key": "Adobe.PCIData", "Value": "false"})
    tags.append({"Key": "Adobe.PciAccount", "Value": "false"})
    tags.append({"Key": "Adobe.SKMSServiceID", "Value": "test"})

    if 'tagSet' in responseElements[resource]:
        existing_tags = responseElements[resource]['tagSet']['items']
        existing_tags = {i['key']: i['value'] for i in existing_tags}
        if 'Name' in existing_tags and existing_tags['Name']!= "":
            tags.append({"Key": "Name", "Value": existing_tags['Name']})
        elif 'name' in existing_tags and existing_tags['name']!= "":
            tags.append({"Key": "name", "Value": existing_tags['name']})
        else:
            tags.append({"Key": "Name", "Value": resource_id})
    else:
        tags.append({"Key": "Name", "Value": resource_id})

    ec2 = boto3.client('ec2', region_name=REGION)
    ec2.create_tags(Resources=[resource_id], Tags=tags)
