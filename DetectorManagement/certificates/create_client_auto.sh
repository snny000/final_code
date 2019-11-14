#!/usr/local/tcl/bin/expect -f

set timeout 1

if { $argc!=1 } {
    send_user "usage: $argv0 <detectorId> \n"
    exit
}

set DETECTORID [lindex $argv 0]

if {[file isdirectory $DETECTORID]} {
    puts "directory has existed!"
} else {
    file mkdir $DETECTORID
}

# 为用户创建一个 key
spawn openssl genrsa -des3 -out ./$DETECTORID/client.key 2048
expect "Enter pass phrase for ./$DETECTORID/client.key:"
send "123456\r"
expect "Verifying - Enter pass phrase for ./$DETECTORID/client.key:"
send "123456\r"
puts "\n"

# 为 key 创建一个证书签名请求 csr 文件
spawn openssl req -new -key ./$DETECTORID/client.key -out ./$DETECTORID/client.csr -extensions v3_req -config "./conf/openssl.conf"
expect "Enter pass phrase for ./$DETECTORID/client.key:"
send "123456\r"
expect "Country Name (2 letter code) \[CN]:"
send "\r"
expect "State or Province Name (full name) \[BeiJing]:"
send "\r"
expect "Locality Name (eg, city) \[BeiJing]:"
send "\r"
expect "Organization Name (eg, company) \[IIE]:"
send "\r"
expect "Organizational Unit Name (eg, section) \[IIE]:"
send "\r"
expect "Common Name (e.g. server FQDN or YOUR name) \[]:"
send "$DETECTORID\r"
expect "Email Address \[xingxingwang@bupt.edu.cn]:"
send "\r"
expect "A challenge password \[]:"
send "123456\r"
expect "An optional company name \[]:"
send "\r"
puts "\n"

# 使用我们私有的 CA key 为刚才的 key 签名
spawn openssl ca -extensions v3_req -in ./$DETECTORID/client.csr -cert ./private/ca.crt -keyfile ./private/ca.key -out ./$DETECTORID/client.crt -config "./conf/openssl.conf"
expect "Sign the certificate? \[y/n]:"
send "y\r"
expect "1 out of 1 certificate requests certified, commit? \[y/n]"
send "y\r"
puts "\n"

# 将证书转换为大多数浏览器都能识别的 PKCS12 文件
spawn openssl pkcs12 -export -clcerts -in ./$DETECTORID/client.crt -inkey ./$DETECTORID/client.key -out ./$DETECTORID/client.p12
expect "Enter pass phrase for ./1/client.key:"
send "123456\r"
expect "Enter Export Password:"
send "123456\r"
expect "Verifying - Enter Export Password:"
send "123456\r"

set ca_src ./private/ca.crt 
set ca_dst ./$DETECTORID/

file copy $ca_src $ca_dst

expect eof
