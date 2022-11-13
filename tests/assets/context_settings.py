from factotum import *

cli = Factum(
    context_settings=Context.settings(
        help_option_names=["--show-help"],
    ),
)
