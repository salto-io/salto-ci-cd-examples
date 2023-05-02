This folder includes [Salto](https://www.salto.io/) CI file examples for azure devops. 

For more information about integrating Salto deployments with git please follow [this guide](https://help.salto.io/en/articles/7182069-integrating-pull-requests-and-automating-with-salto)

___

Please note:
- Azure Devops yml files should be named `.azure-pipelines.yml` and kept under the root folder of your repository
- You azure pipeline should include a secret var named `SALTO_API_TOKEN` that keeps your Salto API token. Instructions for defining a secret var in your azure pipeline can be found [here](https://learn.microsoft.com/en-us/azure/devops/pipelines/process/set-secret-variables?view=azure-devops&tabs=yaml%2Cbash)