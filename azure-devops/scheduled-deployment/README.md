# README.md

Azure DevOps (ADO) does not have an event trigger for “Pull Request Approved” so the mechanism for automatically deploying upon pull request (PR) approval is unavailable.  To get a similar behavior, this `azure-pipelines.yml` and accompanying script periodically poll the ADO API to determine if there are any approved PRs and if so, deploy them.

The polling frequency is set to every 15 minutes because of the [limitations](https://learn.microsoft.com/en-us/azure/devops/pipelines/process/scheduled-triggers?view=azure-devops&tabs=yaml#limits-on-the-number-of-scheduled-runs-in-yaml-pipelines) on the number of YAML pipelines ADO permits (1000 per week).  This results in 672 scheduled runs per week.  There are also Individual runs that will execute when the PR is created, when the PR is closed, and anytime the scripts or yaml file is updated.

### Assumptions:

The `azure-pipelines.yml` expects the script to be in a `pipelines` folder.

[ADO_AUTH_TOKEN](https://learn.microsoft.com/en-us/azure/devops/organizations/accounts/use-personal-access-tokens-to-authenticate?view=azure-devops&tabs=Windows#create-a-pat) and [SALTO_API_TOKEN](https://help.salto.io/en/articles/7245637-salto-cli#h_749fb329f7) are set as SECRET variables.

All files are on the `main` branch.