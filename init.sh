#!/bin/bash

cd server
python -m SimpleHTTPServer 80 >> logs/site_log.txt