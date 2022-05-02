import io
import os
import shutil

import boto3
from affinda import AffindaAPI, TokenCredential
from django.shortcuts import render
from rest_framework import serializers, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from doc.settings import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_STORAGE_BUCKET_NAME,
)
from app.serializers import AffindaSerializer

from .models import Affinda
from .serializers import *


class AffindaNER(APIView):

    def post(self, request):
        data = request.data
        token = "882cef4ed52c12069650b808d49bde924b5252c4"
        credential = TokenCredential(token=token)
        client = AffindaAPI(credential=credential)
        
        session = boto3.Session(
                                    aws_access_key_id=AWS_ACCESS_KEY_ID,
                                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                                )
        s3 = session.resource('s3')
        my_bucket = s3.Bucket(AWS_STORAGE_BUCKET_NAME)

        serializer = AffindaSerializer(
            data=data,
        )
        if serializer.is_valid():
            serializer.save()
            for object_summary in my_bucket.objects.filter(Prefix="media/"):
                file =object_summary.key
                # myfile = file.split("/")[-1]
                # print(myfile)

            for s3_object in my_bucket.objects.all():
                path, filename = os.path.split(s3_object.key)
                UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Uploads')
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                # os.mkdir(path)
                
                file_name= os.path.join(UPLOAD_FOLDER, filename)
                print(file_name)
                # print("*****************************************************************************************************")
                my_bucket.download_file(s3_object.key, str(file_name))
                
                to_file = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                print(to_file)
                
                
            with open(str(file_name), 'rb') as f:
                resume = client.create_resume(file=f)
                data = resume.as_dict()
            shutil.rmtree(os.path.dirname(os.path.abspath(str(file_name))))
            return Response(
                {
                    "data": data,
                    "code": status.HTTP_200_OK,
                   "message": "Media created successfully",
                }
            )
        else:
            return Response(
                {
                    "data": serializer.errors,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "serializer errors",
                }
            ) 
