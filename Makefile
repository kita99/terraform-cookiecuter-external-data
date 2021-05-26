help:
	@echo "  build       build pyz package"


build:
	@poetry install
	@poetry run shiv --python "/usr/bin/env python3" --site-packages "$$(poetry env info --path)" -e terraform_external_data_cookiecutter:main -o terraform-external-data-cookiecutter.pyz .

