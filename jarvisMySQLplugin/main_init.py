# File Name: main_init.py
# Author: Samuel Lewis

#$ TO-DO List $#
#[] TO-DO List Item
#[*] Completed TO-DO List Item

#* Libraries *#

import os
import re
import getpass
from pathlib import Path

#* Custom Libraries *#

#~ import custom made libraries here

#^ Variables ^#

#~ create and store variables here

#& Functions &#

#~ Helper: quote values for .env
def _quote_env_value(value: str) -> str:
    """Quote value if it contains spaces or special chars.
    Escapes backslashes and double quotes inside quoted strings.
    """
    if value is None:
        return ""
    needs_quotes = any(ch in value for ch in [' ', '\t', '#', '"', "'", '=', '\\'])
    if needs_quotes:
        escaped = value.replace('\\', r'\\').replace('"', r'\"')
        return f'"{escaped}"'
    return value


def init(
    usr: str | None = None,
    pwd: str | None = None,
    host: str | None = None,
    port: int | str | None = None,
    db: str | None = None,
    env_path: str | None = None,
    *,
    non_interactive: bool = False,
) -> Path:
    """Initialize credentials by writing them to jarvisMySQLplugin/.env.

    Usage examples:
      - Programmatic: init(usr="me@example.com", pwd="secret")
      - With options: init(usr="me", pwd="secret", host="db.local", port=3307)
      - Interactive: init()  -> prompts for any missing values

    If host/port not provided, they default to localhost:3306.
    Returns the path to the written .env file.
    """
    plugin_dir = Path(__file__).resolve().parent
    env_file = Path(env_path) if env_path else plugin_dir / ".env"

    # Defaults
    default_host = os.environ.get("MYSQL_HOST", "localhost")
    default_port = os.environ.get("MYSQL_PORT", "3306")

    host = (host or "").strip() or default_host
    port = str(port).strip() if port is not None else default_port

    # Collect missing username/password
    if not usr and not non_interactive:
        usr = ""
        while not usr:
            usr = input("MySQL username: ").strip()
            if not usr:
                print("Username cannot be empty.")

    if not pwd and not non_interactive:
        pwd = ""
        while not pwd:
            pwd = getpass.getpass("MySQL password (input hidden): ").strip()
            if not pwd:
                print("Password cannot be empty.")

    if non_interactive:
        if not usr or not pwd:
            raise ValueError("usr and pwd are required in non_interactive mode")

    # Optional DB prompt only when interactive and not provided
    if db is None and not non_interactive:
        db = input("Default database (optional): ").strip() or None

    # Build .env content
    lines = [
        f"MYSQL_HOST={_quote_env_value(host)}",
        f"MYSQL_PORT={_quote_env_value(str(port))}",
        f"MYSQL_USER={_quote_env_value(usr or '')}",
        f"MYSQL_PASSWORD={_quote_env_value(pwd or '')}",
    ]
    if db:
        lines.append(f"MYSQL_DB={_quote_env_value(db)}")

    env_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
    try:
        os.chmod(env_file, 0o600)
    except Exception:
        # Best effort; Windows may ignore POSIX perms (e.g., Windows)
        pass

    print(f"Saved credentials to {env_file} (password not displayed).")
    return env_file


def init_from_command(command: str, env_path: str | None = None) -> Path:
    """Parse commands like: init(usr:john@gmail.com, pwd:1234, host:db, port:3307)

    Whitespace is ignored. Values may be quoted with ' or ". host/port are optional.
    """
    text = command.strip()
    # Allow either full 'init(...)' or just 'usr:..., pwd:...'
    if text.lower().startswith("init"):
        m = re.match(r"^\s*init\s*\((.*)\)\s*$", text, flags=re.IGNORECASE)
        if not m:
            raise ValueError("Invalid init command syntax")
        inner = m.group(1)
    else:
        inner = text

    pairs = {}
    pattern = re.compile(r"(usr|pwd|host|port|db|env)\s*:\s*(\".*?\"|'.*?'|[^,]+)", re.IGNORECASE)
    for key, raw_val in pattern.findall(inner):
        val = raw_val.strip()
        if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
            val = val[1:-1]
        pairs[key.lower()] = val

    usr = pairs.get("usr")
    pwd = pairs.get("pwd")
    host = pairs.get("host")
    port = pairs.get("port")
    db = pairs.get("db")
    env = pairs.get("env")
    if env:
        env_path = env

    return init(usr=usr, pwd=pwd, host=host, port=port, db=db, env_path=env_path, non_interactive=True)

#= Classes =#

#~ define and build classes here

#! Main Program !#

if __name__ == "__main__":
    # CLI usage:
    #   python -m jarvisMySQLplugin.main_init
    #     -> interactive prompts
    #   python -m jarvisMySQLplugin.main_init "init(usr:john@example.com, pwd:1234)"
    #     -> non-interactive with defaults for host/port
    import sys
    if len(sys.argv) > 1:
        cmd = " ".join(sys.argv[1:])
        init_from_command(cmd)
    else:
        print("JARVIS MySQL Plugin setup — let’s store your credentials.")
        print(f".env location: {Path(__file__).resolve().parent / '.env'}")
        init()



#- UNASSIGNED COLOR -#
#| UNASSIGNED COLOR |#
#? UNASSIGNED COLOR ?#
#+ UNASSIGNED COLOR +#
#: UNASSIGNED COLOR :#
#; UNASSIGNED COLOR ;#
#% UNASSIGNED COLOR %#
#@ UNASSIGNED COLOR @#
