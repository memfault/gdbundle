#!/usr/bin/env bash

set -euo pipefail

cd app
tox
du -sh .
