
# LEFT OFF - try two

#cicd-datapipelines-dev--d70a65b DOWN
#cicd-datapipelines-dev--d02da00 DOWN
#cicd-datapipelines-dev--50fa64a DOWN
#cicd-datapipelines-dev--911576e

import boto3
import subprocess as sp
import sys
import os


ecs = boto3.client("ecs")

list_clusters_response = ecs.list_clusters()

deployment_project_names = []
for arn in list_clusters_response["clusterArns"]:
    project_name = arn.split("/")[-1]
    # project_sha = arn.split('--')[-1]
    deployment_project_names.append(project_name)


# Raises InvalidGitRepositoryError when not in a repo
# can remove dep with own function
# hardcoding the directory!
thisdir = os.path.dirname(os.path.abspath(__file__))


sys.exit()
tags = sp.check_output(["cd", thisdir, "ls", "../../.git/refs/tags"]).decode("utf-8")
tags = [tag for tag in tags.split("\n") if tag not in ("")]
shas = [tag.split("-D-")[-1] for tag in tags]

projects_to_be_torn_down = [
    name
    for name in deployment_project_names
    if name.split("--")[-1] not in shas
    # may need to change this
    and 'cicd-datapipelines' in name
    # any long standing deployments can stay here
    and name not in ['cicd-datapipelines-dev--911576e',]
]

print(projects_to_be_torn_down)
#sys.exit()


os.environ["AWS_REGION"] = "us-east-1"


COMPOSE_CMD_LOGIN = '''
AWS_REGION=us-east-1
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --output text | cut -f1)
REGISTRY_URL=$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
aws ecr get-login-password --region $AWS_REGION | \
  docker login --username AWS --password-stdin $REGISTRY_URL
'''

def ecs_login():
    os.system(COMPOSE_CMD_LOGIN)

COMPOSE_CMD_DOWN = '''
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
'''

def ecs_down():
    os.system(COMPOSE_CMD_DOWN)



for project in projects_to_be_torn_down:
    os.environ["SHORT_SHA"] = project.split('--')[-1]
    ecs_login()
    print('logged in')
    ecs_down()
    print('tearing down')

# LEFTOFF
# for project in projects_to_be_torn_down:
# docker command for tearing down project

# teardown
# 1. login
# 2. tear down


# will be an extension of the teardown script effectively, sub the 2
# steps at the end w this script


# can we test that the depl is running? w logs?
# docker compose --project-name PROJECT logs


sys.exit()




















