#!/usr/bin/env bash
pip3 install --target ./package fsspec s3fs
cd package
zip -r ../ppg_failure_detection_dp.zip .
cd ..
zip -g ppg_failure_detection_dp.zip *.py