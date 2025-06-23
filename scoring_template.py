from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Load CodeLlama-7B model (adjust if using quantized or HF fine-tuned variant)
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

    # Extract the output after the prompt
    response = result.split("Binary output:")[-1].strip()
    return response

commit_m = """{{commit_msg}}"""
og_code = """{{original_code}}"""
new_code = """{{revised_code}}"""
context_c = """{{context_code}}"""
output = analyze_commit_codellama(commit_m, og_code, new_code, context_c)
print("CodeLlama Output:", output)
