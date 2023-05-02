This folder includes [Salto](https://www.salto.io/) CI file examples for github. 

For more information about integrating Salto deployments with git please follow [this guide](https://help.salto.io/en/articles/7182069-integrating-pull-requests-and-automating-with-salto)

___

Please note:
- Github yml files should be kept under the `.github/workflows` folder in your repository
- You repository should include a secret var named `SALTO_API_TOKEN` that keeps your Salto API token.
Instructions for defining secrets in your Github repo can be found [here](https://docs.github.com/en/actions/security-guides/encrypted-secrets)