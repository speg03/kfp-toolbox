#!/usr/bin/env bash

set -x

output_dir="$(mktemp -d)"
dsl-compile --mode=V2_COMPATIBLE --py=./examples/echo_pipeline.py --function=echo_pipeline --output="${output_dir}/echo_pipeline.yaml"
dsl-compile-v2 --py=./examples/echo_pipeline.py --function=echo_pipeline --output="${output_dir}/echo_pipeline.json"
