#!/usr/bin/env python

import boto3
import json
import time
import pprint

def aws_client(resource: str):
    client = boto3.client(resource)
    return client

def get_latest_task_definition(application_name: str) -> str:
    client = aws_client("ecs")

    print(application_name)

    response = client.list_task_definitions(
        familyPrefix=application_name,
        status="ACTIVE",
        sort="DESC",
        maxResults=1
    )

    return response["taskDefinitionArns"][0]

def create_spec_content(application_name: str):
    return {
        "version": 0.0,
        "Resources": [{
            "TargetService": {
                "Type": "AWS::ECS::Service",
                "Properties": {
                    "TaskDefinition": get_latest_task_definition(application_name),
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

    deployment_status = ""

    while ecs_target["status"] == "InProgress":
        response = client.get_deployment_target(
            deploymentId=deployment_id,
            targetId=target_id
        )

        task_info = ecs_target["taskSetsInfo"]
        
        for info in task_info:
            print(json.dumps(info, indent=4))
            print("")

        time.sleep(30)


    print(target)

def main():
    #deployment_id = create_deployment("poc-sre-246-dev", "CodeDeployDefault.ECSAllAtOnce")
    wait_deployment("d-SWVT1UBHL", "plug-pagamentos-nt-dev:poc-sre-246-dev")

if __name__ == "__main__":
    main()