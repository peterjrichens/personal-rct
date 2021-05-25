.PHONY: setup_env remove_env new_config execute_nb publish
PROJECT_NAME=personal-rct

ifeq (,$(shell which pyenv))
	HAS_PYENV=False
	CONDA_ROOT=$(shell conda info --root)
	BINARIES = ${CONDA_ROOT}/envs/${PROJECT_NAME}/bin
else
	HAS_PYENV=True
	CONDA_VERSION=$(shell echo $(shell pyenv version | awk '{print $$1;}') | awk -F "/" '{print $$1}')
	BINARIES = $(HOME)/.pyenv/versions/${CONDA_VERSION}/envs/${PROJECT_NAME}/bin
endif

setup_env:
ifeq (True,$(HAS_PYENV))
	@echo ">>> Detected pyenv, setting pyenv version to ${CONDA_VERSION}"
	pyenv local ${CONDA_VERSION}
	conda env create --name $(PROJECT_NAME) -f environment.yaml --force
	pyenv local ${CONDA_VERSION}/envs/${PROJECT_NAME}
else
	@echo ">>> Creating conda environment."
	conda env create --name $(PROJECT_NAME) -f environment.yaml --force
	@echo ">>> Activating new conda environment"
	source $(CONDA_ROOT)/bin/activate $(PROJECT_NAME)
endif

remove_env:
ifeq (True,$(HAS_PYENV))
	@echo ">>> Detected pyenv, removing pyenv version."
	pyenv local ${CONDA_VERSION} && rm -rf ~/.pyenv/versions/${CONDA_VERSION}/envs/$(PROJECT_NAME)
else
	@echo ">>> Removing conda environemnt"
	conda remove -n $(PROJECT_NAME) --all
endif

new_config:
	cp config.example.yaml config.yaml

execute_nb:
	${BINARIES}/papermill notebook_template.ipynb temp_output.ipynb -f config.yaml

publish:
	${BINARIES}/jupyter nbconvert --to html temp_output.ipynb --no-input --template classic
	mv temp_output.html docs/${name}.html
	cd docs && tree -H '.' -L 2 --noreport --charset utf-8 > index.html
