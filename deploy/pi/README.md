# Running on the Raspberry Pi

These files run the tool automatically on the Pi with systemd (Linux's
built-in service manager), as your normal user, not root. The pi-deploy skill
walks through it; the short version:

```bash
# on the Pi, once
cd ~/code && gh repo clone magnum-fultopus && cd magnum-fultopus && uv sync
mkdir -p ~/.config/systemd/user
cp deploy/pi/magnum-fultopus.service deploy/pi/magnum-fultopus.timer ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now magnum-fultopus.timer
loginctl enable-linger "$USER"   # keep running when you're logged out (asks for your password)
```

- Runs `uv run app status` every hour by default. Change `ExecStart` in the
  .service file and `OnCalendar` in the .timer file.
- Logs: `journalctl --user -u magnum-fultopus -n 50`
- Stop: `systemctl --user disable --now magnum-fultopus.timer`
