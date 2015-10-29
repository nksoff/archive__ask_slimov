#!/bin/bash

STREAMS="100"
REQUESTS="10000"

ab -c $STREAMS -n $REQUESTS "http://ask_slimov:8083/" > test-proxy-no-cache.log
echo "proxy NO cache is ready"
ab -c $STREAMS -n $REQUESTS "http://ask_slimov:8083/proxy-cache/" > test-proxy-with-cache.log
echo "proxy WITH cache is ready"
ab -c $STREAMS -n $REQUESTS "http://ask_slimov:8083/test-static.html" > test-static.log
echo "static is ready"
