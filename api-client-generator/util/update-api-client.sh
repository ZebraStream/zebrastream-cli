#!/usr/bin/env sh
#
# Quick and dirty update routine, waiting for better automation
# TODO: manage openapi-python-client in build environment

exec openapi-python-client generate --path openapi-mod.json --config openapi-python-client.yml --output-path . --overwrite
