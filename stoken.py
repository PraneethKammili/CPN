from itsdangerous import URLSafeSerializer
salt='extra@123'
secret_key='Codegnan@2018'
def entoken(data):
    serializer=URLSafeSerializer(secret_key)
    return serializer.dumps(data,salt)
def dctoken(data):
    serializer=URLSafeSerializer(secret_key)
    return serializer.loads(data,salt)