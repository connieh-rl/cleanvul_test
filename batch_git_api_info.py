import pandas as pd
from test_git_api import get_commit_message_from_url, get_changed_python_functions

def main():
    # Load the first 50 rows of the dataset
    df = pd.read_csv("./datasets/CleanVul_vulnscore_0.csv").head(50)
    results = []

    for idx, row in df.iterrows():
        commit_url = row.get('commit_url')
        if not commit_url or not isinstance(commit_url, str) or not commit_url.startswith("http"):
            continue

        # Get commit message
        try:
            commit_msg = get_commit_message_from_url(commit_url)
        except Exception as e:
            commit_msg = f"ERROR: {e}"

        # Get changed python functions
        try:
            context_code = get_changed_python_functions(commit_url)
        except Exception as e:
            context_code = f"ERROR: {e}"

        results.append({
            "commit_msg": commit_msg,
            "original_code": row.get('func_before', ''),
            "revised_code": row.get('func_after', ''),
            "context_code": str(context_code)
        })

    # Save to CSV
    out_df = pd.DataFrame(results)
    out_df.to_csv("batch_git_api_output.csv", index=False)
    print("Saved results to batch_git_api_output_vul0.csv")

if __name__ == "__main__":
    main()