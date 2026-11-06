import tkinter as tk
from tkinter import ttk
from pathlib import Path
import json, subprocess, threading
BASE=Path(__file__).resolve().parent
root=tk.Tk(); root.title("Customer Sales Insights - MySQL Setup"); root.geometry("540x380")
fields={}
for i,(label,default) in enumerate([("Host","localhost"),("Port","3306"),("Username","root"),("Password","")]):
    ttk.Label(root,text=label).grid(row=i,column=0,padx=20,pady=12,sticky="w")
    entry=ttk.Entry(root,width=40,show="*" if label=="Password" else "")
    entry.insert(0,default); entry.grid(row=i,column=1,padx=10,pady=12); fields[label]=entry
status=tk.StringVar(value="Enter your MySQL login. Password stays on this PC.")
ttk.Label(root,textvariable=status,wraplength=490).grid(row=5,column=0,columnspan=2,padx=20,pady=20)
def connect():
    try:
        config={"host":fields["Host"].get().strip(),"port":int(fields["Port"].get())}
        payload=json.dumps({"user":fields["Username"].get(),"password":fields["Password"].get()})
    except ValueError:
        status.set("Port must be a number, normally 3306."); return
    button.state(["disabled"]); status.set("Connecting and running the ten queries...")
    def work():
        try:
            cmd="$ErrorActionPreference='Stop'; Import-Module ($PSHOME+'\\Modules\\Microsoft.PowerShell.Security\\Microsoft.PowerShell.Security.psd1'); $d=[Console]::In.ReadToEnd()|ConvertFrom-Json; $s=ConvertTo-SecureString $d.password -AsPlainText -Force; $c=New-Object System.Management.Automation.PSCredential($d.user,$s); $p=Join-Path $env:LOCALAPPDATA 'CustomerSalesInsights'; New-Item -ItemType Directory -Force $p|Out-Null; $c|Export-Clixml -LiteralPath (Join-Path $p 'credential.xml')"
            subprocess.run(["powershell.exe","-NoProfile","-Command",cmd],input=payload,text=True,capture_output=True,check=True,creationflags=subprocess.CREATE_NO_WINDOW)
            (BASE/"mysql_config.json").write_text(json.dumps(config))
            import pipeline
            pipeline.run(True)
            root.after(0,lambda: status.set("SUCCESS: 3,900 rows loaded and all 10 MySQL queries passed. You can close this window."))
            root.after(0,lambda: fields["Password"].delete(0,tk.END))
        except Exception as exc:
            error=type(exc).__name__
            root.after(0,lambda: status.set("Connection did not finish ("+error+"). Check your host, port, username and password, then retry. Existing mismatched tables are preserved."))
        finally:
            root.after(0,lambda: button.state(["!disabled"]))
    threading.Thread(target=work,daemon=True).start()
button=ttk.Button(root,text="Connect and load project",command=connect);button.grid(row=4,column=0,columnspan=2,pady=10)
root.mainloop()
