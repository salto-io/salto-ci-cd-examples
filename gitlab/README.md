This folder includes [Salto](https://www.salto.io/) CI file examples for gitlab. 

For more information about integrating Salto deployments with git please follow [this guide](https://help.salto.io/en/articles/9909341-salto-git-integration-overview)

___

Please note:
- Gitlab yml files should be named `.gitlab-ci.yml` and kept under the root folder of your repository
- You will need to replace the string `SALTO_API_TOKEN_HERE` with your Salto API token. It is very highly recommended to use a secret for keeping this token. Instructions for defining secrets in your Gitlab repo can be found [here](https://docs.gitlab.com/ee/ci/secrets/)