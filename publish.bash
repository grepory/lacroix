#!/usr/bin/env bash 

for f in *.py; do
  fun=${f%.*}
  echo "Publishing function - $fun"
  aws --debug lambda update-function-code --s3-bucket opsee-releases --s3-key python/lacroix/lacroix.zip --function-name $fun
done
