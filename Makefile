.PHONY: demo demo-snapshot demo-build demo-preview demo-preview-build dashboard-build

# Build the GitHub Pages demo bundle and stage it under docs/, then restore
# plugin/dashboard/dist/ to the live (non-demo) build so the plugin's shipped
# bundle stays correct for users running /pm-job-search:dashboard locally.
# After `git push`: https://archugunov.github.io/pm-job-search/
demo: demo-snapshot demo-build
	rsync -a --delete --exclude='superpowers/' plugin/dashboard/dist/ docs/
	./scripts/check_demo_privacy.sh docs/
	$(MAKE) dashboard-build

# Restore plugin/dashboard/dist/ to the live build (no demo flags, base "/")
# that the plugin ships with for end users.
dashboard-build:
	rm -rf plugin/dashboard/public/demo/
	cd plugin/dashboard && npm run build
	# Strip demo-only assets that Vite copied from public/ — the live plugin
	# bundle never renders MobileLanding, so the mp4 would be dead weight
	# shipped to every user who installs the plugin.
	rm -f plugin/dashboard/dist/dashboard-demo.mp4

# Snapshot the Maya example into public/demo/ for Vite to pick up.
demo-snapshot:
	python3 plugin/dashboard/scripts/snapshot_demo.py \
		--persona maya \
		--out plugin/dashboard/public/demo/

# Build with the GitHub Pages subpath. Used by `make demo`.
demo-build:
	cd plugin/dashboard && VITE_DEMO_MODE=true VITE_BASE=/pm-job-search/ npm run build

# Build with base "/" for local smoke testing. Output: plugin/dashboard/dist/
demo-preview-build: demo-snapshot
	cd plugin/dashboard && VITE_DEMO_MODE=true VITE_BASE=/ npm run build

# Build + serve a local-base demo on http://localhost:8765 so you can verify
# the bundle without faking the GitHub Pages subpath.
demo-preview: demo-preview-build
	@echo "open http://localhost:8765"
	cd plugin/dashboard/dist && python3 -m http.server 8765
