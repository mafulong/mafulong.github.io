.PHONY: help install serve clean

help:
	@echo "Usage:"
	@echo "  make install   - Install dependencies"
	@echo "  make serve    - Start local preview server"
	@echo "  make clean   - Clean generated files"

install:
	@echo "Installing dependencies..."
	bundle install

serve: install
	@echo "Starting Jekyll server at http://127.0.0.1:4000"
	@echo "Press Ctrl+C to stop"
	bundle exec jekyll serve --port 4000

clean:
	@echo "Cleaning generated files..."
	rm -rf _site
