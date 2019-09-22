from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import logging

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

secret_id = 'AKIDe9YjjTlINDrGOKqQbXEfroY4LM7gm4tV'      # 替换为用户的 secretId
secret_key = 'VlnbAVaR8anlW3LNDrHTQ8f171jDSUFl'      # 替换为用户的 secretKey
region = 'ap-beijing'     # 替换为用户的 Region
token = None                # 使用临时密钥需要传入 Token，默认为空，可不填
scheme = 'https'            # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
# 2. 获取客户端对象
client = CosS3Client(config)
def uploads(image):
    with open(image, 'rb') as fp:
        client.put_object(
            Bucket='cothingdetail-1259695184',
            Body=fp,
            Key=image.split("\\")[-1],
            StorageClass='STANDARD',
            EnableMD5=False
        )
    return 1