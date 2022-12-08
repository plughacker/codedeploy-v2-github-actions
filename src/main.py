#!/usr/bin/env python

import boto3
import json
import time
import sys
import os

def aws_client(resource: str):
    client = boto3.client(resource)
    return client

def get_latest_task_definition(application_name: str) -> str:
    client = aws_client("ecs")

    response = client.list_task_definitions(
        familyPrefix=application_name,
        status="ACTIVE",
        sort="DESC",
        maxResults=1
    )

    return response["taskDefinitionArns"][0]

def create_spec_content(application_name: str):
    task_definition = get_latest_task_definition(application_name)

    return {
        "version": 0.0,
        "Resources": [{
            "TargetService": {
                "Type": "AWS::ECS::Service",
                "Properties": {
                    "TaskDefinition": task_definition,
                    "LoadBalancerInfo": {
                        "ContainerName": application_name,
                        "ContainerPort": 3000
                    }
                }
            }
        }]
    }

def create_deployment(application_name: str, deployment_config_name: str) -> str:
    client = aws_client("codedeploy")

    response = client.create_deployment(
        applicationName=application_name,
        deploymentGroupName=f"{application_name}-deployment-group",
        deploymentConfigName=deployment_config_name,
        revision={
            "revisionType": "AppSpecContent",
            "appSpecContent": {
                "content": str(create_spec_content(application_name)),
            }
        }
    )

    return response["deploymentId"]

def wait_deployment(deployment_id: str, target_id: str):
    client = aws_client("codedeploy")

    while True:
        time.sleep(30)

        response = client.get_deployment_target(
            deploymentId=deployment_id,
            targetId=target_id
        )

        ecs_target = response['deploymentTarget']['ecsTarget']
        task_info = ecs_target["taskSetsInfo"]

        for info in task_info:
            print(json.dumps(info, indent=4))
            print("")

        if ecs_target["status"] != "InProgress":
            sys.exit(0)

def main():
    application_name = os.environ.get("INPUT_APPLICATION_NAME")
    cluster_name = os.environ.get("INPUT_CLUSTER_NAME")
    deployment_config_name = os.environ.get("INPUT_DEPLOYMENT_CONFIG_NAME")

    deployment_id = create_deployment(application_name, deployment_config_name)
    wait_deployment(deployment_id, f"{cluster_name}:{application_name}")

if __name__ == "__main__":
    main()
