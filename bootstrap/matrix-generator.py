import os
import json
import re
import uuid

# Base path configuration
config_path = os.getenv("config_path", "./")
tenant_name = os.getenv("tenant_name", "")
tenant_environment = os.getenv("tenant_environment", "")
workspace_name = os.getenv("workspace_name", "")

enviroment_values = ["dev", "test", "prod", "nonprod"]
accounts_files = []
tenant_workspaces = []
matrix_jobs = []

workspace_pattern = re.compile(r'^\s*([\w-]+)\s*=\s*{')

def get_tenant_from_path(path_parts):
    environment = ""
    tenant = ""
    if "accounts.tfvars" in path_parts:
        path_parts.remove("accounts.tfvars")
    # Remove config_path from the path parts
    config_parts = config_path.split(os.sep)
    for part in config_parts:
        if part in path_parts:
            path_parts.remove(part)
    tfvars_path = '/'.join(path_parts)
    if not tenant_environment:
        for env in enviroment_values:
            if env in path_parts:
                environment = env
                print(f"Found environment: '{environment}'")
                path_parts.remove(env)  # Only remove if found
                break
    else:
        environment = tenant_environment

    if not tenant_name:
        tenant_parts = path_parts.copy()  # Use a copy to avoid mutating the original list
        if len(tenant_parts) > 0:
            tenant = '/'.join(tenant_parts)
            print(f"Found tenant: '{tenant}'")
    else:
        tenant = tenant_name

    print(environment)
    print(tenant)
    print(tfvars_path)
    return tenant, environment, tfvars_path

def process_accounts_file(accounts_file):
    """Process an accounts.tfvars file and update matrix_jobs."""
    path_parts = os.path.normpath(accounts_file).split(os.sep)
    tenant, environment, tfvars_path = get_tenant_from_path(path_parts)
    print(f"Extracted tenant: '{tenant}', environment: '{environment}' from path: '{accounts_file}'")
    with open(accounts_file, 'r') as f:
        print(f"Processing {accounts_file}")
        for line in f:
            if "accounts_config" in line:
                continue
            match = workspace_pattern.match(line)
            if match:
                workspace = match.group(1)
                print(f"Found workspace: '{workspace}'")
                # Adjusting the comparison logic for partial match
                if (not tenant or tenant.startswith(tenant)) and (not environment or environment == environment) and (not workspace_name or workspace_name == workspace):
                    print(f"Adding job: tenant={tenant}, environment={environment}, workspace={workspace_name}")
                    matrix_jobs.append({
                        'tenant': tenant,
                        'environment': environment,
                        'workspace': workspace,
                        'tfvars_path': tfvars_path
                    })

# Walk through the directory structure starting from the base path
for root, dirs, files in os.walk(config_path):
    for file in files:
        if file == "accounts.tfvars":
            path_parts = os.path.normpath(root).split(os.sep)
            
            # Treat tenant_name as a single entity in the path
            if tenant_name:
                tenant_path = os.path.normpath(tenant_name)
                if tenant_path not in os.path.join(*path_parts):
                    continue  # Skip if tenant_name is not part of the current path
            
            # Skip irrelevant paths based on environment
            if tenant_environment and tenant_environment not in path_parts:
                continue

            print(f'Looking for config files for {tenant_name} in environment {tenant_environment}')
            accounts_files.append(os.path.join(root, file))

if not accounts_files:
    print("No accounts.tfvars files found.")
    exit(1)
print(accounts_files)

for accounts_file in accounts_files:
    process_accounts_file(accounts_file)

# Convert matrix_jobs to JSON
matrix_jobs_json = json.dumps(matrix_jobs)
print(f"matrix_jobs={matrix_jobs_json}")

# Output to GitHub Actions
with open(os.getenv('GITHUB_OUTPUT'), 'a') as gh_output:
    print(f"matrix_jobs={matrix_jobs_json}", file=gh_output)
