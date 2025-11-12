
#!/usr/bin/env python3
import os
import shlex
import subprocess
import datetime
import uuid
from flask import Flask, request, jsonify, render_template, abort

app = Flask(__name__, template_folder='templates', static_folder='static')

# === CONFIG ===
# Set SIM_API_KEY env var or edit here. If empty string, auth is disabled for local testing.
API_KEY = os.environ.get("SIM_API_KEY", "letmein123")  # set to "" to disable authentication

# Prefer absolute nmap path if available
NMAP_PATH = "/usr/bin/nmap" if os.path.exists("/usr/bin/nmap") else "nmap"

# Helper runner
def run_cmd(cmd_list, timeout=60):
    """
    Run a command capturing stdout & stderr. Returns (rc, stdout, stderr, timed_out_bool)
    """
    try:
        proc = subprocess.run(
            cmd_list,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout
        )
        return proc.returncode, proc.stdout, proc.stderr, False
    except subprocess.TimeoutExpired:
        return -1, "", f"Command timed out after {timeout}s", True
    except Exception as e:
        return -1, "", f"Execution failed: {e}", False

# ---------- Routes ----------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    # If API_KEY is set (non-empty), require header
    if API_KEY:
        key = request.headers.get("X-API-Key", "")
        if key != API_KEY:
            return jsonify({"error": "Unauthorized"}), 401

    body = request.get_json(silent=True) or request.form or {}
    target = (body.get('ip') or body.get('target') or "").strip()
    if not target:
        return jsonify({"error": "missing_target"}), 400

    diagnostics = {"attempts": []}

    # First attempt: conservative top-ports scan
    cmd1 = [NMAP_PATH, "-sV", "--version-light", "--top-ports", "100", "--open", "--host-timeout", "45s", target]
    rc1, out1, err1, to1 = run_cmd(cmd1, timeout=50)
    diagnostics["attempts"].append({
        "cmd": " ".join(shlex.quote(p) for p in cmd1),
        "rc": rc1, "timed_out": bool(to1),
        "stdout": out1[:4000], "stderr": err1[:2000]
    })

    final_out = out1
    final_rc = rc1
    final_timed_out = to1

    # Fallback: try skipping host discovery if first yielded no result or timed out
    if to1 or (not out1.strip()):
        cmd2 = [NMAP_PATH, "-Pn", "-sV", "--version-light", "--top-ports", "100", "--open", "--host-timeout", "60s", target]
        rc2, out2, err2, to2 = run_cmd(cmd2, timeout=70)
        diagnostics["attempts"].append({
            "cmd": " ".join(shlex.quote(p) for p in cmd2),
            "rc": rc2, "timed_out": bool(to2),
            "stdout": out2[:4000], "stderr": err2[:2000]
        })
        # prefer cmd2 output if present
        if out2.strip():
            final_out = out2
            final_rc = rc2
            final_timed_out = to2

    # If still no output, try ping diagnostics
    if (not final_out.strip()) and not final_timed_out:
        ping_cmd = ["ping", "-c", "3", target]
        prc, pout, perr, pto = run_cmd(ping_cmd, timeout=12)
        diagnostics["ping"] = {
            "cmd": " ".join(shlex.quote(p) for p in ping_cmd),
            "rc": prc, "timed_out": bool(pto),
            "stdout": pout[:1000], "stderr": perr[:1000]
        }

    response = {
        "scan_id": str(uuid.uuid4())[:8],
        "target": target,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "scan_output": final_out,
        "rc": final_rc,
        "timed_out": bool(final_timed_out),
        "diagnostics": diagnostics
    }

    return jsonify(response)

@app.route('/exploit', methods=['POST'])
def exploit():
    # If API_KEY is set (non-empty), require header
    if API_KEY:
        key = request.headers.get("X-API-Key", "")
        if key != API_KEY:
            return jsonify({"error": "Unauthorized"}), 401

    body = request.get_json(silent=True) or request.form or {}
    target = (body.get('target') or body.get('ip') or "").strip()
    exploit_key = (body.get('exploit') or body.get('attack') or "simulated_exploit").strip()
    scan_output = body.get('scan_output') or ""

    if not target:
        return jsonify({"error": "missing_target"}), 400

    # build a simulated report (no real exploit)
    report_id = str(uuid.uuid4())[:8]
    ts = datetime.datetime.utcnow().isoformat() + "Z"

    # heuristic: mention vsftpd if scan output contains it
    low = (scan_output or "").lower()
    vuln_note = "No explicit vulnerability detected from scan output."
    if "vsftpd" in low or "ftp" in low:
        vuln_note = "Detected FTP service / vsftpd banner. Older vsftpd 2.3.4 is known to have a backdoor (simulated)."

    simulated_shell = (
        "Simulated shell>\n"
        "$ id\nuid=0(root) gid=0(root)\n"
        "$ hostname\nmetasploitable\n"
        "$ uname -a\nLinux metasploitable 2.6.24-16-server #1 SMP ...\n"
        "(Note: simulated output for demo only)\n"
    )

    report = {
        "id": report_id,
        "target": target,
        "exploit": exploit_key,
        "timestamp": ts,
        "scan_summary": (scan_output[:6000] + ("..." if len(scan_output) > 6000 else "")) if scan_output else "No scan output provided.",
        "vulnerability": vuln_note,
        "outputs": {"simulated_shell": simulated_shell},
        "risk_assessment": {"impact": "High (if real)", "likelihood": "Medium"},
        "recommendations": [
            "Patch or upgrade vulnerable services.",
            "Disable FTP if not required.",
            "Segment lab hosts from production networks.",
            "Use snapshots for rollbacks."
        ],
        "notes": "This is a simulated exploit/report for training. No real exploit executed."
    }

    return jsonify(report)

# simple health route
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "time": datetime.datetime.utcnow().isoformat() + "Z"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

