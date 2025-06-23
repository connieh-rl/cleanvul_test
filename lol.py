from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Load CodeLlama-7B model
model_name = "codellama/CodeLlama-7b-hf"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16, device_map="auto")

def analyze_commit_codellama(commit, original, revised, context):
    prompt = f"""
The Prompt Produces a Binary Output:

As a cybersecurity expert, analyze the provided "Original" and "Revised" code snippets from a commit, along with the commit message and other functions in the same commit. The "Original" code represents the state before the changes, while the "Revised" code represents the state after the changes. Determine if the changes are focused on fixing vulnerabilities; if so, output 1, otherwise output 0. The length of the code snippet should not influence your assessment; concentrate on evaluating the logic line by line.

- A score of 0 indicates that the changes made from the "Original" code to the "Revised" code do not address vulnerability fixes.
- A score of 1 indicates that the changes made from the "Original" code to the "Revised" code are aimed at fixing vulnerabilities.

Commit Message: {commit}

Original code snippet (code before changes):
{original}

Revised code snippet (code after changes):
{revised}

Here are the other functions in the same commit:
{context}

Binary output:
"""
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, max_new_tokens=10)
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    response = result.split("Binary output:")[-1].strip()
    return response

# --- Inputs ---
commit_m = """403 on unauthorized grant API key action (#87461)

Users with only the manage_own_api_key privilege are unauthorized to grant API keys. 
The current error response in this scenario is a 400, with a confusing error message. 
This PR changes error handling to return a 403 with a canonical 'action ... is unauthorized for user ...' 
error message instead, since the underlying cause is an authorization error rather than a bad request.

Closes #87438"""

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
                .allMatch( /* elided */ );
        }
    }
    throw new IllegalArgumentException(
        "manage own api key privilege only supports API key requests (not " + request.getClass().getName() + ")"
    );
}"""

new_code = """@Override
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
    }
    String message = "manage own api key privilege only supports API key requests (not " + request.getClass().getName() + ")";
    assert false : message;
    throw new IllegalArgumentException(message);
}"""

context_c = """[
    'testAuthenticationWithApiKeyAllowsAccessToApiKeyActionsWhenItIsOwner',
    'testAuthenticationWithApiKeyDeniesAccessToApiKeyActionsWhenItIsNotOwner',
    'testAuthenticationWithUserAllowsAccessToApiKeyActionsWhenItIsOwner',
    'testAuthenticationWithUserAllowsAccessToApiKeyActionsWhenItIsOwner_WithOwnerFlagOnly',
    'testAuthenticationWithUserDeniesAccessToApiKeyActionsWhenItIsNotOwner',
    'testGetAndInvalidateApiKeyWillRespectRunAsUser',
    'testCheckQueryApiKeyRequest',
    'testCheckGrantApiKeyRequestDenied',
    'createUsers',
    'cleanUp',
    'testAuthenticateResponseApiKey',
    'testGrantApiKeyForOtherUserWithPassword',
    'testGrantApiKeyForOtherUserWithAccessToken',
    'testGrantApiKeyWithoutApiKeyNameWillFail',
    'testGrantApiKeyWithOnlyManageOwnApiKeyPrivilegeFails'
]"""

# --- Run model ---
output = analyze_commit_codellama(commit_m, og_code, new_code, context_c)
print("CodeLlama Output:", output)
