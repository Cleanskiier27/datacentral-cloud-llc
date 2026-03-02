.PHONY: launchpad 10-1 launch ac lift

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
