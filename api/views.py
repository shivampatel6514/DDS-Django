from django.http import JsonResponse
import boto3,uuid
from typing import Dict, List , Any
from botocore.exceptions import NoCredentialsError
from django.http import HttpResponse,Http404
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
from passlib.hash import bcrypt

region = 'us-west-2'
aws_access_key_id = 'AKIAQFC4UVNMBVG3QHZE---jhbhjbhvu'
aws_secret_access_key = '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----utyftufu'
    
# Create a DynamoDB client 
dynamodb = boto3.resource('dynamodb', region_name=region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

# Specify your DynamoDB table name
table_name = 'themes'
table = dynamodb.Table(table_name)

# @app.get("/get-theme/")
# async def get_theme():
#     return get_data_from_table("themes")

@csrf_exempt 
def themeList(request):
    if request.method == 'POST':
        data = request.POST  # Access POST data
        data = json.loads(request.body.decode('utf-8'))
        # print(data.get('name'))

        table_name = 'themes'
        table = dynamodb.Table(table_name)
        id = str(uuid.uuid4())
        created_at = str(datetime.now())
        # hashed_password = bcrypt.hash(data.get('password'))

        # Insert contacts into DynamoDB
        with table.batch_writer() as batch:
            batch.put_item(Item={
                'id': id,
                'name': data.get('name'),
                'demo': data.get('demo'),
                'keys': data.get('keys'),
                'client_keys': data.get('client_keys'),
                'created_at': created_at
            })
        data = findById("themes",id)    
        return JsonResponse({"message": "Data saved successfully", "status": True, "data": data})

    data =  get_data_from_table("themes")
    return JsonResponse(data)

@csrf_exempt
def themeListId(request,id):
    idChecks = idCheck("themes",id)
    if idChecks is None:
        return JsonResponse({"message": "Data not found", "status": False, "data": []})
    
    if request.method == 'GET':
        data = get_data_from_table_by_id("themes",id)
        return JsonResponse(data)
    
    elif request.method == 'DELETE':
        print("dele data")
        data = delete_item_from_table("themes", id)
        if data["status"]:
            return JsonResponse(data)   
    
    elif request.method == 'POST':
        data = request.POST  # Access POST data
        return JsonResponse({'message': 'This is a POST request.', 'data': dict(data)})



@csrf_exempt 
def userList(request):
    if request.method == 'POST':
        data = request.POST  # Access POST data
        data = json.loads(request.body.decode('utf-8'))
        print(data.get('name'))

        table_name = 'users'
        table = dynamodb.Table(table_name)
        id = str(uuid.uuid4())
        created_at = str(datetime.now())
        hashed_password = bcrypt.hash(data.get('password'))

        # Insert contacts into DynamoDB
        with table.batch_writer() as batch:
            batch.put_item(Item={
                'id': id,
                'name': data.get('name'),
                'email': data.get('email'),
                'password': hashed_password,
                'domain': data.get('domain'),
                'mobile': data.get('mobile'),
                'role_type': data.get('massage'),
                'created_at': created_at
            })
        data = findById("users",id)    
        return JsonResponse({"message": "Data saved successfully", "status": True, "data": data})

    data =  get_data_from_table("users")
    return JsonResponse(data)

@csrf_exempt 
def userListId(request,id):
    print(request.method)
    idChecks = idCheck("users",id)
    if idChecks is None:
        return JsonResponse({"message": "Data not found", "status": False, "data": []})
    
    if request.method == 'GET':
        data = get_data_from_table_by_id("users",id)
        return JsonResponse(data)
    
    elif request.method == 'DELETE':
        print("dele data")
        data = delete_item_from_table("users", id)
        if data["status"]:
            return JsonResponse(data)   
    
    elif request.method == 'POST':
        data = request.POST  # Access POST data
        return JsonResponse({'message': 'This is a POST request.', 'data': dict(data)})



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



# sitedataList,sitedataListId
@csrf_exempt 
def sitedataList(request):
    if request.method == 'POST':
        data = request.POST  # Access POST data
        data = json.loads(request.body.decode('utf-8'))
        print(data.get('name'))

        table_name = 'site_data'
        table = dynamodb.Table(table_name)
        id = str(uuid.uuid4())
        created_at = str(datetime.now())

        with table.batch_writer() as batch:
            batch.put_item(Item={
                'id': id,
                'name': data.get('name'),
                'description': data.get('description'),
                'domain': data.get('domain'),
                'client_keys': data.get('client_keys'),
                'keys': data.get('keys'),
                'theme_id': data.get('theme_id'),
                'user_id': data.get('user_id'),
                'created_at': created_at
            })
        data = findById("site_data",id)    
        return JsonResponse({"message": "Data saved successfully", "status": True, "data": data})

    data =  get_data_from_table("site_data")
    return JsonResponse(data)

@csrf_exempt 
def sitedataListId(request,id):
    idChecks = idCheck("site_data",id)
    if idChecks is None:
        return JsonResponse({"message": "Data not found", "status": False, "data": []})
    
    if request.method == 'GET':
        data = get_data_from_table_by_id("site_data",id)
        return JsonResponse(data)
    
    elif request.method == 'DELETE':
        data = delete_item_from_table("site_data", id)
        if data["status"]:
            return JsonResponse(data)   
    
    elif request.method == 'POST':
        data = request.POST  # Access POST data
        return JsonResponse({'message': 'This is a POST request.', 'data': dict(data)})




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