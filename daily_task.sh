#!/bin/bash
set -e

make scratch-data
git commit -am "Back up db on $(date)" content.db
git push
