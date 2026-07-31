#!/usr/bin/env python3
"""Extract ChatGPT session token from Brave cookies and use scrapling to send work for analysis."""

import os
import sqlite3
import shutil
import tempfile
import json
import subprocess
from pathlib import Path

# Brave cookie database path
brave_cookies = Path.home() / "AppData/Local/BraveSoftware/Brave-Browser/User Data/Default/Network/Cookies"
brave_local_state = Path.home() / "AppData/Local/BraveSoftware/Brave-Browser/User Data/Local State"

print(f"Cookie DB exists: {brave_cookies.exists()} ({brave_cookies.stat().st_size if brave_cookies.exists() else 0} bytes)")
print(f"Local State exists: {brave_local_state.exists()} ({brave_local_state.stat().st_size if brave_local_state.exists() else 0} bytes)")

# Try to copy the cookie DB (it might be locked by Brave)
tmp_dir = tempfile.mkdtemp()
tmp_cookies = os.path.join(tmp_dir, "Cookies")

try:
    shutil.copy2(str(brave_cookies), tmp_cookies)
    print(f"Copied cookie DB to {tmp_cookies}")
    
    # Read the cookie DB
    conn = sqlite3.connect(tmp_cookies)
    cursor = conn.cursor()
    
    # List ChatGPT-related cookies
    cursor.execute("SELECT host_key, name, value, encrypted_value, path, is_secure, is_httponly FROM cookies WHERE host_key LIKE '%chatgpt%' OR host_key LIKE '%openai%'")
    rows = cursor.fetchall()
    print(f"\nFound {len(rows)} ChatGPT/OpenAI cookies:")
    
    for row in rows:
        host_key, name, value, encrypted_value, path, is_secure, is_httponly = row
        val_preview = value[:50] if value else f"[encrypted: {len(encrypted_value)} bytes]"
        print(f"  {host_key} | {name} = {val_preview}")
    
    conn.close()
except Exception as e:
    print(f"Error: {e}")
finally:
    shutil.rmtree(tmp_dir, ignore_errors=True)
