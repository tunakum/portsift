WEB_PORTS = {
    80: "HTTP",
    443: "HTTPS",
    8000: "HTTP-Alt",
    8080: "HTTP-Proxy",
    8443: "HTTPS-Alt",
}

DB_PORTS = {
    1433: "MSSQL",
    3306: "MySQL",
    5432: "PostgreSQL",
    27017: "MongoDB",    
}

MAIL_PORTS = {
    25: "SMTP",
    110: "POP3",
    143: "IMAP",
    465: "SMTPS",
    587: "SMTP-Submission",
    993: "IMAPS",
    995: "POP3S",
}

REMOTE_PORTS = {
    20: "FTP-Data",
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    445: "SMB",
}

NETWORK_PORTS = {
    53: "DNS",
    67: "DHCP",
    161: "SNMP",
}   

COMMON_PORTS = {
    **WEB_PORTS,
    **DB_PORTS,
    **MAIL_PORTS,
    **REMOTE_PORTS,
    **NETWORK_PORTS,
}


def get_service(port):
    return COMMON_PORTS.get(port, "Unknown")