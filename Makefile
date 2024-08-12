setup_ec2:
	bash setup/setup_vm.sh && \
	exec newgrp docker

LOCAL_TAG:=$(shell date +"%Y-%m-%d-%H-%M")
LOCAL_IMAGE_NAME:=stream-model-cyberbullying-detection:${LOCAL_TAG}

unit_tests:
	echo "Perform unit tests..."
	pytest tests/unit_tests

build: unit_tests
	cd ~/cyberbullying_detection/deployment && \
	docker build -t ${LOCAL_IMAGE_NAME} .

tests: build
	echo "Perform integration tests..."
	LOCAL_IMAGE_NAME=${LOCAL_IMAGE_NAME} bash tests/integration_tests/run.sh

quality_checks:
	isort .
	black .
	pylint --recursive=y .

run_pre_commit:
	pip install pre-commit
	pre-commit install