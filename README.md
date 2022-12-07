# codedeploy-v2-github-actions

## Example

```
on: [push]


jobs:
  code_deploy:
    name: 'Code Deploy'
    runs-on: ubuntu-latest
    steps:
      - name: Code deploy
        uses: plughacker/codedeploy-v2-github-actions 
        with:
          application_name: ms-test
          cluster_name: default
          deployment_config_name: CodeDeployDefault.ECSAllAtOnce 
          region: us-east-1
```

## Inputs

| Input name     | Description                                         | Required |
|----------------|-----------------------------------------------------|----------|
| application_name         | The name of the Code Deploy               | Yes      |
| cluster_name             | The name of the ECS cluster               | Yes      |
| deployment_config_name   | The name of the Code Deploy config        | Yes      |
| region                   | AWS Region                                |          |

