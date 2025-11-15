#yanlış girme hakkı gelecek, 3 veya 5 yanlış sonrasında kapanacak
import time
import pyfiglet
from rich.console import Console
from rich.table import Table
from rich.text import Text
from scanner.core import scan_ports
from scanner.utils import validate_ip
from scanner.ports import get_service


console = Console()

def display_banner():
    ascii_art = pyfiglet.figlet_format("portsift", font = "big")
    colored_art = Text(ascii_art, style = "navy_blue")
    console.print(colored_art)
    
    console.print("[dim]Fast & Simple Port Scanner[/dim]\n", justify="center")
    console.rule(style="grey50")
    
    custom_art = r"""                                                                    
  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠐⢄⠀⠀
⠀⡰⠊⠙⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⢃⠀
⢰⠀⠀⠀⡇⠀⠀⠀⠀⠀⣀⣤⠴⣄⡀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠈⡄
⡔⠁⠀⠀⡇⠀⠀⢀⠤⠂⠉⠀⠀⠀⠀⠈⢐⠤⡀⠀⢸⠀⠀⠀⠀⡇
⡇⠀⠀⠀⠃⠀⡰⠉⢠⠀⠀⠀⠀⠀⠀⠀⡆⠀⠈⢂⢸⠀⠀⠀⢀⠇
⠱⠀⠀⠀⠰⣜⣤⣤⡀⡇⠀⠀⠀⠀⠀⠀⢀⡾⢻⣶⣯⠀⠀⠢⡈⠀
⠀⠣⡀⠀⢠⢿⣿⣤⣿⣤⡠⠐⠒⠒⠂⢄⣿⣷⣾⣿⡏⡇⢀⠜⠀⠀
⠀⠀⠈⠢⢸⠜⢿⣿⣿⢿⡄⠀⠀⠀⠀⢸⠛⣿⣿⡟⠔⡏⠁⠀⠀⠀
⠀⠀⠀⠀⠈⢂⣡⠿⠯⠁⣈⣢⣀⣠⣔⠡⠤⠒⢉⠱⠊⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠈⠉⠖⠲⠂⠀⣤⠀⠐⠒⢈⠋⢆⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠇⠀⠺⣆⠀⠀⡎⠀⢸⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⡏⠀⠀⢸⠀⠀⠉⠀⢠⠀⠀⠘⡇⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢀⣠⠤⠼⡇⠀⠀⠸⠀⠀⠀⠀⠘⠀⠀⠀⠹⢄⡀⠀⠀⠀⠀
⠀⢀⠎⠉⠉⢣⠀⡇⠀⠀⠀⡄⠀⠀⠀⡇⠀⠀⠀⠀⢠⡬⠒⠦⣀⠀
⠀⠘⡁⠀⠀⢠⠃⢡⠀⠀⠀⣷⣤⣤⣤⠀⠀⠀⡜⠀⡆⠀⠀⠀⢹⠀
⠀⠀⠈⠐⠒⠈⠈⠉⠱⠢⡞⠂⠀⠀⠘⢢⡤⠎⠑⠒⠓⠤⠤⠄⠃⠀                                                                                                  
    """
    console.print(custom_art, style = "dark_blue")


def get_target_ip():
    console.print("[white]Target IP:[/white]")
    while True:
        ip = console.input("[cyan]portsift>[/cyan] ").strip()
        if validate_ip(ip):
            return ip
        else:
            console.print("[red]✗ Invalid IP. Try again.[/red]")

def get_port_range():
    console.print("\n[cyan]Port Range:[/cyan]")
    console.print("  1. Quick scan (1-1024)")
    console.print("  2. Full scan (1-65535)")
    console.print("  3. Custom ports")
    
    console.print("\n[white]Choose [1/2/3]:[/white]")
    choice = console.input("[cyan]portsift>[/cyan] ").strip()
    
    if choice == "1":
        return range(1, 1025)
    elif choice == "2":
        return range(1, 65536)
    elif choice == "3":
        console.print("[white]Enter ports (e.g., 21,22,80):[/white]")
        ports_input = console.input("[cyan]portsift>[/cyan] ").strip()
        try:
            return [int(p.strip()) for p in ports_input.split(",")]
        except ValueError:
            console.print("[yellow]⚠ Invalid input, using quick scan[/yellow]")
            return range(1, 1025)
    else:
        console.print("[yellow]⚠ Invalid choice, using quick scan[/yellow]")
        return range(1, 1025)

def display_results(open_ports, scan_time):

    console.print(f"\n[green]✓ Scan completed in {scan_time:.2f}s[/green]\n")
    
    if(open_ports):
        table = Table(title=f"Found {len(open_ports)} Open Ports", 
                      show_header=True, 
                      header_style="blue3")
        
        table.add_column("Port", style="cyan", justify="right", width=8)
        table.add_column("Service", style = "cyan", width=20)
        table.add_column("Status", style="dark_green", width=10)
        
        for port in open_ports:
            service = get_service(port)
            table.add_row(str(port), service, "OPEN")
        
        console.print(table)
    else:
        console.print("[red]✗[/red] [yellow]No open ports found.[/yellow]")

def run_cli():

    try:
        display_banner()
        
        target_ip = get_target_ip()        
        port_range = get_port_range()
        
        console.print(f"\n[cyan]→ Scanning {target_ip}...[/cyan]")
        start_time = time.time()
        
        open_ports = scan_ports(target_ip, port_range)
        
        scan_time = time.time() - start_time
        
        display_results(open_ports, scan_time)
        
    except KeyboardInterrupt:
        console.print("\n\n[red]✗[bright_red] Scan interrupted.[/bright_red] Exiting...")
        exit(0)