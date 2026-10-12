#!/usr/bin/env python3
"""PA Collab Hub — zero-dependency shared server for the DGPA PA network.
Serves index.html and a tiny JSON API. Last-write-wins per faculty profile.

Usage: python3 server.py [--host 0.0.0.0] [--port 8000]
"""
import argparse, json, threading
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse

BASE = Path(__file__).resolve().parent
DATA = BASE / "data.json"
LOCK = threading.Lock()

def load():
    with LOCK:
        return json.loads(DATA.read_text(encoding="utf-8"))

def save(d):
    with LOCK:
        DATA.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")

class H(SimpleHTTPRequestHandler):
    def log_message(self, *a):  # quiet
        pass

    def _json(self, obj, code=200):
        b = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        p = urlparse(self.path).path
        if p == "/api/data":
            self._json(load())
        elif p in ("/", "/index.html"):
            self.path = "/index.html"
            super().do_GET()
        else:
            super().do_GET()

    def do_POST(self):
        p = urlparse(self.path).path
        try:
            body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))).decode("utf-8"))
        except Exception:
            return self._json({"ok": False, "error": "bad json"}, 400)
        d = load()
        if p == "/api/profile":
            name = body.get("name")
            prof = body.get("profile")
            if name not in d.get("faculty", {}) or not isinstance(prof, dict):
                return self._json({"ok": False, "error": "unknown faculty"}, 404)
            allowed = {"themes", "methods", "regions", "interests", "domain"}
            d["faculty"][name] = {k: prof[k] for k in allowed if k in prof} | {
                "rank": d["faculty"][name]["rank"], "sig": d["faculty"][name].get("sig", "")}
            nl = body.get("new_labels") or {}
            for dim in ("themes", "methods", "regions"):
                if isinstance(nl.get(dim), dict):
                    d[dim].update({str(k): str(v) for k, v in nl[dim].items()})
            d.setdefault("changelog", []).append({"at": body.get("at", ""), "who": name, "what": "profile"})
            save(d)
            return self._json({"ok": True})
        if p == "/api/signature":
            if not isinstance(body.get("pinned"), list):
                return self._json({"ok": False, "error": "bad payload"}, 400)
            d["signature"] = {"pinned": body["pinned"], "updated_by": body.get("who", ""),
                              "updated_at": body.get("at", "")}
            save(d)
            return self._json({"ok": True})
        self._json({"ok": False, "error": "unknown route"}, 404)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="0.0.0.0")
    ap.add_argument("--port", type=int, default=8000)
    a = ap.parse_args()
    import os
    os.chdir(BASE)
    print(f"PA Collab Hub → http://{a.host}:{a.port}  (share http://<this-machine-ip>:{a.port} on the LAN)")
    ThreadingHTTPServer((a.host, a.port), H).serve_forever()
