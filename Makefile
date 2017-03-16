.PHONY: test docs infra


test: flake8 test_codebase

flake8:
	flake8 api

pylint:
	pylint --rcfile=pylintrc api -E

test_codebase:
	py.test tests/ --cov=$(CURDIR)/api --cov-config=$(CURDIR)/.coveragerc

test_docs: docs spelling #linkcheck

docs:
	sphinx-build -n -b html -d docs/build/doctrees docs docs/build/html

linkcheck:
	sphinx-build -W -b linkcheck -d docs/build/doctrees docs docs/build/linkcheck
infra:	infra_apply

ENV=local
infra_apply:
	cd infra/terraform/$(ENV) && terraform apply

ENV=local
infra_clean:
	cd infra/terraform/$(ENV) && terraform destroy -force

spelling:
	sphinx-build -b spelling -d docs/build/doctrees docs docs/build/spelling
