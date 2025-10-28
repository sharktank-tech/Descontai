import socket
host="db.ymqrprlpwrhxpdwfbtjk.supabase.co"
port=5432
for fam in (socket.AF_INET, socket.AF_INET6):
    try:
        s=socket.socket(fam, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((host,port))
        print("Connected using", "IPv4" if fam==socket.AF_INET else "IPv6")
        s.close()
    except Exception as e:
        print("Failed on", "IPv4" if fam==socket.AF_INET else "IPv6", ":", e)
