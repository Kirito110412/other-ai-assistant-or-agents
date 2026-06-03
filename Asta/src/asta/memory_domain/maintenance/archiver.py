import os
import time
import logging

logger = logging.getLogger("Archiver")

class Archiver:
    """
    Compresses stale, unused context.
    """
    def __init__(self, storage_dir="~/.personalos/memory_graph", cold_storage_dir="~/.personalos/archive"):
        self.storage_dir = os.path.expanduser(storage_dir)
        self.cold_storage_dir = os.path.expanduser(cold_storage_dir)
        os.makedirs(self.cold_storage_dir, exist_ok=True)

    async def run_archive_cycle(self, max_age_days=90):
        """
        Moves nodes untouched for a given period to cold storage, but maintains
        the vector embedding so the abstract lesson is never lost.
        """
        logger.info(f"Scanning for memories older than {max_age_days} days...")

        if not os.path.exists(self.storage_dir):
            return

        md_files = [f for f in os.listdir(self.storage_dir) if f.endswith(".md")]
        current_time = time.time()
        archived_count = 0

        for file in md_files:
            file_path = os.path.join(self.storage_dir, file)
            # Check last access or modified time
            file_age_days = (current_time - os.path.getmtime(file_path)) / (86400)

            if file_age_days > max_age_days:
                # Move to cold storage
                cold_path = os.path.join(self.cold_storage_dir, file)
                os.rename(file_path, cold_path)
                archived_count += 1
                logger.info(f"Archived {file} (Age: {file_age_days:.1f} days)")

        logger.info(f"Archive cycle complete. {archived_count} files moved to cold storage.")
