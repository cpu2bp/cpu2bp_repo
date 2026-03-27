To properly run server_start.py on remote PC, open power Shell in !!!ADMINISTRATOR!!! mode and execute the following:

New-NetFirewallRule -DisplayName "Flask Server Port 5000" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 5000