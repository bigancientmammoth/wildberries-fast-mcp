
.PHONY: build
build: python -m build

.PHONY: deploy
deploy: twine upload dist/*


