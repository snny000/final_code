#!/bin/sh


# 创建一个 key
openssl genrsa -out server/server.key 2048

# 为我们的 key 创建一个证书签名请求 csr 文件
openssl req -new -key server/server.key -out server/server.csr -extensions v3_req -config "./conf/openssl.conf"

# 使用我们私有的 CA key 为刚才的 key 签名
openssl ca -extensions v3_req -in server/server.csr -cert private/ca.crt -keyfile private/ca.key -out server/server.crt -config "./conf/openssl.conf"
