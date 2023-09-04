import typer

from pysqlrecon.logger import logger
from pysqlrecon.lib import PySqlRecon

app = typer.Typer()
COMMAND_NAME = "enableole"
HELP = "[red][PRIV][/] Enable OLE automation procedures [I,L]"
LINK_COMPATIBLE = True
IMPERSONATE_COMPATIBLE = True


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):

    pysqlrecon: PySqlRecon = ctx.obj['pysqlrecon']
    use_basic_tables = ctx.obj['basic_tables']

    # verify opts are compatible with module before connecting
    if not PySqlRecon.validate_opts(
        LINK_COMPATIBLE,
        IMPERSONATE_COMPATIBLE,
        pysqlrecon.link,
        pysqlrecon.impersonate
    ):
        exit()

    pysqlrecon.connect()

    if pysqlrecon.link is not None:        
        if not pysqlrecon.validate_link():
            logger.warning(f"{pysqlrecon.link} is not a linked server")
            pysqlrecon.disconnect()
            exit()

        logger.info(f"Enabling OLE automation procedures on {pysqlrecon.link} via {pysqlrecon.target}")
        pysqlrecon.linked_module_toggle("OLE Automation Procedures", "1")

        pysqlrecon.linked_check_module("OLE Automation Procedures")
        pysqlrecon.print_results(use_basic_tables)

    else:
        logger.info(f"Enabling OLE automation procedures on {pysqlrecon.target}")
        pysqlrecon.module_toggle("OLE Automation Procedures", "1")
        pysqlrecon.check_module("OLE Automation Procedures")
        pysqlrecon.print_results(use_basic_tables)

    pysqlrecon.disconnect()