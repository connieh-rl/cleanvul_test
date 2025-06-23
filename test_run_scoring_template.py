import argparse
import os
from jinja2 import Template
from pathlib import Path
import requests
from urllib.parse import urlparse
import random
import csv
from test_git_api import get_commit_message_from_url, get_java_methods_from_commit


def sample_random_row(csv_file_path):
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)  # DictReader uses the first row as headers

        selected_row = None
        for i, row in enumerate(reader, 1):
            if random.randint(1, i) == 1:
                selected_row = row  # row is an OrderedDict (acts like a dict)

    return selected_row

def retreive_cleanvul_instance_and_generate_scoring_script(score: int):
    path_to_open = os.path.expanduser(f'~/Desktop/CleanVul/datasets/CleanVul_vulnscore_{int(score)}.csv')
    sampled_instance_row = sample_random_row(path_to_open)
    #type(sampled_instance_row))
    template_path = Path(__file__).parent / ('scoring_template.py')
    template = Template(template_path.read_text())
    canonical_sol = sampled_instance_row['func_after']
    template_vars = {
        "commit_msg": get_commit_message_from_url(sampled_instance_row['commit_url']),
        "original_code": sampled_instance_row['func_before'],
        "revised_code": canonical_sol,
        "context_code": get_java_methods_from_commit(sampled_instance_row['commit_url'])
    }

    final_script = template.render(**template_vars)
    return final_script


def main():
    parser = argparse.ArgumentParser(description="Run file with a validation score.")

    parser.add_argument(
        "--validation_score",
        type=float,
        required=False,  
        help="Provide a numeric validation score (e.g., 0.85)."
    )

    args = parser.parse_args()

    if args.validation_score is not None:
        if args.validation_score in range(0, 4):
            print(f"Validation score provided: {args.validation_score}")
            # Your logic using the score

            test_github_commit_message = """
        `       403` on unauthorized grant API key action (#87461)

            Users with only the manage_own_api_key privilege are unauthorized to
            grant API keys. The current error response in this scenario is a 400,
            with a confusing error message. This PR changes error handling to
            return a 403 with a canonical 'action ... is unauthorized for user
            ...' error message instead, since the underlying cause is an
            authorization error rather than a bad request.

            Closes #87438
            """

            test_context_functions = """
            ['testAuthenticationWithApiKeyAllowsAccessToApiKeyActionsWhenItIsOwner', 'testAuthenticationWithApiKeyDeniesAccessToApiKeyActionsWhenItIsNotOwner', 'testAuthenticationWithUserAllowsAccessToApiKeyActionsWhenItIsOwner', 'testAuthenticationWithUserAllowsAccessToApiKeyActionsWhenItIsOwner_WithOwnerFlagOnly', 'testAuthenticationWithUserDeniesAccessToApiKeyActionsWhenItIsNotOwner', 'testGetAndInvalidateApiKeyWillRespectRunAsUser', 'testCheckQueryApiKeyRequest', 'testCheckGrantApiKeyRequestDenied', 'createUsers', 'cleanUp', 'testAuthenticateResponseApiKey', 'testGrantApiKeyForOtherUserWithPassword', 'testGrantApiKeyForOtherUserWithAccessToken', 'testGrantApiKeyWithoutApiKeyNameWillFail', 'testGrantApiKeyWithOnlyManageOwnApiKeyPrivilegeFails']
            """
            og_code = """@Override
        protected boolean extendedCheck(String action, TransportRequest request, Authentication authentication) {
            if (request instanceof CreateApiKeyRequest) {
                return true;
            } else if (request instanceof final GetApiKeyRequest getApiKeyRequest) {
                return checkIfUserIsOwnerOfApiKeys(
                    authentication,
                    getApiKeyRequest.getApiKeyId(),
                    getApiKeyRequest.getUserName(),
                    getApiKeyRequest.getRealmName(),
                    getApiKeyRequest.ownedByAuthenticatedUser()
                );
            } else if (request instanceof final InvalidateApiKeyRequest invalidateApiKeyRequest) {
                final String[] apiKeyIds = invalidateApiKeyRequest.getIds();
                if (apiKeyIds == null) {
                    return checkIfUserIsOwnerOfApiKeys(
                        authentication,
                        null,
                        invalidateApiKeyRequest.getUserName(),
                        invalidateApiKeyRequest.getRealmName(),
                        invalidateApiKeyRequest.ownedByAuthenticatedUser()
                    );
                } else {
                    return Arrays.stream(apiKeyIds)
                        .allMatch(
...
            throw new IllegalArgumentException(
                "manage own api key privilege only supports API key requests (not " + request.getClass().getName() + ")"
            );
        }"""
            
            revised_code = """
            @Override
        protected boolean extendedCheck(String action, TransportRequest request, Authentication authentication) {
            if (request instanceof CreateApiKeyRequest) {
                return true;
            } else if (request instanceof final GetApiKeyRequest getApiKeyRequest) {
                return checkIfUserIsOwnerOfApiKeys(
                    authentication,
                    getApiKeyRequest.getApiKeyId(),
                    getApiKeyRequest.getUserName(),
                    getApiKeyRequest.getRealmName(),
                    getApiKeyRequest.ownedByAuthenticatedUser()
                );
            } else if (request instanceof final InvalidateApiKeyRequest invalidateApiKeyRequest) {
                final String[] apiKeyIds = invalidateApiKeyRequest.getIds();
                if (apiKeyIds == null) {
                    return checkIfUserIsOwnerOfApiKeys(
                        authentication,
                        null,
                        invalidateApiKeyRequest.getUserName(),
                        invalidateApiKeyRequest.getRealmName(),
                        invalidateApiKeyRequest.ownedByAuthenticatedUser()
                    );
                } else {
                    return Arrays.stream(apiKeyIds)
                        .allMatch(
                            apiKeyId -> checkIfUserIsOwnerOfApiKeys(
                                authentication,
                                apiKeyId,
                                invalidateApiKeyRequest.getUserName(),
                                invalidateApiKeyRequest.getRealmName(),
                                invalidateApiKeyRequest.ownedByAuthenticatedUser()
                            )
                        );
                }   
            String message = "manage own api key privilege only supports API key requests (not " + request.getClass().getName() + ")";
            assert false : message;
            throw new IllegalArgumentException(message);
            }
            """

            template_path = Path(__file__).parent / ('scoring_template.py')
            template = Template(template_path.read_text())
            template_vars = {
                "commit_msg": test_github_commit_message,
                "original_code": og_code,
                "revised_code": revised_code,
                "context_code": test_context_functions,
            }

        final_script = template.render(**template_vars)
        print("Final script generated:\n", final_script)
        import subprocess
        subprocess.run(f"echo '{final_script}' > output.py", shell=True)
        #subprocess.run("python3 output.py", shell=True)

        result = subprocess.run("python3 output.py", shell=True, capture_output=True, text=True)

        output_str = result.stdout  # This is the printed output from output.py
        print("Captured output:", output_str)
        return output_str
    else:
        print("No validation score provided.")

if __name__ == "__main__":
    main()