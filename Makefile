lint:
	isort .
	black .
	autoflake --in-place --remove-all-unused-imports --remove-unused-variables --recursive .
