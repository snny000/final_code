#!/bin/sh

# 生成私钥 key 文件
openssl genrsa -out private/ca.key 2048

# 生成证书请求 csr 文件
openssl req -new -key private/ca.key -out private/ca.csr -extensions v3_req -config "./conf/openssl.conf"

# 生成凭证 crt 文件
openssl x509 -req -days 3650 -in private/ca.csr -signkey private/ca.key -out private/ca.crt

# 为我们的 key 设置起始序列号和创建 CA 键库
echo '01' > serial   # 可以是任意四个字符
touch index.txt

# 为 "用户证书" 的移除创建一个证书撤销列表
openssl ca -gencrl -out ./private/ca.crl -crldays 7 -config "./conf/openssl.conf"
