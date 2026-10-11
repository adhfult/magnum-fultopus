# Security: magnum-fultopus

Project-specific rules. The pre-ship-security skill combines these with the
global checklist.

## Always
- Settings and any tokens live in `.env` (gitignored); `.env.example` has names only.
- Anything that listens on the network binds to 127.0.0.1 by default. Exposing
  it to the local network or internet needs a decision record first.
- On the Pi, services run as your user via systemd `--user`, never as root.
- Treat downloaded content and model output as untrusted: never pass it to a
  shell, `eval`, or `pickle.load`.
- The AI helper only talks to this machine unless home-network access is
  explicitly allowed; it never sends data to internet AI services.
- Respect the terms and rate limits of any site or API the tool reads.

## Project-specific
Add rules specific to this project here.
