# Set up your learning lab

Dev Opps is a guided course and a record of your evidence. The page does not execute commands. You read a lesson here, run its commands in your own disposable lab, compare the result, and save what you learned. Start at week 1; the architecture map and numbered journey are shortcuts to the same lessons.

## The weekly loop

1. **Understand:** read the concepts and explain one example aloud.
2. **Build:** run one command block at a time. Read what each part does before running it. Stop when the expected result differs.
3. **Diagnose:** introduce the named fault only inside your lab. Record a hypothesis before opening the hint. The recovery is in an expandable answer.
4. **Practice:** do the independent exercise. Every fourth week integrates that level into a capstone with acceptance checks.
5. **Prove:** explain the result and recovery without merely repeating the commands. Save your evidence and mark the week Proved when its checks pass.

Two hours a day is a planning guide. A useful session is 20 minutes understanding, 60 minutes building, 25 minutes testing or diagnosing, and 15 minutes writing evidence. Split long steps across sessions. Repeating a difficult week is expected; the calendar is not a certification.

## Choose the machine you will learn on

The commands use **Ubuntu 24.04 LTS and Bash**. Bash is the shell inside the Ubuntu terminal. Windows PowerShell is used only for the Windows installation steps below. Do not paste Bash commands into PowerShell or vice versa.

A disposable Linux virtual machine is the most consistent route for service management. WSL2 on Windows is convenient for the early lessons. Docker later needs a working Linux container engine. No cloud account is required for the free learning track, including the later cloud-concept lessons. Each affected lesson has a Free local practice route; provider execution is an optional separate exercise.

Use a machine with room for the operating system, container images and database volumes. Check storage before installing. Keep course downloads on a drive with sufficient space; never fill the operating-system drive to complete a lab. The course website can live on D: while the Linux working directory lives inside your Ubuntu home directory.

## Windows: install or inspect WSL2

Open PowerShell. First inspect what is already installed:

```powershell
wsl --status
wsl --list --verbose
```

`wsl --status` reports the WSL configuration. `--list --verbose` lists installed distributions and whether each uses version 1 or 2. An existing Ubuntu 24.04 distribution with version 2 can be reused if it is your own learning environment. Do not unregister a distribution to start this course: unregistering deletes its data.

If WSL or Ubuntu 24.04 is missing, open PowerShell as Administrator and run:

```powershell
wsl --install -d Ubuntu-24.04
```

`--install` installs the required Windows components and the requested Linux distribution; `-d` names that distribution. Follow the Windows prompt to restart if required. Open Ubuntu from the Start menu and create a normal Linux username and password. The password prompt intentionally shows no characters while typing. Administrator approval is for installing the environment, not for every course command.

If installation cannot enable virtualization on this computer, use an Ubuntu VM or a Linux computer you control. WSL setup depends on Windows edition, updates and virtualization support; an install error is an environment issue to resolve before the lesson, not a reason to rewrite the commands.

## Linux: install the initial tools

The following blocks run **inside Ubuntu Bash**. First confirm the operating system:

```bash
cat /etc/os-release
uname -r
```

`cat` prints Ubuntu's release metadata. `uname -r` prints the running kernel version. Record both. A WSL kernel will identify itself differently from a normal VM kernel; that distinction matters when you reach systemd and networking.

Install the first-level tools:

```bash
sudo apt-get update
sudo apt-get install -y git curl python3 python3-venv python3-pip iproute2 procps dnsutils openssl ca-certificates
```

`sudo` runs this one package-management command with administrator privileges. `apt-get update` refreshes the package catalog; it does not upgrade all installed packages. `apt-get install` installs the named packages; `-y` accepts its installation prompt. Read the package list and required storage first if your lab is constrained, and omit `-y` to review interactively.

Git records changes. curl makes HTTP requests. Python and its venv module run isolated application environments. iproute2 supplies `ip` and `ss` for routes and sockets. procps supplies `ps` and `free` for process and memory inspection. dnsutils supplies `dig`. OpenSSL and certificate authorities support TLS inspection and verification.

Check the installation:

```bash
python3 --version
git --version
curl --version
ss --version
dig -v
```

Each command prints the installed version. You should have Python 3.12 or newer for the included Taskboard lab. If a command is missing, read the package install error and check network connectivity and available disk space. Do not use a random install script from a search result.

## Download the course lab files

[Download the Dev Opps lab files](../downloads/dev-opps-labs.zip) and extract the archive into a directory you control. It contains `labs/taskboard` and `labs/delivery`. Keep that directory available: week 3 asks for its location and copies the starter into your Linux learning workspace. You can inspect the included README before copying anything. The archive contains source and dependency lists; it does not include installed dependencies or credentials.

When following the public website, download these files once before week 3. When using the full offline course archive, the same `labs` directory is already included. Extract the archive first rather than opening files inside the compressed folder.

## Terminal basics before the first command

A shell prompt often ends with `$`. It is not part of the command: the course blocks intentionally omit it. Commands are case-sensitive. Copy one complete block, including any closing `EOF` or `PY` line. Those markers finish a here-document: text that the shell passes to a file-writing command or Python program.

`Ctrl+C` interrupts the foreground program in that terminal. A server usually keeps running until interrupted; a terminal that is waiting for requests is not broken. Keep a second Ubuntu terminal open to inspect the server. `exit` closes a shell session after you have stopped the programs you own.

`~` means your Linux home directory. A relative path is interpreted from your current directory, which `pwd` prints. Commands starting with `cd ~/dev-opps-lab` establish the course workspace explicitly. Keep Linux source files inside the Linux filesystem when using WSL, rather than assuming `C:\...` is a Bash path.

The course will ask you for the extracted course directory when it copies the included Taskboard assets in week 3. In WSL, a Windows D: directory is usually accessible under `/mnt/d/`. Enter your actual location when prompted; the lessons do not assume another person's Windows username.

## What stays on your machine

The website stores progress in this browser's local storage. It does not upload your terminal output or execute your lab. Use **Progress and backup** to export progress regularly. Clearing browser storage or switching browser origins can make the local record unavailable until you import a backup. Save evidence files in your lab Git repository as well.

Use synthetic tasks and lab identities. Never put tokens, private keys, real customer data or cloud credentials in evidence notes, screenshots, commits or public course contributions. Before public exposure, the later lessons require a reviewed real identity integration; the included teaching tokens are for a private lab only.

## Get unstuck without guessing

1. Record the working directory, exact command, exit status and relevant diagnostic. Redact credentials.
2. Compare the expected result in the lesson. Is the tool absent, the process absent, the port wrong, the dependency unavailable, or the response incorrect?
3. Open the diagnostic hint. Inspect the named evidence before making a change.
4. Make one scoped change. Repeat the same verification so the result is comparable.
5. Write why the evidence supports the recovery. A restart that happens to work is not yet an explanation.

## Source references

- [Microsoft: install WSL](https://learn.microsoft.com/en-us/windows/wsl/install) — installation commands and requirements.
- [Ubuntu command-line introduction](https://ubuntu.com/tutorials/command-line-for-beginners) — terminal, paths and command structure.
- [Python virtual environments](https://docs.python.org/3/library/venv.html) — isolating project dependencies from the operating system.

Continue with week 1 from the study plan. You will create the workspace there, so no project files need to exist yet.

For the full route, see [Learn without a cloud bill](free-learning.md).
