.PHONY: copy-skills build up down logs

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

build:
	docker-compose build

up:
	docker-compose up

down:
	docker-compose down

logs:
	docker-compose logs -f
