import os
import sys
import json
import glob
import uuid

from cookiecutter.main import cookiecutter


def generate_cookiecutter(config):
    cookiecutter_vars = json.loads(config["cookiecutter_vars"])
    output_dir = f"/tmp/{uuid.uuid4().hex}"
    checkout = None

    if "cookiecutter_git_checkout" in config:
        checkout = config["cookiecutter_git_checkout"]

    cookiecutter(
        config["cookiecutter_template"],
        checkout=checkout,
        extra_context=cookiecutter_vars,
        output_dir=output_dir,
        no_input=True,
    )

    return glob.glob(f"{output_dir}/*")[0]


def list_resulting_files(output_dir):
    result = []

    for root, _, files in os.walk(output_dir):
        dir_without_prefix = root.removeprefix(output_dir)
        dir_without_prefix = dir_without_prefix.removeprefix("/")

        for f in files:
            file = f

            if dir_without_prefix:
                file = f"{dir_without_prefix}/{f}"

            result.append(file)

    return result


def template_is_repository(template):
    if template.startswith("git"):
        return True

    if template.startswith("https://"):
        return True

    if template.startswith("gh:"):
        return True

    return False


def main():
    try:
        terraform_config = json.loads(sys.stdin.read())

        if "cookiecutter_template" not in terraform_config:
            raise Exception("Missing cookiecutter_template")

        if template_is_repository(terraform_config["cookiecutter_template"]):
            if "cookiecutter_git_checkout" not in terraform_config:
                raise Exception("Missing cookiecutter_git_checkout")

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
