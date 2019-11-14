#!/bin/bash

for i in $( seq 1 50 )
do
    nohup python aaa_test_https.py >./log/test${i}.log &
done