import boto3
import csv

def lambda_handler(event, context):
    region='us-west-2'
    try: 
        # get a handle on s3
        session = boto3.Session(region_name=region)
        s3 = session.resource('s3')
        dyndb = boto3.client('dynamodb', region_name=region)
        bucket = s3.Bucket('capstone191') 
        obj = bucket.Object(key='MoviesOnStreamingPlatforms_updated.csv') 
        # get the object
        response = obj.get()
        # read the contents of the file
        lines = response['Body'].read().decode('utf-8').splitlines()
 
        firstrecord=True
        csv_reader = csv.reader(lines)
        for row in csv_reader:
            if (firstrecord):
                firstrecord=False
                continue
            MovieID = row[1]
            Title = row[2]
            Year = row[3]
            Age = row[4]
            IMDb = row[5]
            Netflix = row[7]
            Hulu = row[8]
            Prime = row[9]
            response = dyndb.put_item(
                TableName='MovieSpread',
                Item={
                # 'S' for type String, 'N' for Number.
                'MovieID' : {'N':str(MovieID)},
                'Title': {'S':str(Title)},
                'Year': {'N':str(Year)},
                'Age': {'S':str(Age)},
                'IMDb': {'N':str(IMDb)},
                'Netflix': {'N':str(Netflix)},
                'Hulu': {'N':str(Hulu)},
                'Prime': {'N':str(Prime)},
                }
            )
        result = 'Put succeeded:'
    except Exception as err:
        result = format(err)
        
    return {
        'body': result
    }
