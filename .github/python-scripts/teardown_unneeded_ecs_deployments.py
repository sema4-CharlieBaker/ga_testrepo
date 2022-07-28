import boto3
import subprocess as sp
import sys
import os


## compute projects_to_be_torn_down
# get project-names of deployments of the application
def list_clusters():
    ecs = boto3.client("ecs")
    arns = ecs.list_clusters()["clusterArns"]
    return [arn.split("/")[-1] for arn in arns]


deployment_project_names = list_clusters()

# get shas of deployment tags
os.chdir(os.path.dirname(os.path.abspath(__file__)))
tags = sp.check_output(["ls", "../../.git/refs/tags"]).decode("utf-8")
tags = [tag for tag in tags.split() if tag not in ("")]
shas = [tag.split("-D-")[-1] for tag in tags]
print("shas", shas)

# compute projects to be torn down
projects_to_be_torn_down = [
    name
    for name in deployment_project_names
    # if hash not in the existing tags
    if name.split("--")[-1] not in shas
    # may need to change this
    and "cicd-datapipelines" in name
    # any long standing deployments can stay here
    and name
    not in [
        "cicd-datapipelines-dev--911576e",
    ]
]

print("projects_to_be_torn_down", projects_to_be_torn_down)


## read in the login and teardown docker-compose scripts and execute
def read_script(path):
    with open(path, "r") as f:
        return f.read()


COMPOSE_CMD_LOGIN = read_script("../bash-scripts/ecr_login.sh")
COMPOSE_CMD_DOWN = read_script("../bash-scripts/ecs_down.sh")


os.environ["AWS_REGION"] = "us-east-1"
for project in projects_to_be_torn_down:
    os.environ["SHORT_SHA"] = project.split("--")[-1]
    os.system(COMPOSE_CMD_LOGIN)
    os.system(COMPOSE_CMD_DOWN)
