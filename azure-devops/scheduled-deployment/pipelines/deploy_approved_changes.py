# import the libraries needed by the script
import os
import requests
from requests.auth import HTTPBasicAuth
import pprint
import subprocess
import sys

# The tokens ae stored as secret variables in the pipeline
auth_token = os.environ['ADO_AUTH_TOKEN']
salto_api_token = os.environ['SALTO_API_TOKEN']

# base_url, project, and repository are environment variables from the VM
base_url = os.environ['ENDPOINT_URL_SYSTEMVSSCONNECTION']
project = os.environ['SYSTEM_TEAMPROJECT']
repository = os.environ['BUILD_REPOSITORY_NAME']

# params are for URL exansion.  This script was tested against api version
# 7.1-preview.1  https://learn.microsoft.com/en-us/rest/api/azure/devops/core/?view=azure-devops-rest-7.1
params = {"api-version" : "7.1-preview.1"}


def get_pull_requests():
    # get all pull requests for the repository and return the
    # pull request ID and other key information
    ####
    # initialize the dictionary to be returned to calling process
    all_prs = {}
    # construct the URL to get the PRs for this repository
    url = base_url + project + '/_apis/git/repositories/' + repository + '/pullrequests'
    # perform the GET request
    response = requests.get(url, auth=HTTPBasicAuth('', auth_token), params=params)
    # check to see if the GET request was successful
    if response.status_code != 200:
        # exit with the error code if it was unsuccessful
        sys.exit(response.status_code)
    # get the JSON from the GET 
    all_pr_data = response.json()
    # iterate over the pull requests to build the required data structure
    for pull_request in all_pr_data['value']:
        pr_id = pull_request['pullRequestId']
        project_id = pull_request['repository']['project']['id']
        raw_branch = pull_request['targetRefName']
        target_branch = raw_branch.replace('refs/heads/','')
        all_prs[pr_id] = {'project_id':project_id,
                          'target_branch':target_branch
                          }
    # return the required data structure
    return(all_prs)

def get_pr_status(pr_id, project_id):
    # check the pull request and ensure all of the required checks have passed
    ####
    # construct the artifact ID for the pull request passed
    # template for artifact ID:  https://learn.microsoft.com/en-us/rest/api/azure/devops/policy/evaluations/list?view=azure-devops-rest-7.1
    artifact_id = 'vstfs:///CodeReview/CodeReviewId/' + project_id + '/' + str(pr_id)
    # add the artifact ID to the URL parameters
    params["artifactId"] = artifact_id
    # construct the URL to get the PRs for this repository
    url = base_url + project + '/_apis/policy/evaluations'
    # perform the GET request
    response = requests.get(url, auth=HTTPBasicAuth('', auth_token), params=params)
    # check to see if the GET request was successful
    if response.status_code != 200:
        # exit with the error code if it was unsuccessful
        sys.exit("Unable to get status for Pull Request #" + str(pr_id))
    # get the JSON from the GET 
    all_data = response.json()
    eval_list = all_data['value']
    # iterate over the evaluations ensuring all requirements are fulfilled
    for config in eval_list:
        print(config['status'])
        if config['status'] != 'approved':
            return False
    # Now we've made it all the way thru all of the configurations 
    # and all have returned 'approved' so we can say everything is approved
    return True

def download_salto_client():
    # Download and extract the Salto client
    ####
    print('Downloading Salto Client')
    # download the Salto client
    file_name = 'linux-x64.tar.gz'
    url = 'https://cli.salto.io/release/1/linux-x64.tar.gz'
    # perform the GET request
    response = requests.get(url)
    # check to see if the GET request was successful
    if response.status_code != 200:
        # exit with the error code if it was unsuccessful
        sys.exit('Unable to download Salto client')
    # write the file to disk
    with open(file_name, mode='wb') as file:
        file.write(response.content)
    print('Extracting Salto Client')
    # extract the compressed tar file
    subprocess.run(['tar', 'xvzf', file_name])
    
def execute_salto_deployment(target_branch):
   # run the Salto deployment and capture the STDERR for use if necessary
   result = subprocess.run(['./salto-cloud'
                            ,'deployment'
                            ,'deploy'
                            ,'--api-token'
                            ,salto_api_token
                            ,'--branch-name'
                            ,target_branch
                            ,'--push']
                            ,stderr=subprocess.PIPE
                        )
   print('Return Code: ', result.returncode)
   # check to see if the Salto deployment was successful
   if result.returncode != 0:
       # report the error and exit
       print(result.stderr)
       exit(result.returncode)


if __name__ == "__main__":
    # get all active pull requests for the repository
    active_pull_requests = get_pull_requests()
    pprint.pp(active_pull_requests)
    # iterate over the list of PRs to get the status
    for pull_request in list(active_pull_requests.keys()):
        project_id = active_pull_requests[pull_request]['project_id'] 
        print(project_id)
        # check the approval status of the pull request
        pr_status = get_pr_status(pull_request, project_id)
        # if the PR is not approved, remove it from the list of PRs
        if not pr_status:
            del active_pull_requests[pull_request]
    pprint.pp(active_pull_requests)
    # if there are no PRs left in the list, exit success
    if len(active_pull_requests) < 1: 
        print('No approved pull requests.  Exiting.')
        exit(0)
    # if there are any PRs left in the list, they are approved so
    # download the Salto client
    download_salto_client()
    # for all remaining approved PRs, use Salto to deploy them in 
    # PR ID order (oldest to newest)
    for pull_request in sorted(list(active_pull_requests.keys())):
        execute_salto_deployment(active_pull_requests[pull_request]['target_branch'])