import argparse
from jinja2 import Template
from pathlib import Path
import requests
from urllib.parse import urlparse

from test_git_api import get_commit_message_from_url

def main():
    parser = argparse.ArgumentParser(description="Run file with a validation score.")

    parser.add_argument(
        "--validation_score",
        type=float,
        required=False,  # Make True if you want to force the user to provide it
        help="Provide a numeric validation score (e.g., 0.85)."
    )

    args = parser.parse_args()

    if args.validation_score is not None:
        if args.validation_score in range(0, 4):
            print(f"Validation score provided: {args.validation_score}")
            # Your logic using the score

            #Retrieve.

            #Fill in scoring template.


    else:
        print("No validation score provided.")

if __name__ == "__main__":
    main()

def sample_random_row(csv_file_path):
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # Skip or store header if needed

        selected_row = None
        for i, row in enumerate(reader, 1):
            if random.randint(1, i) == 1:
                selected_row = row

    return selected_row

def retreive_cleanvul_instance_and_generate_scoring_script(score: int):
    path_to_open = (f'../CleanVul/datasets/CleanVul_vulnscore_{str(score)}.csv')
    sampled_instance_row = sample_random_row(path_to_open)
    template_path = ('scoring_template.py')
    template = Template(template_path.read_text())
    canonical_sol = sampled_instance_row['func_after']
    template_vars = {   
        # "config_filename": "test_config.json",
        "commit_msg":get_commit_message_from_url(sampled_instance_row['commit_url']),
        "original_code":sampled_instance_row['func_before'],
        "revised_code":canonical_sol,
        "context_code":
    }

    final_script = template.render(**template_vars)
    return final_script
