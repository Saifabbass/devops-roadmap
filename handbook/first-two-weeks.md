# First two weeks: explain, break and repair a small service

This is an optional pacing companion. The guided weekly lessons are the primary teaching route and contain the complete explanations, expected results, controlled faults and answers. Use [lab setup](lab-setup.md) first. Follow this alongside [curriculum week 1](../index.html#week-1), [week 2](../index.html#week-2) and the [engineering handbook](engineering-handbook.md). There are **14 sessions of two hours**: seven sessions per week, totaling 14 hours weekly.

Every session uses **15 minutes retrieval → 25 minutes learning → 65 minutes lab → 15 minutes evidence**. During retrieval, answer the session's question before reading. During learning, read the relevant linked documentation, then predict what the lab will show. Keep evidence under your dedicated lab directory: command, observation, explanation, failed hypothesis and recovery check. Save concise notes, not an indiscriminate terminal dump.

You may skip familiar explanation only by demonstrating the session's outcome without instructions and recording the evidence. Spend the recovered time on the variation or failure case. A remembered command is not proof.

## Before session 1: choose the right shell

All blocks below are **Linux Bash**, except this optional Windows preflight:

```powershell
wsl --status
wsl --list --verbose
```

Use an existing WSL Linux distribution or a disposable Linux VM. If WSL is absent, follow [Microsoft's installation instructions](https://learn.microsoft.com/en-us/windows/wsl/install); installation can require administrator access and a restart. Nothing has been installed or executed for you by this guide.

Use a normal, non-root Linux account. Required tools are Python 3.12+, Git 2.28+, curl, OpenSSL 3+, `ss`, `ip`, `getent` and standard Linux utilities. Check availability; use your distribution's package documentation for anything missing. Do not improvise installer scripts. If setup consumes the session, repeat session 1 after resolving it.

The HTTP server is a disposable teaching tool, not a production server. Serve only the new `site` directory, with no secrets or symbolic links. Bind to `127.0.0.1`. Stop servers with **Ctrl-C in their own terminal**. Keep the lab files for evidence; no recursive cleanup is necessary. [Python HTTP server documentation](https://docs.python.org/3/library/http.server.html).

Run session 1's directory setup once. On later days, restore the saved export lines and restart the current server in terminal A when needed. Use terminal B in the same Linux distribution for investigation. Session 11 deliberately replaces the plain HTTP server with the TLS server on the same port.

## Session 1 — Establish a known working service

**Retrieve:** What distinguishes a program, a process and a listening service?

Check tools, then create an isolated workspace:

```bash
command -v python3 git curl openssl ss ip getent
python3 --version
git --version
openssl version
export LAB_DIR="$(mktemp -d "$HOME/devops-foundations.XXXXXX")"
export LAB_PORT=8765
mkdir "$LAB_DIR/site" "$LAB_DIR/evidence"
printf '<h1>Taskboard lab: ready</h1>\n' > "$LAB_DIR/site/index.html"
printf 'export LAB_DIR=%q\nexport LAB_PORT=%q\n' "$LAB_DIR" "$LAB_PORT"
ss -ltn "sport = :$LAB_PORT"
```

Copy the printed export lines into your notes and every new lab terminal. If the port already has a listener, choose another unused high port and update `LAB_PORT` in every terminal; leave the existing process alone.

In terminal A, start:

```bash
python3 -m http.server "$LAB_PORT" --bind 127.0.0.1 --directory "$LAB_DIR/site"
```

In terminal B:

```bash
curl --noproxy '*' --max-time 5 -i "http://127.0.0.1:$LAB_PORT/"
```

**Evidence:** directory path, tool versions, HTTP 200, expected body and matching server log. Explain why terminal A remains occupied. End with Ctrl-C.

## Session 2 — Identify the process and its parent

**Retrieve:** Which process owns yesterday's listener?

Restart the server in A. In B:

```bash
ss -ltnp "sport = :$LAB_PORT"
ps -u "$USER" -o pid,ppid,stat,etime,args
```

Find the matching server PID, then set `SERVER_PID` to that observed number:

```bash
read -r -p "Observed server PID: " SERVER_PID
ps -p "$SERVER_PID" -o pid,ppid,user,stat,etime,args
readlink "/proc/$SERVER_PID/cwd"
```

Explain PID versus parent PID, elapsed time versus CPU time, and working directory versus the explicit served directory. Inspect only this process; environment variables of unrelated processes can contain secrets. Use the [kernel's `/proc` reference](https://www.kernel.org/doc/html/latest/filesystems/proc.html) to interpret the filesystem view.

**Evidence:** a shell → Python process diagram. Stop and restart A; show that the service can have the same address but a different PID.

## Session 3 — Diagnose a port collision

**Retrieve:** Can two unrelated servers bind the same address and port?

Keep A running. In B, attempt the same server command from session 1. The second process should fail with an address-in-use error. Confirm the first server still responds, then inspect its listener.

Do not solve this by killing every Python process. Identify the existing owner, return to A and stop your known server. Retry the command in B; it should now start. Use A as the investigating terminal if needed.

**Evidence:** the failed startup, the unchanged original endpoint and the successful retry. Explain the difference between process startup failure and an HTTP error returned by a running process. Draw which terminal currently owns the server.

## Session 4 — Separate HTTP status from command success

**Retrieve:** Does a completed network request imply the requested page exists?

With the server running:

```bash
curl --noproxy '*' --max-time 5 -sS -o /dev/null \
  -w 'http=%{http_code}\n' "http://127.0.0.1:$LAB_PORT/missing"
printf 'curl_exit=%s\n' "$?"
curl --noproxy '*' --max-time 5 -fsS -o /dev/null \
  "http://127.0.0.1:$LAB_PORT/missing"
printf 'curl_exit=%s\n' "$?"
```

The first transfer normally exits successfully despite HTTP 404; `--fail` makes the second report failure. Capture `$?` immediately. Compare both requests with A's log and the successful root path. Consult the [curl manual](https://curl.se/docs/manpage.html) for the options you used.

**Evidence:** a table of path, HTTP status, client exit status and server log. Write the condition a future CI smoke test should actually assert.

## Session 5 — Diagnose a filesystem permission failure

**Retrieve:** Under which user's permissions does the server read a file?

Create only a disposable file:

```bash
printf 'disposable permission exercise\n' > "$LAB_DIR/site/restricted.txt"
stat -c '%A %U %G %n' "$LAB_DIR/site/restricted.txt"
chmod 000 "$LAB_DIR/site/restricted.txt"
curl --noproxy '*' --max-time 5 -i \
  "http://127.0.0.1:$LAB_PORT/restricted.txt"
chmod 600 "$LAB_DIR/site/restricted.txt"
curl --noproxy '*' --max-time 5 -i \
  "http://127.0.0.1:$LAB_PORT/restricted.txt"
```

Run as a normal user: root can invalidate this exercise. Observe the actual error rather than assuming every permission failure becomes HTTP 403. Explain why owner-only read permission works when the server is that owner.

**Evidence:** before/after permissions and responses. Record the smallest required permission change; never use broad recursive permissions as a repair.

## Session 6 — Use Git to explain and reverse a change

**Retrieve:** How do the working tree, index and commit differ?

Create a separate training repository. The identity below applies only there and is explicitly a lab identity:

```bash
git init -b main "$LAB_DIR/repo"
git -C "$LAB_DIR/repo" config user.name "DevOps Lab"
git -C "$LAB_DIR/repo" config user.email "lab@example.invalid"
cp "$LAB_DIR/site/index.html" "$LAB_DIR/repo/index.html"
git -C "$LAB_DIR/repo" add index.html
git -C "$LAB_DIR/repo" commit -m "Record working response"
git -C "$LAB_DIR/repo" switch -c lab-response
printf '<h1>Wrong deployment</h1>\n' > "$LAB_DIR/repo/index.html"
git -C "$LAB_DIR/repo" diff
git -C "$LAB_DIR/repo" add index.html
git -C "$LAB_DIR/repo" diff --cached
git -C "$LAB_DIR/repo" commit -m "Introduce lab regression"
git -C "$LAB_DIR/repo" revert --no-edit HEAD
git -C "$LAB_DIR/repo" log --oneline -3
```

Copy the recovered file to `site/index.html` and verify its response. Read [Git revert](https://git-scm.com/docs/git-revert).

**Evidence:** three commits and a verified recovery. Explain why a history-preserving revert suits a shared repository.

## Session 7 — Week 1 practical gate

**Retrieve:** Explain the service from disk to process to socket to response.

Without copying earlier commands, reproduce and diagnose these faults one at a time: stopped server, occupied port and unreadable disposable file. Restore a working response after each. Use your notes only after recording where recall failed.

Write a one-page runbook containing startup, expected listener, response check, log location, controlled shutdown and restart. Include a decision tree that starts from evidence rather than “restart everything.”

**Pass evidence:** correct PID and served directory, proven loopback binding, three diagnosed faults and verified recoveries. Finish a short Git change-and-revert exercise. Missing any outcome means repeating that portion before marking [week 1](../index.html#week-1) complete.

## Session 8 — Name resolution is a separate boundary

**Retrieve:** Does knowing a hostname prove an application is reachable?

```bash
getent ahosts localhost
getent ahosts example.com
getent ahosts no-such-name.invalid
```

Record actual answers; public addresses can change. `getent` uses the system's configured name-service lookup, so a result may come from local configuration rather than a fresh DNS exchange.

Inspect your lab network without changing it:

```bash
ip address show
ip route show
```

Identify the loopback address, the interface used for ordinary traffic and the default route, if one exists. Explain that a more specific matching route wins over a default route. For a paper exercise, `10.20.30.0/24` contains 256 IPv4 addresses because 8 bits remain for the host portion. In a conventional subnet, the network and broadcast addresses are not ordinary host addresses; cloud providers can reserve additional addresses. Do not treat this calculation as permission to scan that range. Draw which next hop your machine would use for an address outside its directly connected subnet.

With your local server running, override resolution for this request only:

```bash
curl --noproxy '*' --max-time 5 \
  --resolve "taskboard.test:$LAB_PORT:127.0.0.1" \
  "http://taskboard.test:$LAB_PORT/"
```

**Evidence:** explain why this works without changing `/etc/hosts` or publishing DNS. Draw hostname → address → route → port, explain the `/24` example, and name what remains untested about public DNS.

## Session 9 — Read the HTTP exchange

**Retrieve:** Which parts of the URL become request information?

```bash
curl --noproxy '*' --max-time 5 -v "http://127.0.0.1:$LAB_PORT/"
curl --noproxy '*' --max-time 5 -I "http://127.0.0.1:$LAB_PORT/"
curl --noproxy '*' --max-time 5 -i "http://127.0.0.1:$LAB_PORT/not-here"
```

Locate method, path, Host header, response status, content type and body. Compare GET with HEAD. Do not assume a header proves the application's business behavior is correct.

Change the disposable index page to say “wrong result” and observe that it can still return 200. Restore it from your lab Git repository.

**Evidence:** annotate one exchange and write two assertions: expected status and expected content. Explain why both matter for Taskboard.

## Session 10 — Identify where a request failed

**Retrieve:** What evidence separates name failure, connection failure and HTTP failure?

Create a failure matrix using the nonexistent `.invalid` name, your stopped local server and the running server's missing path. Bound each request with a five-second timeout. Do not scan arbitrary ports.

Measure a successful local request:

```bash
curl --noproxy '*' --max-time 5 -sS -o /dev/null \
  -w 'dns=%{time_namelookup} connect=%{time_connect} first_byte=%{time_starttransfer} total=%{time_total}\n' \
  "http://127.0.0.1:$LAB_PORT/"
```

These times are cumulative milestones, not four independent durations. A numeric loopback address does not meaningfully benchmark DNS.

**Evidence:** request, last successful layer, observed error and next diagnostic check. Explain why connection refusal and waiting until timeout suggest different possibilities.

## Session 11 — Create a local TLS experiment

**Retrieve:** What does encryption alone fail to establish about a server?

Create an unencrypted **lab-only** private key in a private directory outside the served files. Do not upload or commit it:

```bash
mkdir -m 700 "$LAB_DIR/tls"
(
  umask 077
  openssl req -x509 -newkey rsa:2048 -sha256 -days 7 -noenc \
    -keyout "$LAB_DIR/tls/key.pem" -out "$LAB_DIR/tls/cert.pem" \
    -subj '/CN=localhost' -addext 'subjectAltName=DNS:localhost'
)
```

Read the [OpenSSL certificate-generation options](https://docs.openssl.org/3.5/man1/openssl-req/). Stop the HTTP server. Save this reviewed code as `$LAB_DIR/tls_server.py` using your editor:

```python
import os
import ssl
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

root = Path(os.environ["LAB_DIR"])
handler = partial(SimpleHTTPRequestHandler, directory=str(root / "site"))
server = ThreadingHTTPServer(("127.0.0.1", int(os.environ["LAB_PORT"])), handler)
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(root / "tls/cert.pem", root / "tls/key.pem")
server.socket = context.wrap_socket(server.socket, server_side=True)
try:
    server.serve_forever()
except KeyboardInterrupt:
    pass
finally:
    server.server_close()
```

Start it in A with `python3 "$LAB_DIR/tls_server.py"`. Explain each responsibility before execution. [Python TLS documentation](https://docs.python.org/3/library/ssl.html).

**Evidence:** certificate versus private-key roles, private file location and loopback listener.

## Session 12 — Separate certificate trust from hostname identity

**Retrieve:** Why should a self-signed endpoint fail normal verification?

```bash
curl --noproxy '*' --max-time 5 "https://localhost:$LAB_PORT/"
curl --noproxy '*' --max-time 5 --cacert "$LAB_DIR/tls/cert.pem" \
  --resolve "localhost:$LAB_PORT:127.0.0.1" "https://localhost:$LAB_PORT/"
curl --noproxy '*' --max-time 5 --cacert "$LAB_DIR/tls/cert.pem" \
  "https://127.0.0.1:$LAB_PORT/"
```

The second request should succeed. The last should fail hostname verification: the certificate names `localhost`, not the IP address. Record actual diagnostics. Do not disable verification or install this certificate into a system trust store.

**Evidence:** three outcomes with distinct explanations. If the certificate has expired when revisiting, generate a fresh pair in a new private lab directory and explicitly update the server paths.

## Session 13 — Trace the entire HTTPS path

**Retrieve:** Put resolution, TCP, TLS and HTTP in order.

```bash
openssl x509 -in "$LAB_DIR/tls/cert.pem" -noout -subject -issuer -dates
openssl s_client -connect "127.0.0.1:$LAB_PORT" \
  -servername localhost -verify_hostname localhost -verify_return_error \
  -CAfile "$LAB_DIR/tls/cert.pem" </dev/null
```

Explain the address used to connect, server-name indication, hostname verification and the explicitly trusted certificate. Then request a nonexistent path over correctly verified TLS. A TLS success can still be followed by HTTP 404. [OpenSSL TLS client reference](https://docs.openssl.org/3.5/man1/openssl-s_client/).

**Evidence:** one layered diagram, including which step produced each observed failure. Explain which parts would move to a load balancer in a cloud deployment.

## Session 14 — Week 2 practical gate

**Retrieve:** Diagnose “the website is down” without assuming the failing layer.

Use only your runbook to diagnose five isolated cases: stopped server, wrong served content, missing path, untrusted certificate and hostname mismatch. Predict the outcome before each experiment. Keep the endpoint local and change one condition at a time.

For every case, record the first discriminating check, observed evidence, explanation, smallest repair and recovery assertion. Explain what your experiment cannot prove about production DNS, internet routing, certificate renewal or application authorization.

**Pass evidence:** five correct diagnoses, a complete request-path explanation and a runbook another learner can follow. Mark [week 2](../index.html#week-2) complete only after reproducing these outcomes. Stop the known server with Ctrl-C and confirm its listener disappeared. Keep the evidence; cloud accounts and Kubernetes can wait until these boundaries are clear.
