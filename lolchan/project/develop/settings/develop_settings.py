from ievv_opensource.utils import ievvdevrun
from ievv_opensource.utils import ievvbuildstatic
from .developsettings_common import *


IEVVTASKS_DEVRUN_RUNNABLES = {
    'default': ievvdevrun.config.RunnableThreadList(
        ievvdevrun.runnables.dbdev_runserver.RunnableThread(),
        ievvdevrun.runnables.django_runserver.RunnableThread(),
    ),
}
