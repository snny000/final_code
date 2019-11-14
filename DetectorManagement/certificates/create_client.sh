#!/bin/sh


# 为用户创建一个 key
openssl genrsa -des3 -out ./users/client.key 2048

# 为 key 创建一个证书签名请求 csr 文件
openssl req -new -key ./users/client.key -out ./users/client.csr -extensions v3_req -config "./conf/openssl.conf"

# 使用我们私有的 CA key 为刚才的 key 签名
openssl ca -extensions v3_req -in ./users/client.csr -cert ./private/ca.crt -keyfile ./private/ca.key -out ./users/client.crt -config "./conf/openssl.conf"

# 将证书转换为大多数浏览器都能识别的 PKCS12 文件
openssl pkcs12 -export -clcerts -in ./users/client.crt -inkey ./users/client.key -out ./users/client.p12
