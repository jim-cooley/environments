import boto3

s3 = boto3.resource('s3')

# print out bucket names
for bucket in s3.buckets.all():
  print(bucket.name)

# upload a new file
data = open('test.jpg', 'rb')
s3.Bucket('my-bucket').put_object(Key='test.jpg', Body=data)
