#!/bin/bash
reqs="./requirements.txt"
readonly reqs
echo "正在安装依赖环境"
pip3 install -r ${reqs}
echo "正在创建数据库..."
python3 tools/dump_to_db.py
