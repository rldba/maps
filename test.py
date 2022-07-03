import os
from dadata import Dadata

token = os.environ.get('DADATA_TOKEN')
secret = os.environ.get('DADATA_SECRET')

with Dadata(token, secret) as dadata:
    result = dadata.clean("address", "Уфа театральная 3")
    print(result)
