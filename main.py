from os import get_terminal_size
from typing import Optional

import click
import uvicorn  # type:ignore

from src.app import app as AppRoot  # noqa:F401
from src.utils.config import DEBUG, VERSION, Config
from src.utils.log import LOG_LEVEL, logger

COPYRIGHT = r"""<b><g>
  _    _ _ _     _          _____ _____  
 | |  | (_) |   (_)   /\   |  __ \_   _| 
 | |__| |_| |__  _   /  \  | |__) || |   
 |  __  | | '_ \| | / /\ \ |  ___/ | |   
 | |  | | | |_) | |/ ____ \| |    _| |_  
 |_|  |_|_|_.__/|_/_/    \_\_|   |_____| 
</g><e>
An alternative implement of Imjad API
Project: https://github.com/mixmoe/HibiAPI
</e></b>"""  # noqa:W291,W293

LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "default": {
            "class": "src.utils.log.LoguruHandler",
        },
    },
    "loggers": {
        "uvicorn.error": {
            "handlers": ["default"],
            "level": LOG_LEVEL,
        },
        "uvicorn.access": {
            "handlers": ["default"],
            "level": LOG_LEVEL,
        },
    },
}

try:
    width, height = get_terminal_size()
except OSError:
    width, height = 0, 0


@click.command(name="HibiAPI")
@click.option(
    "--host",
    "-h",
    default=Config["server"]["host"].as_str(),
    help="listened server address",
    show_default=True,
)
@click.option(
    "--port",
    "-p",
    default=Config["server"]["port"].as_number(),
    help="listened server port",
    show_default=True,
)
@click.option(
    "--workers", "-w", default=1, help="amount of server workers", show_default=True
)
@click.option(
    "--reload",
    "-r",
    default=DEBUG,
    help="automatic reload while file changes",
    show_default=True,
    is_flag=True,
)
def main(host: str, port: int, workers: int, reload: bool):
    logger.warning("\n".join(i.center(width) for i in COPYRIGHT.splitlines()))
    logger.info("HibiAPI version: <g><b>%s</b></g>" % VERSION)
    logger.info(
        "Server is running under <b>%s</b> mode!"
        % ("<r>debug</r>" if DEBUG else "<g>production</g>")
    )
    uvicorn.run(
        "main:AppRoot",
        host=host,
        port=port,
        debug=DEBUG,
        access_log=False,
        log_config=LOG_CONFIG,
        workers=workers,
        reload=reload,
        forwarded_allow_ips=Config["server"]["allowed-forward"].get(
            Optional[str]  # type:ignore
        ),
    )


if __name__ == "__main__":
    main()
