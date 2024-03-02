from django.http import JsonResponse
import boto3,uuid
from typing import Dict, List , Any
from botocore.exceptions import NoCredentialsError
from django.http import HttpResponse,Http404
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime

region = 'us-west-2'
aws_access_key_id = 'AKIAQFC4UVNMBVG3QHZEjhvjh'
aws_secret_access_key = 'lHRXhrf4q+Nb+cx0aaBz9W+JLdR2fAdjmo,knjkjkjnEKwUxS'
    
# Create a DynamoDB client 
dynamodb = boto3.resource('dynamodb', region_name=region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

# Specify your DynamoDB table name
table_name = 'themes'
table = dynamodb.Table(table_name)

# @app.get("/get-theme/")
# async def get_theme():
#     return get_data_from_table("themes")


def themeList(request):
    data =  get_data_from_table("themes")
    return JsonResponse(data)

def userList(request):
    data =  get_data_from_table("users")
    return JsonResponse(data)

@csrf_exempt 
def contactList(request):
    if request.method == 'POST':
        data = request.POST  # Access POST data
        data = json.loads(request.body.decode('utf-8'))
        print(data.get('name'))

        table_name = 'contacts'
        table = dynamodb.Table(table_name)
        id = str(uuid.uuid4())
        created_at = str(datetime.now())

        # Insert contacts into DynamoDB
        with table.batch_writer() as batch:
            batch.put_item(Item={
                'id': id,
                'name': data.get('name'),
                'email': data.get('email'),
                'domain': data.get('domain'),
                'mobile': data.get('mobile'),
                'subject': data.get('subject'),
                'massage': data.get('massage'),
                'created_at': created_at
            })
        data = findById("contacts",id)    
        return JsonResponse({"message": "Data saved successfully", "status": True, "data": data})

    data =  get_data_from_table("contacts")
    return JsonResponse(data)

@csrf_exempt 
def contactListId(request,id):
    idChecks = idCheck("contacts",id)
    if idChecks is None:
        return JsonResponse({"message": "Data not found", "status": False, "data": []})
    
    if request.method == 'GET':
        data = get_data_from_table_by_id("contacts",id)
        return JsonResponse(data)
    
    elif request.method == 'DELETE':
        data = delete_item_from_table("contacts", id)
        if data["status"]:
            return JsonResponse(data)   
    
    elif request.method == 'POST':
        data = request.POST  # Access POST data
        return JsonResponse({'message': 'This is a POST request.', 'data': dict(data)})

# @csrf_exempt 
# def createContact(request):
#     return 

# def themeList(request):
#     data =  get_data_from_table("themes")

#     return JsonResponse(data)



def get_data_from_table(table_name: str) -> Dict[str, any]:
    try:
        table = dynamodb.Table(table_name)
        response = table.scan()
        items = response.get('Items', [])
        return {"message": "Data retrieved successfully", "status": True, "data": items}
    except NoCredentialsError as e:
        return {"message": f"Credentials not available: {e}", "status": False, "data": []}
        
def get_data_from_table_by_id(table_name: str, user_id: str) -> Dict[str, Any]:
    try:
        table = dynamodb.Table(table_name)
        response = table.get_item(
            Key={
                'id': user_id
            }
        )
        item = response.get('Item')
        if item:
            return {"message": "Data retrieved successfully", "status": True, "data": item}
        else:
            return HttpResponse(status=404, detail="No data found with this id")
    except:
        return HttpResponse(status=500, detail=f"Credentials not available: {e}")

def delete_item_from_table(table_name: str, id: str) -> Dict[str, Any]:
    try:
        table = dynamodb.Table(table_name)
        response = table.get_item(
            Key={
                'id': id
            }
        )
        item = response.get('Item')
        if item:
            response = table.delete_item(
            Key={
                'id': id
            }
            )
            return {"message": "Data deleted successfully", "status": True, "data": item}
        else:
            raise HttpResponse(status=404, detail=f"Item with ID {id} not found in table {table_name}")    

    except NoCredentialsError as e:
        return {"message": f"Credentials not available: {e}", "status": False}


def idCheck(table_name: str, id: str):
    table = dynamodb.Table(table_name)
    response = table.get_item(
        Key={
            'id': id
        }
    )
    item = response.get('Item')
    if item:
        return item

def findById(table_name: str, id: str):
    table = dynamodb.Table(table_name)
    response = table.get_item(
        Key={
            'id': id
        }
    )
    item = response.get('Item')
    return item   