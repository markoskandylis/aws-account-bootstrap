import os
import json
import re
import uuid

# Base path configuration
lza_environment = os.getenv("LZA_ENVIRONMENT")
tenant_input = os.getenv("TENANT_INPUT", "")
environment_input = os.getenv("ENVIRONMENT_INPUT", "")
base_path = f"tenants/{lza_environment}"
accounts_files = []
tenant_workspaces = []

daccounts_files = []
matrix_jobs = []

def get_tenant_from_path(path_parts):
    """Extract tenant name and environment from path parts."""
    if "accounts.tfvars" in path_parts:
        path_parts.remove("accounts.tfvars")
    index = len(path_parts) - 1

    # Determine tenant and environment
    tenant = "/".join(path_parts[2:index])
    environment = path_parts[index]
    return tenant, environment

def process_accounts_file(accounts_file):
    """Process an accounts.tfvars file and update matrix_jobs."""
    path_parts = os.path.normpath(accounts_file).split(os.sep)
    tenant, environment = get_tenant_from_path(path_parts)
    if tenant and environment:
        # Find or create the tenant entry
        with open(accounts_file, 'r') as f:
            print(f"Processing {accounts_file}")
            for line in f:
                if "env_config" in line:
                    continue
                match = workspace_pattern.match(line)
                if match:
                    workspace_name = match.group(1)
                    if (not tenant_input or tenant == tenant_input) and (not environment_input or environment == environment_input):
                        matrix_jobs.append({
                            'tenant': tenant,
                            'environment': environment,
                            'workspace': workspace_name
                        })

# Walk through the directory structure starting from the base path
for root, dirs, files in os.walk(base_path):
    for file in files:
        if file == "accounts.tfvars":
            path_parts = os.path.normpath(root).split(os.sep)
            # Skip if tenant_input is specified and not in the path
            if tenant_input and tenant_input not in path_parts:
                continue
            if environment_input and environment_input not in path_parts:
                continue
            
            tenant, environment = get_tenant_from_path(path_parts)
            if tenant and environment:
                # Append the file path to the accounts_files list
                accounts_files.append(os.path.join(root, file))

if not accounts_files:
    print("No accounts.tfvars files found.")
    exit(1)
print(accounts_files)
workspace_pattern = re.compile(r'^\s*([\w-]+)\s*=\s*{')

for accounts_file in accounts_files:
    process_accounts_file(accounts_file)

# Convert matrix_jobs to JSON
matrix_jobs_json = json.dumps(matrix_jobs)
print(f"matrix_jobs={matrix_jobs_json}")

# Output to GitHub Actions
# Output to GitHub Actions
with open(os.getenv('GITHUB_OUTPUT'), 'a') as gh_output:
    print(f"matrix_jobs={matrix_jobs_json}", file=gh_output)
