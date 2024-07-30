setup_ec2:
	bash ~/setup/setup_vm.sh 

LOCAL_TAG:=$(shell date +"%Y-%m-%d-%H-%M")
LOCAL_IMAGE_NAME:=stream-model-duration:${LOCAL_TAG}

unit_tests:
	echo "Perform unit tests..."
	pytest tests/unit_tests

build: test
	docker build -t ${LOCAL_IMAGE_NAME} .

tests: build
	echo "Perform integration tests..."
	LOCAL_IMAGE_NAME=${LOCAL_IMAGE_NAME} bash tests/integraton_tests/run.sh

quality_checks:
	isort .
	black .
	pylint --recursive=y .

run_pre_commit:
	pip install pre-commit
	pre-commit install