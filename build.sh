#!/bin/bash

pip install -r requirements.txt

rm -rf ./src/generated
mkdir -p ./src/generated

python -m grpc_tools.protoc --proto_path=./src --python_out=./src/generated --grpc_python_out=./src/generated server.proto
