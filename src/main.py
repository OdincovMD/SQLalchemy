from queries.orm import SyncOrm
from queries.core import SyncCore
import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))

# SyncCore.create_tables()
# SyncCore.insert_data()
# SyncCore.select_workers()
# SyncCore.update_worker()
# SyncCore.insert_resumes()

SyncOrm.create_tables()
SyncOrm.insert_data()
# SyncOrm.select_data()
SyncOrm.update_worker()
SyncOrm.insert_resumes()
# SyncOrm.select_resumes_avg()
# SyncOrm.select_data()
# SyncOrm.join_cte_subquery_window_func()
# SyncOrm.select_workers_with_joined_relationship()
# SyncOrm.select_workers_with_condition_relationship()
SyncOrm.select_workers_with_contains_eager_relationship()

