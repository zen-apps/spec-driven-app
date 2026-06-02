copy-skills:
	rm -rf .claude/skills
	mkdir -p .claude/skills
	cp -R skills/. .claude/skills/
	if [ -d optional_skills ]; then cp -R optional_skills/. .claude/skills/; fi
	@echo "Copied skill(s) to .claude/skills/"
	rm -rf .agents/skills
	mkdir -p .agents/skills
	cp -R skills/. .agents/skills/
	if [ -d optional_skills ]; then cp -R optional_skills/. .agents/skills/; fi
	@echo "Copied skill(s) to .agents/skills/"

# --- Docker ---
# Build the service image(s) defined in docker-compose.yml.
build:
	docker compose build

# Build (if needed) and run the stack in the foreground; Ctrl+C to stop.
# Requires the Gemini service-account JSON in ./credentials.
run:
	docker compose up --build

# Stop and remove the running containers.
down:
	docker compose down

logs:
	docker compose logs -f
