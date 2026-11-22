#!/bin/bash
# fixlocal.sh - Chạy khi container khởi động, khởi động mock_server.py một lần duy nhất
if ! pgrep -f "mock_server.py" > /dev/null; then
    nohup python3 /home/ubuntu/srv/mock_server.py > /home/ubuntu/srv/mock_server.log 2>&1 &
fi
