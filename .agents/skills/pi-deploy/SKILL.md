---
name: pi-deploy
description: Deploy or update this project on the Raspberry Pi so it runs automatically. Use when the user wants to run the tool on the Pi, run it on a schedule, keep it running in the background, or check why it stopped, including "put this on the Pi", "run this every hour", "make it start automatically", or "check the Pi logs".
---

# Deploying to the Raspberry Pi

The Pi runs the tool from its own clone of the repo, managed by systemd as the
user (no root). Code moves PC -> GitHub -> Pi, never by copying files.

## First deploy
1. On the PC: tests and ruff pass, changes are committed and pushed.
2. On the Pi (the user runs these, or you run them if this session is on the Pi):
   ```bash
   cd ~/code && gh repo clone magnum-fultopus && cd magnum-fultopus
   uv sync
   cp .env.example .env   # then edit values for the Pi if needed
   uv run app status      # confirm it works before scheduling it
   ```
3. Adjust `deploy/pi/magnum-fultopus.service` (`ExecStart`) and `.timer`
   (`OnCalendar`) for what should run and how often. For something that runs
   continuously instead of on a schedule, use `Type=simple`, add
   `Restart=on-failure`, and enable the .service without the .timer.
4. Install and start:
   ```bash
   mkdir -p ~/.config/systemd/user
   cp deploy/pi/magnum-fultopus.service deploy/pi/magnum-fultopus.timer ~/.config/systemd/user/
   systemctl --user daemon-reload
   systemctl --user enable --now magnum-fultopus.timer
   ```
5. So it keeps running when nobody is logged in, the user runs
   `loginctl enable-linger "$USER"` once (it may ask for their password).

## Updating
```bash
cd ~/code/magnum-fultopus && git pull && uv sync
systemctl --user daemon-reload   # only if files in deploy/pi/ changed; re-copy them first
```

## Checking on it
- Status: `systemctl --user status magnum-fultopus.timer magnum-fultopus.service`
- Logs: `journalctl --user -u magnum-fultopus -n 50 --no-pager`
- Next run: `systemctl --user list-timers`

## Pi constraints
- 64-bit ARM: prefer pure-Python packages or ones that publish arm64 wheels;
  building from source on the Pi is slow and may fail.
- Limited RAM: the Pi 400 has 4 GB. Avoid loading large files or models all at
  once. Only tiny local models (about 1.7B) fit; for anything bigger, borrow a
  PC's model with `local-ai-profile.sh --remote <PC address>`.
- Keep secrets in the Pi's own `.env`, never in the repo.
