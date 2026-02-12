import tomllib
import os
import subprocess
import sys

def sync_metadata():
    try:
        with open("pyproject.toml", "rb") as f:
            data = tomllib.load(f)
        
        project = data.get("project", {})
        description = project.get("description", "")
        keywords = project.get("keywords", [])
        
        if not description and not keywords:
            print("No metadata found in pyproject.toml")
            return

        # Prepare gh command
        # gh repo edit [repo] --description "..." --add-topic "topic1,topic2"
        cmd = ["gh", "repo", "edit", os.environ.get("GITHUB_REPOSITORY"), "--description", description]
        
        if keywords:
            # Note: gh repo edit --add-topic replaces or appends depending on version, 
            # but usually it's cleaner to set them all.
            # Using --add-topic and joining by comma is the standard way.
            topics = ",".join(keywords)
            cmd.extend(["--add-topic", topics])
        
        print(f"Executing: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Error updating metadata: {result.stderr}")
            sys.exit(1)
        
        print("Metadata synced successfully!")

    except FileNotFoundError:
        print("pyproject.toml not found")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    sync_metadata()
