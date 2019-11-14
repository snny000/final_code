#!/bin/sh

# 查看KEY信息
# openssl rsa -noout -text -in users/client.key
# 查看CSR信息
# openssl req -noout -text -in users/client.csr
# 查看证书信息
# openssl x509 -noout -text -in users/client.crt


########## CA证书 ##########

# 生成私钥 key 文件
openssl genrsa -out private/ca.key 2048

# 生成证书请求 csr 文件
openssl req -new -key private/ca.key -out private/ca.csr -extensions v3_req -config "./conf/openssl.conf"

# 生成凭证 crt 文件
openssl x509 -req -days 365 -extensions v3_req -in private/ca.csr -signkey private/ca.key -out private/ca.crt

# 为我们的 key 设置起始序列号和创建 CA 键库
echo FACE > serial   # 可以是任意四个字符
touch index.txt

# 为 "用户证书" 的移除创建一个证书撤销列表
openssl ca -gencrl -out ./private/ca.crl -crldays 7 -config "./conf/openssl.conf"

########## 服务器证书 ##########

# 创建一个 key
openssl genrsa -out server/server.key 2048

# 为我们的 key 创建一个证书签名请求 csr 文件
openssl req -new -key server/server.key -out server/server.csr -extensions v3_req -config "./conf/openssl.conf"

# 使用我们私有的 CA key 为刚才的 key 签名
openssl ca -extensions v3_req -in server/server.csr -cert private/ca.crt -keyfile private/ca.key -out server/server.crt -config "./conf/openssl.conf"

########## 客户端证书 ##########

# 为用户创建一个 key
openssl genrsa -des3 -out ./users/client.key 2048

# 为 key 创建一个证书签名请求 csr 文件
openssl req -new -key ./users/client.key -out ./users/client.csr -extensions v3_req -config "./conf/openssl.conf"

# 使用我们私有的 CA key 为刚才的 key 签名
openssl ca -extensions v3_req -in ./users/client.csr -cert ./private/ca.crt -keyfile ./private/ca.key -out ./users/client.crt -config "./conf/openssl.conf"

# 将证书转换为大多数浏览器都能识别的 PKCS12 文件
openssl pkcs12 -export -clcerts -in ./users/client.crt -inkey ./users/client.key -out ./users/client.p12
