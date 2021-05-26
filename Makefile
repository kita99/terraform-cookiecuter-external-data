help:
	@echo "  build       build pyz package"


build:
	@poetry install
	@poetry run shiv --python "/usr/bin/env python3" --site-packages "$$(poetry env info --path)" -e terraform_cookiecutter_external_data:main -o terraform-cookiecutter-external-data.pyz .
