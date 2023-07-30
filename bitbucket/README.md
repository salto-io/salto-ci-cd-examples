This folder includes [Salto](https://www.salto.io/) CI file examples for bitbucket. 

For more information about integrating Salto deployments with git please follow [this guide](https://help.salto.io/en/articles/7182069-integrating-pull-requests-and-automating-with-salto)

___

Please note:
- BitBucket yml files should be named `bitbucket-pipelines.yml` and kept under the root folder of your repository
- You repository should include a secret var named `SALTO_API_TOKEN` that keeps your Salto API token. Instructions for defining a secret var in your BitBucket repo can be found [here](https://support.atlassian.com/bitbucket-cloud/docs/variables-and-secrets/)
