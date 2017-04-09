aws s3 sync wwwroot s3://donm.cc \
    --acl public-read \
    --exclude '.DS_Store'

