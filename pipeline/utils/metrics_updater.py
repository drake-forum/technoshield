#!/usr/bin/env python3

import time
import threading
import logging
from typing import Dict, Any

from pipeline.utils.metrics import update_data_freshness
from pipeline.utils.logging_config import get_logger

logger = get_logger("pipeline.metrics")


class MetricsUpdater:
    """A class to periodically update metrics that need regular refreshing"""
    
    def __init__(self, update_interval: int = 60):
        """Initialize the metrics updater
        
        Args:
            update_interval: Time in seconds between updates
        """
        self.update_interval = update_interval
        self.running = False
        self.thread = None
    
    def start(self):
        """Start the metrics updater thread"""
        if self.running:
            logger.warning("Metrics updater is already running")
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._update_loop, daemon=True)
        self.thread.start()
        logger.info(f"Started metrics updater thread with {self.update_interval}s interval")
    
    def stop(self):
        """Stop the metrics updater thread"""
        if not self.running:
            logger.warning("Metrics updater is not running")
            return
        
        self.running = False
        if self.thread:
            self.thread.join(timeout=5.0)
            if self.thread.is_alive():
                logger.warning("Metrics updater thread did not terminate cleanly")
            else:
                logger.info("Stopped metrics updater thread")
    
    def _update_loop(self):
        """Main update loop that runs in a separate thread"""
        while self.running:
            try:
                # Update data freshness metrics
                update_data_freshness()
                
                # Add more metric updates here as needed
                
            except Exception as e:
                logger.error(f"Error in metrics updater: {str(e)}")
            
            # Sleep for the update interval
            time.sleep(self.update_interval)


# Singleton instance
_updater = None


def start_metrics_updater(update_interval: int = 60):
    """Start the metrics updater with the specified interval"""
    global _updater
    
    if _updater is None:
        _updater = MetricsUpdater(update_interval)
    
    _updater.start()
    return _updater


def stop_metrics_updater():
    """Stop the metrics updater if it's running"""
    global _updater
    
    if _updater is not None:
        _updater.stop()