aws s3 --region us-east-1 sync --cache-control no-cache --exclude "*" --include "*.html" docs/_build/html s3://drafting.goodhertz.com
aws s3 --region us-east-1 sync docs/_build/html s3://drafting.goodhertz.com