#!/usr/bin/env bash
pip3 install --target ./package fsspec s3fs
cd package
zip -r ../temp_failure_detection_dp.zip .
cd ..
zip -g temp_failure_detection_dp.zip *.py