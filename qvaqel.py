#!/data/data/com.termux/files/usr/bin/python3
# -*- coding: utf-8 -*-
# QVAQEL - Security Toolkit Menu for Termux v3.0
import os, sys, subprocess, shutil, re

QDIR = os.path.expanduser("~/qvaqel")
TOOLS = os.path.join(QDIR, "tools")
os.makedirs(TOOLS, exist_ok=True)

C0="\033[0m"; B1="\033[1;34m"; B2="\033[34m"; B3="\033[38;5;39m"
B4="\033[38;5;27m"; GR="\033[1;32m"; RD="\033[1;31m"; YL="\033[1;33m"

ansi_re = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
def vlen(s): return len(ansi_re.sub('', s))

def grad(text, c1, c2):
    out=[]; lines=text.split('\n'); n=max(1,len(lines)-1)
    for i,L in enumerate(lines):
        r=int(c1[0]+(c2[0]-c1[0])*i/n)
        g=int(c1[1]+(c2[1]-c1[1])*i/n)
        b=int(c1[2]+(c2[2]-c1[2])*i/n)
        out.append(f"\033[38;2;{r};{g};{b}m{L}\033[0m")
    return '\n'.join(out)

def center(text):
    tw=shutil.get_terminal_size().columns
    for L in text.split('\n'):
        p=max(0,(tw-vlen(L))//2)
        print(' '*p+L)

def banner():
    os.system("clear")
    art = """
    ██████    █████   █████   █████████      ██████    ██████████ █████
  ███░░░░███ ░░███   ░░███   ███░░░░░███   ███░░░░███ ░░███░░░░░█░░███
 ███    ░░███ ░███    ░███  ░███    ░███  ███    ░░███ ░███  █ ░  ░███
░███     ░███ ░███    ░███  ░███████████ ░███     ░███ ░██████    ░███
░███   ██░███ ░░███   ███   ░███░░░░░███ ░███   ██░███ ░███░░█    ░███
░░███ ░░████   ░░░█████░    ░███    ░███ ░░███ ░░████  ░███ ░   █ ░███
 ░░░██████░██    ░░███      █████   █████ ░░░██████░██ ██████████ █████
   ░░░░░░ ░░      ░░░      ░░░░░   ░░░░░    ░░░░░░ ░░ ░░░░░░░░░░ ░░░░░"""
    center(grad(art,(173,216,230),(70,130,180)))
    for L in [f"{B3}[+] Company : Qvaqel Security Project{C0}",
              f"{B3}[+] Github  : https://github.com/qvaqel{C0}",
              f"{B3}[+] Coded By: qvaqel team{C0}",
              f"{B3}[+] Version : 3.0 (Blue Edition){C0}",
              f"{YL}[!] Educational use only!{C0}"]:
        p=max(0,(shutil.get_terminal_size().columns-vlen(L))//2)
        print(' '*p+L)
    sep=f"{B4}{'─'*40}{C0}"
    p=max(0,(shutil.get_terminal_size().columns-vlen(sep))//2)
    print(' '*p+sep)

def ok(m): print(f"{GR}[+] {m}{C0}")
def info(m): print(f"{B3}[*] {m}{C0}")
def err(m): print(f"{RD}[-] {m}{C0}")
def pause(): input(f"\n{B2}Press Enter...{C0}")
def sh(c): return subprocess.run(c,shell=True).returncode

def apt_i(*p):
    for x in p:
        info(f"Installing {x}...")
        ok(f"{x} ok") if sh(f"pkg install -y {x} >/dev/null 2>&1")==0 else err(f"{x} fail")

def pip_i(*p):
    for x in p:
        info(f"pip {x}"); ok(f"{x} ok") if sh(f"pip install {x} >/dev/null 2>&1")==0 else err(f"{x} fail")

def git_g(url,n):
    d=os.path.join(TOOLS,n)
    if os.path.isdir(d): sh(f"git -C '{d}' pull >/dev/null 2>&1")
    else: sh(f"git clone --depth 1 {url} '{d}' >/dev/null 2>&1")
    ok(f"{n} ready")

def run_t(n,cmd):
    d=os.path.join(TOOLS,n)
    if os.path.isdir(d):
        os.chdir(d); sh(cmd); os.chdir(QDIR)
    else: err(f"{n} not installed")

# ===== TOOLS =====
INFO_GATHERING=[("Nmap",lambda:apt_i("nmap"),"nmap --help"),("RedHawk",lambda:git_g("https://github.com/Tuhinshubhra/RED_HAWK","redhawk"),None),("MaxSubdoFinder",lambda:git_g("https://github.com/Maxitte/MaxSubdoFinder","maxsubdo"),None),("ReconDog",lambda:git_g("https://github.com/s0md3v/ReconDog","recon"),"python dog.py"),("Seeker",lambda:(git_g("https://github.com/thewhiteh4t/seeker","seeker"),pip_i("requests")),"python seeker.py"),("Trape",lambda:(git_g("https://github.com/jofpin/trape","trape"),pip_i("flask","requests")),"python trape.py"),("Sherlock",lambda:git_g("https://github.com/sherlock-project/sherlock","sherlock"),"python sherlock.py"),("Photon",lambda:git_g("https://github.com/s0md3v/Photon","photon"),"python photon.py")]
WEB_ANALYSIS=[("SQLmap",lambda:git_g("https://github.com/sqlmapproject/sqlmap","sqlmap"),"python sqlmap.py -h"),("Nikto",lambda:git_g("https://github.com/sullo/nikto","nikto"),"perl nikto.pl -h"),("WPScan",lambda:(apt_i("ruby"),sh("gem install wpscan")),"wpscan --help"),("Dirb",lambda:apt_i("dirb"),"dirb"),("WhatWeb",lambda:apt_i("whatweb"),"whatweb --help"),("XSSer",lambda:apt_i("xsser"),"xsser --help"),("Burp",lambda:apt_i("burpsuite"),"burpsuite"),("OWASP-ZAP",lambda:apt_i("zaproxy"),"zaproxy")]
VULN_SCAN=[("Nuclei",lambda:sh("go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest"),"nuclei -h"),("Dalfox",lambda:sh("go install github.com/hahwul/dalfox/v2@latest"),"dalfox"),("Commix",lambda:git_g("https://github.com/commixproject/commix","commix"),"python commix.py --help"),("Skipfish",lambda:apt_i("skipfish"),"skipfish"),("Wapiti",lambda:apt_i("wapiti"),"wapiti --help"),("Arachni",lambda:apt_i("arachni"),"arachni --help"),("Wfuzz",lambda:pip_i("wfuzz"),"wfuzz --help"),("JoomScan",lambda:git_g("https://github.com/OWASP/joomscan","joomscan"),"perl joomscan.pl")]
PASS_HASH=[("John",lambda:apt_i("john"),"john"),("Hydra",lambda:apt_i("hydra"),"hydra -h"),("Hashcat",lambda:apt_i("hashcat"),"hashcat --help"),("HashID",lambda:pip_i("hashid"),"hashid -h"),("Crunch",lambda:apt_i("crunch"),"crunch"),("Medusa",lambda:apt_i("medusa"),"medusa -h"),("Cupp",lambda:git_g("https://github.com/Mebus/cupp","cupp"),"python cupp.py"),("RSMangler",lambda:git_g("https://github.com/digininja/RSMangler","rsmangler"),"python rsmangler.py")]
WIRELESS=[("Aircrack-ng",lambda:apt_i("aircrack-ng"),"aircrack-ng"),("Bettercap",lambda:apt_i("bettercap"),"bettercap -h"),("Reaver",lambda:apt_i("reaver"),"reaver"),("Bully",lambda:apt_i("bully"),"bully"),("Wifite",lambda:git_g("https://github.com/derv82/wifite2","wifite"),"python wifite.py"),("Kismet",lambda:apt_i("kismet"),"kismet"),("Fern",lambda:git_g("https://github.com/savio-code/fern-wifi-cracker","fern"),None),("Fluxion",lambda:git_g("https://github.com/FluxionNetwork/fluxion","fluxion"),"bash fluxion.sh")]
PHISHING=[("SocialFish",lambda:(git_g("https://github.com/UndeadSec/SocialFish","socialfish"),pip_i("flask")),"python SocialFish.py"),("Zphisher",lambda:git_g("https://github.com/htr-tech/zphisher","zphisher"),"bash zphisher.sh"),("Gophish",lambda:git_g("https://github.com/gophish/gophish","gophish"),None),("BlackPhish",lambda:git_g("https://github.com/iinc0gnit0/BlackPhish","blackphish"),"python blackphish.py"),("ShellPhish",lambda:git_g("https://github.com/An0nUD4Y/shellphish","shellphish"),"bash shellphish.sh"),("SayCheese",lambda:git_g("https://github.com/hangetzzu/saycheese","saycheese"),"bash saycheese.sh"),("PyPhisher",lambda:git_g("https://github.com/KasRoudra2/PyPhisher","pyphisher"),"python pyphisher.py"),("Evilginx",lambda:git_g("https://github.com/kgretzky/evilginx2","evilginx"),"python evilginx.py")]
EXPLOIT=[("Metasploit",lambda:sh("pkg install -y unstable-repo && pkg install -y metasploit"),"msfconsole --version"),("SearchSploit",lambda:sh("pkg install -y exploitdb"),"searchsploit"),("MSFVenom",lambda:sh("pkg install -y metasploit"),"msfvenom --help"),("Routersploit",lambda:git_g("https://github.com/threat9/routersploit","routersploit"),"python rsf.py"),("BeEF",lambda:sh("gem install beef"),"beef"),("Faraday",lambda:pip_i("faradaysec"),"faraday --help"),("ExploitDB",lambda:git_g("https://github.com/offensive-security/exploitdb","exploitdb"),None),("Commix",lambda:git_g("https://github.com/commixproject/commix","commix"),"python commix.py")]
SOCIAL=[("SET",lambda:git_g("https://github.com/trustedsec/social-engineer-toolkit","set"),"python setoolkit"),("KingPhisher",lambda:git_g("https://github.com/securestate/king-phisher","kingphisher"),None),("Maltego",lambda:apt_i("maltego"),"maltego"),("Recon-ng",lambda:git_g("https://github.com/lanmaster53/recon-ng","recon-ng"),"python recon-ng"),("theHarvester",lambda:git_g("https://github.com/laramies/theHarvester","theharvester"),"python theHarvester.py"),("SpiderFoot",lambda:git_g("https://github.com/smicallef/spiderfoot","spiderfoot"),"python sf.py"),("Osintgram",lambda:git_g("https://github.com/Datalux/Osintgram","osintgram"),"python main.py"),("Maigret",lambda:git_g("https://github.com/soxoj/maigret","maigret"),"python maigret.py")]
FORENSICS=[("Autopsy",lambda:apt_i("autopsy"),"autopsy"),("Volatility",lambda:pip_i("volatility"),"vol.py --help"),("Binwalk",lambda:apt_i("binwalk"),"binwalk --help"),("Foremost",lambda:apt_i("foremost"),"foremost"),("SleuthKit",lambda:apt_i("sleuthkit"),"fls --help"),("Guymager",lambda:apt_i("guymager"),"guymager"),("BulkExtractor",lambda:apt_i("bulk-extractor"),"bulk_extractor --help"),("Redline",lambda:apt_i("redline"),"redline")]
REVERSE=[("Ghidra",lambda:git_g("https://github.com/NationalSecurityAgency/ghidra","ghidra"),None),("Radare2",lambda:apt_i("radare2"),"r2 -h"),("Objdump",lambda:apt_i("binutils"),"objdump --help"),("Cutter",lambda:apt_i("cutter"),"cutter"),("Frida",lambda:pip_i("frida"),"frida --version"),("Ltrace",lambda:apt_i("ltrace"),"ltrace --help"),("Strace",lambda:apt_i("strace"),"strace --help"),("IDA-Free",lambda:apt_i("ida-free"),"idafree")]
MALWARE=[("YARA",lambda:apt_i("yara"),"yara --help"),("ClamAV",lambda:apt_i("clamav"),"clamscan --help"),("PEfile",lambda:pip_i("pefile"),"python -m pefile"),("Cuckoo",lambda:git_g("https://github.com/cuckoosandbox/cuckoo","cuckoo"),None),("Capa",lambda:pip_i("capa"),"capa --help"),("VirusTotal-API",lambda:pip_i("virustotal-api"),"python -m virustotal_api"),("MalwareBazaar",lambda:pip_i("mwdblib"),"python -m mwdblib"),("AnyRun",lambda:pip_i("anyrun"),"python -m anyrun")]
STEGANO=[("Steghide",lambda:apt_i("steghide"),"steghide --help"),("Stegsolve",lambda:git_g("https://github.com/eugenekolo/sec-tools","stegsolve"),None),("Outguess",lambda:apt_i("outguess"),"outguess --help"),("Zsteg",lambda:sh("gem install zsteg"),"zsteg"),("ExifTool",lambda:apt_i("exiftool"),"exiftool"),("Stegano",lambda:pip_i("stegano"),"python -m stegano"),("OpenStego",lambda:apt_i("openstego"),"openstego"),("WbStego",lambda:apt_i("wbstego"),"wbstego")]
CRYPTO=[("OpenSSL",lambda:apt_i("openssl"),"openssl version"),("GPG",lambda:apt_i("gnupg"),"gpg --help"),("VeraCrypt",lambda:apt_i("veracrypt"),"veracrypt --version"),("Kleopatra",lambda:apt_i("kleopatra"),"kleopatra"),("CCrypt",lambda:apt_i("ccrypt"),"ccrypt --help"),("RsaCtfTool",lambda:git_g("https://github.com/RsaCtfTool/RsaCtfTool","rsactftool"),"python RsaCtfTool.py"),("CyberChef",lambda:apt_i("cyberchef"),"cyberchef"),("Hashcat",lambda:apt_i("hashcat"),"hashcat --help")]
DDOS=[("LOIC",lambda:git_g("https://github.com/NewEraCracker/LOIC","loic"),None),("Slowloris",lambda:pip_i("slowloris"),"slowloris --help"),("HULK",lambda:git_g("https://github.com/grafov/hulk","hulk"),"python hulk.py"),("Xerxes",lambda:git_g("https://github.com/zanyarjamal/xerxes","xerxes"),"gcc xerxes.c -o xerxes"),("GoldenEye",lambda:git_g("https://github.com/jseidl/GoldenEye","goldeneye"),"python goldeneye.py"),("T50",lambda:apt_i("t50"),"t50 --help"),("UFONet",lambda:git_g("https://github.com/epsylon/ufonet","ufonet"),"python ufonet"),("Torshammer",lambda:git_g("https://github.com/dotfighter/torshammer","torshammer"),"python torshammer.py")]
NETWORK=[("Wireshark",lambda:apt_i("wireshark"),"wireshark"),("Tcpdump",lambda:apt_i("tcpdump"),"tcpdump --help"),("Netstat",lambda:apt_i("net-tools"),"netstat --help"),("Iptables",lambda:apt_i("iptables"),"iptables --help"),("Nftables",lambda:apt_i("nftables"),"nft --help"),("Suricata",lambda:apt_i("suricata"),"suricata --help"),("Snort",lambda:apt_i("snort"),"snort --help"),("Zeek",lambda:apt_i("zeek"),"zeek --help")]
CLOUD=[("AWS-CLI",lambda:apt_i("awscli"),"aws --version"),("Azure-CLI",lambda:apt_i("azure-cli"),"az --version"),("GCloud",lambda:apt_i("google-cloud-sdk"),"gcloud --version"),("Terraform",lambda:apt_i("terraform"),"terraform --version"),("Packer",lambda:apt_i("packer"),"packer --version"),("Ansible",lambda:pip_i("ansible"),"ansible --version"),("Docker",lambda:apt_i("docker"),"docker --version"),("Kubectl",lambda:apt_i("kubectl"),"kubectl --help")]
MOBILE=[("MobSF",lambda:git_g("https://github.com/MobSF/Mobile-Security-Framework-MobSF","mobsf"),"python manage.py runserver"),("APKTool",lambda:apt_i("apktool"),"apktool --help"),("Jadx",lambda:apt_i("jadx"),"jadx --help"),("Frida-Mobile",lambda:pip_i("frida"),"frida --version"),("Drozer",lambda:git_g("https://github.com/FSecureLABS/drozer","drozer"),"python drozer.py"),("Androguard",lambda:pip_i("androguard"),"python -m androguard"),("Objection",lambda:pip_i("objection"),"objection --help"),("Magisk",lambda:apt_i("magisk"),"magisk --version")]
IOT=[("Firmware-Analysis",lambda:git_g("https://github.com/attify/firmware-analysis-toolkit","fat"),"python fat.py"),("RouterSploit",lambda:git_g("https://github.com/threat9/routersploit","routersploit"),"python rsf.py"),("Zigbee-Tools",lambda:apt_i("zigbee-tools"),"zigbee --help"),("BLE-Tools",lambda:apt_i("bluez"),"bluetoothctl"),("MQTT-Tools",lambda:pip_i("paho-mqtt"),"python -m paho.mqtt"),("CoAP-Tools",lambda:pip_i("aiocoap"),"python -m aiocoap"),("IoT-Exploit",lambda:git_g("https://github.com/exploit-db/exploitdb","iot-exploit"),None),("Mirai-Scanner",lambda:git_g("https://github.com/james93102/Mirai-Source-Code","mirai"),None)]
API_SEC=[("Postman",lambda:apt_i("postman"),"postman"),("Insomnia",lambda:apt_i("insomnia"),"insomnia"),("Swagger",lambda:pip_i("swagger-ui"),"python -m swagger_ui"),("OWASP-API",lambda:git_g("https://github.com/OWASP/API-Security","owasp-api"),None),("Kong",lambda:apt_i("kong"),"kong --version"),("Tyk",lambda:apt_i("tyk"),"tyk --version"),("Apigee",lambda:apt_i("apigee"),"apigee --help"),("3scale",lambda:apt_i("3scale"),"3scale --help")]
CONTAINER=[("Docker-Sec",lambda:apt_i("docker"),"docker --version"),("Kubernetes-Sec",lambda:apt_i("kubectl"),"kubectl --help"),("Falco",lambda:apt_i("falco"),"falco --help"),("Trivy",lambda:sh("go install github.com/aquasecurity/trivy@latest"),"trivy --help"),("Clair",lambda:apt_i("clair"),"clair --help"),("Anchore",lambda:pip_i("anchorecli"),"anchore-cli --help"),("Sysdig",lambda:apt_i("sysdig"),"sysdig --help"),("Neuvector",lambda:apt_i("neuvector"),"neuvector --help")]
DB_SEC=[("SQLmap",lambda:git_g("https://github.com/sqlmapproject/sqlmap","sqlmap"),"python sqlmap.py -h"),("NoSQLMap",lambda:git_g("https://github.com/codingo/NoSQLMap","nosqlmap"),"python nosqlmap.py"),("DBPwAudit",lambda:apt_i("dbpwaudit"),"dbpwaudit --help"),("Odat",lambda:git_g("https://github.com/quentinhardy/odat","odat"),"python odat.py"),("Mongodump",lambda:apt_i("mongodb-tools"),"mongodump --help"),("PgDump",lambda:apt_i("postgresql"),"pg_dump --help"),("MySQL-Audit",lambda:apt_i("mysql-audit"),"mysql-audit --help"),("Redis-Tools",lambda:apt_i("redis-tools"),"redis-cli --help")]
EMAIL=[("Phishing-Email",lambda:git_g("https://github.com/drk1wi/Modlishka","modlishka"),"python modlishka.py"),("Email-Spoofer",lambda:git_g("https://github.com/AlisamTechnology/ATSCAN","atscan"),"python atscan.py"),("SMTP-Tester",lambda:pip_i("smtplib"),"python -m smtplib"),("MailSniper",lambda:git_g("https://github.com/dafthack/MailSniper","mailsniper"),None),("Gophish-Email",lambda:git_g("https://github.com/gophish/gophish","gophish"),None),("KingPhisher-Email",lambda:git_g("https://github.com/securestate/king-phisher","kingphisher"),None),("Email-Harvester",lambda:git_g("https://github.com/maldevel/EmailHarvester","emailharvester"),"python EmailHarvester.py"),("TheHarvester-Email",lambda:git_g("https://github.com/laramies/theHarvester","theharvester"),"python theHarvester.py")]
DNS=[("DNSRecon",lambda:git_g("https://github.com/darkoperator/dnsrecon","dnsrecon"),"python dnsrecon.py"),("DNSScan",lambda:apt_i("dnsscan"),"dnsscan --help"),("Sublist3r",lambda:git_g("https://github.com/aboul3la/Sublist3r","sublist3r"),"python sublist3r.py"),("Amass",lambda:sh("go install github.com/OWASP/Amass/v3/...@latest"),"amass --help"),("MassDNS",lambda:git_g("https://github.com/blechschmidt/massdns","massdns"),"make && ./bin/massdns"),("Fierce",lambda:git_g("https://github.com/mschwager/fierce","fierce"),"python fierce.py"),("DNSenum",lambda:apt_i("dnsenum"),"dnsenum --help"),("DNSmap",lambda:apt_i("dnsmap"),"dnsmap --help")]
SSL=[("SSLScan",lambda:apt_i("sslscan"),"sslscan --help"),("TestSSL",lambda:git_g("https://github.com/drwetter/testssl.sh","testssl"),"bash testssl.sh"),("SSLLabs",lambda:pip_i("ssllabs"),"python -m ssllabs"),("OpenSSL-Tools",lambda:apt_i("openssl"),"openssl --help"),("Certbot",lambda:apt_i("certbot"),"certbot --help"),("LetsEncrypt",lambda:apt_i("letsencrypt"),"letsencrypt --help"),("SSLyze",lambda:pip_i("sslyze"),"sslyze --help"),("TLS-Scanner",lambda:git_g("https://github.com/tls-attacker/tls-scanner","tls-scanner"),"java -jar tls-scanner.jar")]
VPN=[("OpenVPN",lambda:apt_i("openvpn"),"openvpn --version"),("WireGuard",lambda:apt_i("wireguard-tools"),"wg --help"),("StrongSwan",lambda:apt_i("strongswan"),"strongswan --version"),("SoftEther",lambda:apt_i("softether-vpn"),"softether --help"),("Pritunl",lambda:apt_i("pritunl"),"pritunl --help"),("ZeroTier",lambda:apt_i("zerotier-one"),"zerotier-cli --help"),("Tailscale",lambda:apt_i("tailscale"),"tailscale --version"),("NetBird",lambda:apt_i("netbird"),"netbird --help")]
TOR=[("Tor",lambda:apt_i("tor"),"tor --version"),("TorBrowser",lambda:apt_i("torbrowser-launcher"),"torbrowser-launcher"),("OnionScan",lambda:git_g("https://github.com/s-rah/onionscan","onionscan"),"python onionscan.py"),("OnionShare",lambda:apt_i("onionshare"),"onionshare --help"),("Ricochet",lambda:apt_i("ricochet"),"ricochet --help"),("Whonix",lambda:apt_i("whonix"),"whonix --help"),("Tails",lambda:apt_i("tails"),"tails --help"),("SubgraphOS",lambda:apt_i("subgraph-os"),"subgraph --help")]
ANON=[("Proxychains",lambda:apt_i("proxychains"),"proxychains --help"),("Torify",lambda:apt_i("tor"),"torify --help"),("Anonsurf",lambda:git_g("https://github.com/Und3rf10w/kali-anonsurf","anonsurf"),"bash anonsurf.sh"),("MAC-Changer",lambda:apt_i("macchanger"),"macchanger --help"),("SpoofMAC",lambda:pip_i("spoofmac"),"spoof-mac --help"),("VPN-Auto",lambda:pip_i("vpn-auto"),"python -m vpn_auto"),("DNS-Leak",lambda:pip_i("dns-leak-test"),"python -m dns_leak_test"),("WebRTC-Leak",lambda:pip_i("webrtc-leak-test"),"python -m webrtc_leak_test")]
BACKUP=[("Rsync",lambda:apt_i("rsync"),"rsync --help"),("Borg",lambda:apt_i("borgbackup"),"borg --help"),("Restic",lambda:apt_i("restic"),"restic --help"),("Duplicati",lambda:apt_i("duplicati"),"duplicati --help"),("Timeshift",lambda:apt_i("timeshift"),"timeshift --help"),("Deja-Dup",lambda:apt_i("deja-dup"),"deja-dup --help"),("BackInTime",lambda:apt_i("backintime"),"backintime --help"),("Amanda",lambda:apt_i("amanda-client"),"amanda --help")]
MONITOR=[("Nagios",lambda:apt_i("nagios"),"nagios --version"),("Zabbix",lambda:apt_i("zabbix"),"zabbix --help"),("Prometheus",lambda:apt_i("prometheus"),"prometheus --version"),("Grafana",lambda:apt_i("grafana"),"grafana --help"),("Datadog",lambda:pip_i("datadog"),"python -m datadog"),("NewRelic",lambda:pip_i("newrelic"),"python -m newrelic"),("Sentry",lambda:pip_i("sentry-sdk"),"python -m sentry_sdk"),("PagerDuty",lambda:pip_i("pagerduty"),"python -m pagerduty")]
LOG=[("ELK-Stack",lambda:apt_i("elasticsearch"),"elasticsearch --version"),("Splunk",lambda:apt_i("splunk"),"splunk --version"),("Graylog",lambda:apt_i("graylog"),"graylog --help"),("Fluentd",lambda:apt_i("fluentd"),"fluentd --version"),("Logstash",lambda:apt_i("logstash"),"logstash --help"),("Kibana",lambda:apt_i("kibana"),"kibana --help"),("Loki",lambda:apt_i("loki"),"loki --help"),("Promtail",lambda:apt_i("promtail"),"promtail --help")]
COMPLIANCE=[("OpenSCAP",lambda:apt_i("openscap"),"oscap --help"),("CIS-CAT",lambda:apt_i("cis-cat"),"cis-cat --help"),("Lynis",lambda:apt_i("lynis"),"lynis --help"),("OSSEC",lambda:apt_i("ossec"),"ossec --help"),("Wazuh",lambda:apt_i("wazuh"),"wazuh --help"),("Tripwire",lambda:apt_i("tripwire"),"tripwire --help"),("AIDE",lambda:apt_i("aide"),"aide --help"),("Samhain",lambda:apt_i("samhain"),"samhain --help")]
REPORT=[("Dradis",lambda:git_g("https://github.com/dradis/dradis-ce","dradis"),"python bin/setup"),("Serpico",lambda:git_g("https://github.com/SerpicoProject/Serpico","serpico"),"ruby serpico.rb"),("PwnDoc",lambda:git_g("https://github.com/pwndoc/pwndoc","pwndoc"),"npm install"),("Faraday-Report",lambda:pip_i("faradaysec"),"faraday --help"),("Ghostwriter",lambda:git_g("https://github.com/GhostManager/Ghostwriter","ghostwriter"),"python manage.py runserver"),("DefectDojo",lambda:git_g("https://github.com/DefectDojo/django-DefectDojo","defectdojo"),"python manage.py runserver"),("SecurityNik",lambda:git_g("https://github.com/securitynik/securitynik","securitynik"),None),("ReportGen",lambda:pip_i("reportgen"),"python -m reportgen")]
DOC=[("MkDocs",lambda:pip_i("mkdocs"),"mkdocs --help"),("Sphinx",lambda:pip_i("sphinx"),"sphinx-build --help"),("Docusaurus",lambda:apt_i("docusaurus"),"docusaurus --help"),("GitBook",lambda:apt_i("gitbook"),"gitbook --help"),("Notion",lambda:pip_i("notion-api"),"python -m notion_api"),("Confluence",lambda:pip_i("confluence-api"),"python -m confluence_api"),("WikiJS",lambda:apt_i("wikijs"),"wikijs --help"),("BookStack",lambda:apt_i("bookstack"),"bookstack --help")]

CATEGORIES = [
    ("Information Gathering", INFO_GATHERING), ("Web Analysis", WEB_ANALYSIS),
    ("Vulnerability Scanner", VULN_SCAN), ("Password & Hash", PASS_HASH),
    ("Wireless Tools", WIRELESS), ("Phishing Tools", PHISHING),
    ("Exploit Tools", EXPLOIT), ("Social Engineering", SOCIAL),
    ("Forensics Tools", FORENSICS), ("Reverse Engineering", REVERSE),
    ("Malware Analysis", MALWARE), ("Steganography", STEGANO),
    ("Cryptography", CRYPTO), ("DDoS Tools", DDOS),
    ("Network Analysis", NETWORK), ("Cloud Security", CLOUD),
    ("Mobile Security", MOBILE), ("IoT Security", IOT),
    ("API Security", API_SEC), ("Container Security", CONTAINER),
    ("Database Security", DB_SEC), ("Email Security", EMAIL),
    ("DNS Security", DNS), ("SSL/TLS Tools", SSL),
    ("VPN Tools", VPN), ("Tor Tools", TOR),
    ("Anonymity Tools", ANON), ("Backup Tools", BACKUP),
    ("Monitoring Tools", MONITOR), ("Logging Tools", LOG),
    ("Compliance Tools", COMPLIANCE), ("Reporting Tools", REPORT),
    ("Documentation", DOC), ("Terminal Panel", None),
    ("Update System", None), ("About System", None),
    ("Settings", None), ("Help", None),
    ("Credits", None), ("Exit System", None),
]

# ===== КОМПАКТНОЕ МЕНЮ: 3 колонки, заголовок на всю ширину =====
def main_menu():
    cw = 26  # ширина колонки (увеличил чтобы все названия помещались)
    nc = 3
    nr = 14  # строк
    total_width = cw * nc + (nc - 1)  # общая ширина с разделителями
    
    lines = []
    # Верхняя рамка
    lines.append(f"┌{'─'*total_width}┐")
    # Заголовок на всю ширину (одна длинная строка)
    title = " QVAQEL MAIN MENU "
    lines.append(f"│{title:^{total_width}}│")
    lines.append(f"├{'─'*cw}┬{'─'*cw}┬{'─'*cw}┤")
    
    for row in range(nr):
        parts = []
        for col in range(nc):
            idx = row + col * nr
            if idx < len(CATEGORIES):
                cell = f"[{idx+1:02d}] {CATEGORIES[idx][0]}"
                parts.append(f" {cell:<{cw-1}}")
            else:
                parts.append(f" {'':<{cw-1}}")
        lines.append("│" + "│".join(parts) + "│")
    
    lines.append(f"└{'─'*cw}┴{'─'*cw}┴{'─'*cw}┘")
    return lines

def box(lines):
    if not lines: lines=[""]
    w=max(vlen(l) for l in lines)+2
    t="┏"+"━"*w+"┓"; b="┗"+"━"*w+"┛"
    res=[t]
    for l in lines:
        vl=vlen(l); pad=' '*(w-vl-2) if vl<w-2 else ''
        res.append(f"┃ {l}{pad} ┃")
    res.append(b)
    return '\n'.join(res)

def submenu(title, prompt, tools):
    if tools is None: return
    while True:
        banner(); print()
        cols=3; rows=(len(tools)+cols-1)//cols
        box_lines=[f"== {title} ==",""]
        for r in range(rows):
            parts=[]
            for c in range(cols):
                idx=r+c*rows
                if idx<len(tools):
                    parts.append(f"[{idx+1:02d}] {tools[idx][0]}")
                else:
                    parts.append("")
            box_lines.append("   ".join(parts))
        box_lines.append("")
        box_lines.append(f"[{len(tools)+1:02d}] Back   [{len(tools)+2:02d}] Exit")
        boxed=box(box_lines)
        center(grad(boxed,(135,206,250),(100,149,237)))
        try: ch=input(f"\n{B1}{prompt}: {C0}").strip()
        except: return
        if not ch.isdigit(): continue
        ch=int(ch)
        if 1<=ch<=len(tools):
            nm,inst,run=tools[ch-1]
            try: inst()
            except Exception as e: err(str(e))
            if run: run_t(nm.lower(),run)
            pause()
        elif ch==len(tools)+1: return
        elif ch==len(tools)+2: sys.exit(0)

def terminal_panel():
    while True:
        banner(); print()
        lines=["== Terminal Panel ==","","[01] Setup storage  [02] Install pkgs  [03] Neofetch","[04] Open tools dir [05] Back",""]
        center(box(lines))
        ch=input(f"\n{B1}Panel: {C0}").strip()
        if ch=="1": sh("termux-setup-storage"); pause()
        elif ch=="2": apt_i("git","python","wget","curl","php","ruby","openssh","figlet","toilet","jq","zip","unzip","pv","nano","neofetch"); pause()
        elif ch=="3": sh("neofetch 2>/dev/null"); pause()
        elif ch=="4": os.chdir(TOOLS); sh(os.environ.get("SHELL","bash")); os.chdir(QDIR)
        elif ch=="5": return

def update_system():
    banner(); info("Updating..."); sh("pkg update -y && pkg upgrade -y"); ok("Updated"); pause()

def about_system():
    banner(); print()
    lines=["== About qvaqel ==","","Name    : qvaqel Blue Edition","Version : 3.0","Lang    : Python 3",f"Tools in: {TOOLS}",""]
    center(box(lines)); pause()

def settings_menu():
    banner(); print()
    lines=["== Settings ==","","[01] Theme: Blue","[02] Language: EN","[03] Back",""]
    center(box(lines)); pause()

def help_menu():
    banner(); print()
    lines=["== Help ==","","1. Choose category","2. Install & run tools","3. Back to return",""]
    center(box(lines)); pause()

def credits_menu():
    banner(); print()
    lines=["== Credits ==","","Project: Qvaqel Security","Team: qvaqel team","Version: 3.0",""]
    center(box(lines)); pause()

def first_run():
    flag=os.path.join(QDIR,".deps_ok")
    if os.path.exists(flag): return
    banner(); info("First run: deps...")
    apt_i("git","python","wget","curl","php","ruby","openssh","figlet","toilet","jq","zip","unzip","pv","neofetch")
    open(flag,"w").write("ok"); ok("Ready"); import time; time.sleep(1)

def main():
    first_run()
    while True:
        banner(); print()
        menu_lines = main_menu()
        menu_text = '\n'.join(menu_lines)
        menu_grad = grad(menu_text, (135, 206, 250), (100, 149, 237))
        center(menu_grad)
        try: opt=input(f"\n{B1}Options: {C0}").strip()
        except: opt="40"
        if not opt.isdigit(): continue
        opt_num = int(opt)
        if 1 <= opt_num <= len(CATEGORIES):
            cat_name, cat_tools = CATEGORIES[opt_num - 1]
            if cat_tools is None:
                if cat_name == "Terminal Panel": terminal_panel()
                elif cat_name == "Update System": update_system()
                elif cat_name == "About System": about_system()
                elif cat_name == "Settings": settings_menu()
                elif cat_name == "Help": help_menu()
                elif cat_name == "Credits": credits_menu()
                elif cat_name == "Exit System": banner(); print(f"{B3}Bye!{C0}"); sys.exit(0)
            else: submenu(cat_name, cat_name[:4], cat_tools)

if __name__=="__main__":
    main()
