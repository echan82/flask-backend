#!/usr/bin/python
from flask import request, json
from flask_restful import Resource,reqparse
from exception.checked_exception import CheckedException
from exception.runtime_exception import RuntimeException
from model.model_sample import Movies
from boto3.dynamodb.conditions import Key, Attr
from util.decimal_encoder import DecimalEncoder
import boto3
import json
import logging


class MoviesByYear(Resource):  
    def __init__(self, logger=None):
        self.logger = logging.getLogger(__name__)
   
    def get(self):
            #validate_year()
            year=validate_year(self)
            
            self.logger.debug('year: %s',year) 

            #get_movies_by_year()
            response=get_movies_by_year(self,year)
            
            #json.dumps()
            json_dump_result=json.dumps(response['Items'],cls=DecimalEncoder)
            
            #marshmallow.loads()
            movies=Movies()
            movies=movies.loads(json_dump_result,many=True)
            
            response_data=movies.data
            self.logger.debug(response_data)       
            
            return response_data

def validate_year(self):
    parser=reqparse.RequestParser()
    parser.add_argument('year',type=int)

    try:
    
        args=parser.parse_args(strict=True)
    
    except Exception as ex:
        self.logger.error(ex, exc_info=True)
        raise CheckedException('Invalid args',400,999)
    
    else:
        year=args['year']
        if year is None:
            raise CheckedException('You need to add the year',400,999)
    
    return year

def get_movies_by_year(self,year):
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('Movies')
        response = table.query(
            ProjectionExpression="#yr, title, info.genres, info.actors[0]",
            ExpressionAttributeNames={ "#yr": "year" }, # Expression Attribute Names for Projection Expression only.
            KeyConditionExpression=Key('year').eq(year) & Key('title').between('A', 'L'),
         )
        
        '''

        A single Query will only return a result set that fits within the 1 MB size limit. To determine whether there are more results, and to retrieve them one page at a time, applications should do the following:

        1.Examine the low-level Query result:
            If the result contains a LastEvaluatedKey element, proceed to step 2.
            If there is not a LastEvaluatedKey in the result, then there are no more items to be retrieved.
        2.Construct a new Query request, with the same parameters as the previous one—but this time, take the LastEvaluatedKey value from step 1 and use it as the ExclusiveStartKey parameter in the new Query request.
            Run the new Query request.
            Go to step 1.
        '''
        # If you have the 'LastEvaluatedKey' in your 'response' , You have to read this -> 'https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Query.html'
        
        response_count=response['Count']

        if response_count is 0:
            raise CheckedException('Not found',404,404)

    except CheckedException as ex:
        raise ex
        
    except Exception as ex:
        self.logger.error(ex, exc_info=True)
        raise RuntimeException('Runtime Exception',500,999)
             
    return response    
    
              
        
