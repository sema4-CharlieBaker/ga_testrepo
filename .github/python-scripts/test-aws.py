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


print(deployment_project_names)

# Raises InvalidGitRepositoryError when not in a repo
# can remove dep with own function
# hardcoding the directory!
thisdir = os.path.dirname(os.path.abspath(__file__))
print(thisdir)
os.chdir(thisdir)
tags = sp.check_output(["ls", "../../.git/refs/tags"]).decode("utf-8")
print(tags)
tags = [tag for tag in tags.split() if tag not in ("")]
print(tags)
shas = [tag.split("-D-")[-1] for tag in tags]
print(shas)

projects_to_be_torn_down = [
    name
    for name in deployment_project_names
    # if hash not in the existing tags
    if name.split("--")[-1] not in shas
    # may need to change this
    and 'cicd-datapipelines' in name
    # any long standing deployments can stay here
    and name not in ['cicd-datapipelines-dev--911576e',]
]

print(projects_to_be_torn_down)


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






















