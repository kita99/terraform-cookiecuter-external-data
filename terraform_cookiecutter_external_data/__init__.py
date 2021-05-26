import os
import sys
import json
import glob
import uuid

from cookiecutter.main import cookiecutter


def generate_cookiecutter(config, output_path):
    cookiecutter_vars = json.loads(config["cookiecutter_vars"])

    cookiecutter(
        config["cookiecutter_repo"],
        checkout=config["cookiecutter_repo_commit_hash"],
        extra_context=cookiecutter_vars,
        output_dir=output_path,
        no_input=True,
    )


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

        output_path = "/tmp/" + uuid.uuid4().hex

        generate_cookiecutter(terraform_config, output_path)
        files = list_resulting_files(output_path)

        output = json.dumps({
            "paths": ",".join(files),
            "prefix": output_path
        })
        sys.stdout.write(output)
    except Exception as e:
        sys.stderr.write(f'{type(e).__name__}: {e}')
        sys.exit(1)


if __name__ == '__main__':
    main()
