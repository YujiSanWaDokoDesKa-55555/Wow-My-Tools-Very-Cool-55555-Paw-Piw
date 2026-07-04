P = \033[1;37m
H = \033[1;32m
M = \033[1;31m
K = \033[1;33m
B = \033[1;34m
U = \033[1;35m
C = \033[1;36m
R = \033[0m

TERMUX_PATH := /data/data/com.termux/files/usr/bin/bash

detectCLI:
	@echo "$(P)[$(H)?$(P)]$(R) Mengecek lingkungan$(M)...$(R)"
	@if [ -f "$(TERMUX_PATH)" ]; then \
		echo "$(P)[$(H)✓$(P)]$(R) Termux terdeteksi!"; \
		OS_TYPE="termux"; \
	elif [ -f "/etc/debian_version" ]; then \
		grep -qi ubuntu /etc/os-release && OS_TYPE="ubuntu" || OS_TYPE="debian"; \
		echo "$(P)[$(H)✓$(P)]$(R) $$OS_TYPE terdeteksi!"; \
	else \
		echo "$(P)[$(M)!$(P)]$(R) OS tidak didukung!"; \
		exit 1; \
	fi; \
	echo $$OS_TYPE > .os_type

run:
	@python cl.py

fix: detectCLI
	@OS_TYPE=$$(cat .os_type); \
	if [ "$$OS_TYPE" = "termux" ]; then \
		pip uninstall requests -y; \
		pip uninstall psutil -y; \
		pip install requests; \
		pip install "urllib3<2"; \
		bash python313.sh; \
	else \
		. venv/bin/activate && \
		pip uninstall requests -y && \
		pip uninstall psutil -y && \
		pip install requests && \
		pip install "urllib3<2"; \
	fi