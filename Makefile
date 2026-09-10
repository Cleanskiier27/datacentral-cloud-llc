.PHONY: launchpad 10-1 launch ac lift setup-arch setup-linux

launchpad:
	APP_URL=https://networkbuster.net $(MAKE) 10-1
	APP_URL=https://networkbuster.net $(MAKE) launch
	APP_URL=https://networkbuster.net $(MAKE) ac
	APP_URL=https://networkbuster.net $(MAKE) lift

10-1:
	@echo "[10-1] Run database migrations here. Set up your migration command (e.g., alembic upgrade head)."

launch:
	@echo "[launch] Run database seed here. Populate initial data for APP_URL=$(APP_URL)."

ac:
	@echo "[ac] Start the application here. Set up your start command (e.g., python main.py)."

lift:
	@echo "[lift] Run any post-start tasks here (e.g., worker processes, scheduled jobs)."

setup-arch:
	chmod +x ./setup_arch.sh
	./setup_arch.sh

setup-linux:
	chmod +x ./setup_linux.sh
	./setup_linux.sh

# --- MOONBASE.BOT / BUSTER.BOT Build Targets ---
.PHONY: build moonbase.bot buster.bot test docker-build docker-up docker-down

build: moonbase.bot

moonbase.bot:
	python scripts/build_moonbase_bot.py

buster.bot: moonbase.bot

test:
	python -m unittest test_moonbase_bot.py

docker-build:
	docker build -f Dockerfile.moonbase -t moonbase-bot:latest .

docker-up:
	docker compose -f docker-compose.minecraft.yml up -d

docker-down:
	docker compose -f docker-compose.minecraft.yml down

