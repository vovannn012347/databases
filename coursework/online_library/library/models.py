from __future__ import unicode_literals

from django.conf import settings
from bson.objectid import ObjectId
from pymongo import MongoClient
from django.db import models
import os

db_conf = settings.MONGODB_SETTINGS
Mongo_db = MongoClient(**db_conf['connection'])[db_conf['db']]

# Create your models here.
class Library:
    files_url = 'coursework\\online_library\\library\\books\\files\\'
    images_url = 'coursework\\online_library\\library\\books\\images\\'

    @staticmethod
    def find(offset=0, limit=10):
        books = Mongo_db.books.find(skip=offset, limit=limit)
        return books

    @staticmethod
    def get_book(book_id):
        return Mongo_db.books.find_one(ObjectId(book_id))

    @staticmethod
    def Insert_Book(request, form):

        result = Mongo_db.books.insert_one({
            'name' : form.cleaned_data['name'],
            'author' : form.cleaned_data['author'],
            'description' : form.cleaned_data['description'],
            'rate' : form.cleaned_data['rate'],
            'rates' :{
                request.user.username : form.cleaned_data['rate']
            },
            'image' : request.FILES['image'].name,
            'image_type' : request.FILES['image'].content_type,
            'content' : request.FILES['bookFile'].name,
            'content_type' :  request.FILES['bookFile'].content_type,
            'created_by':{
                'name':  request.user.username
            }
        })
        return result.inserted_id

    @staticmethod
    def edit_Book(request, data, book_id):
        book = Mongo_db.books.find_one(ObjectId(book_id))

        if request.FILES.get('image', False):
            Library.handleUploadedImages(request.FILES['image'])
            book['image'] = request.FILES['image'].name
            book['image_type'] = request.FILES['image'].content_type


        if request.FILES.get('bookFile', False):
            Library.handleUploadedFiles(request.FILES['bookFile'])
            book['content']= request.FILES['bookFile'].name
            book['content_type']= request.FILES['bookFile'].content_type

        book['name']= data['name']
        book['author']= data['author']
        book['description']= data['description']
        book['rates'][book['created_by']['name']] = data['rate']

        Mongo_db.books.update_one({'_id':ObjectId(book_id)}, { '$set' : book} )

    @staticmethod
    def handleUploadedFiles(filedata):
        with open( Library.files_url + filedata.name, 'wb+') as destination:
            for chunk in filedata.chunks():
                destination.write(chunk)

    @staticmethod
    def handleUploadedImages(filedata):
        with open(Library.images_url + filedata.name, 'wb+') as destination:
            for chunk in filedata.chunks():
                destination.write(chunk)

    @staticmethod
    def addBookmark(user_name, book_id, book_page):
        return False

    @staticmethod
    def getBookmarks(user_name):
        return Mongo_db.bookmarks.find({'user'})
