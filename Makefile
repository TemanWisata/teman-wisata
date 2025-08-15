clean:
	uv run cleanpy .

setup-dev:
	uv sync
	uv run pre-commit install

setup:
	uv sync --no-dev

lint:
	uv run ruff check .
	uv run mypy .


setup-ui:
	echo "Setting up the project..."

run:
	uv run main.py

nerdctl-build:
	nerdctl --address /run/k3s/containerd/containerd.sock build -t teman-wisata -f deployment/docker/Dockerfile --namespace k8s.io .

docker-build:
	docker build -t teman-wisata -f deployment/docker/Dockerfile .

docker-run:
	docker run -d --name teman-wisata-apps -p 8000:8000 teman-wisata

docker-stop:
	docker stop teman-wisata-apps
