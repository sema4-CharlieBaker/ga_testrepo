AWS_REGION=us-east-1
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --output text | cut -f1)
REGISTRY_URL=$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
PROJECT_NAME=cicd-datapipelines-dev--$SHORT_SHA

docker context create ecs myecscontext --from-env

GITHUB_SHA=$SHORT_SHA \
REGISTRY_URL=$REGISTRY_URL \
  docker --context myecscontext \
    compose \
    --project-name $PROJECT_NAME \
    down
