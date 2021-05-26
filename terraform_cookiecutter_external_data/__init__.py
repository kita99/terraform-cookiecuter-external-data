import os
import sys
import json
import glob
import uuid

from cookiecutter.main import cookiecutter


def generate_cookiecutter(config):
    cookiecutter_vars = json.loads(config["cookiecutter_vars"])
    output_dir = f"/tmp/{uuid.uuid4().hex}"

    cookiecutter(
        config["cookiecutter_repo"],
        checkout=config["cookiecutter_repo_commit_hash"],
        extra_context=cookiecutter_vars,
        output_dir=output_dir,
        no_input=True,
    )

    return glob.glob(f"{output_dir}/*")[0]


def list_resulting_files(output_dir):
    files = glob.glob(f"{output_dir}/**", recursive=True)
    files += glob.glob(f"{output_dir}/.**", recursive=True)
    files = [f for f in files if os.path.isfile(f)]
    return [f.removeprefix(output_dir + "/") for f in files]


def main():
    try:
        terraform_config = json.loads(sys.stdin.read())

        if "cookiecutter_repo" not in terraform_config:
            raise Exception("Missing cookiecutter_repo")

        if "cookiecutter_repo_commit_hash" not in terraform_config:
            raise Exception("Missing cookiecutter_repo_commit_hash")

        if "cookiecutter_vars" not in terraform_config:
            raise Exception("Missing cookiecutter_vars")

        prefix = generate_cookiecutter(terraform_config)
        files = list_resulting_files(prefix)

        output = json.dumps({
            "paths": ",".join(files),
            "prefix": prefix
        })
        sys.stdout.write(output)
    except Exception as e:
        sys.stderr.write(f'{type(e).__name__}: {e}')
        sys.exit(1)


if __name__ == '__main__':
    main()
