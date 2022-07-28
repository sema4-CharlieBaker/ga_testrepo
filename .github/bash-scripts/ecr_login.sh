AWS_REGION=us-east-1
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --output text | cut -f1)
REGISTRY_URL=$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

aws ecr get-login-password --region $AWS_REGION | \
  docker login --username AWS --password-stdin $REGISTRY_URL
