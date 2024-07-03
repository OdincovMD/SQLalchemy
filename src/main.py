import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from queries.core import SyncCore
from queries.orm import SyncOrm

# SyncCore.create_tables()
# SyncCore.insert_data()
# SyncCore.select_workers()
# SyncCore.update_worker()


# SyncOrm.create_tables()
# SyncOrm.insert_data()
# SyncOrm.select_data()