import paramiko
import sys

cmd = sys.argv[1] if len(sys.argv) > 1 else "hostname"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=10)

# Use bash -c with the command to preserve variable expansion
stdin, stdout, stderr = client.exec_command(f'bash -c "{cmd}"', timeout=60)
out = stdout.read().decode()
err = stderr.read().decode()
if out:
    print(out, end="")
if err:
    print(err, end="", file=sys.stderr)

client.close()
sys.exit(stdout.channel.recv_exit_status())
