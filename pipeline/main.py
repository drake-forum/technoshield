#!/usr/bin/env python3

import os
import time
import logging
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

# Import pipeline components
from pipeline.utils.logging_config import setup_logging, get_logger
from pipeline.utils.metrics_updater import start_metrics_updater

# Setup logging
setup_logging()
logger = get_logger("pipeline")

# Import pipeline components
from pipeline.ingest import data_collector
from pipeline.process import event_processor
from pipeline.models import threat_detector
from pipeline.utils import db_connector, config


def main():
    """Main entry point for the TECHNOSHIELD data processing pipeline."""
    logger.info("Starting TECHNOSHIELD data processing pipeline")
    
    try:
        # Start metrics updater for periodic metrics updates
        start_metrics_updater(update_interval=60)
        logger.info("Started metrics updater")
        
        # Initialize database connection
        db = db_connector.DatabaseConnector()
        logger.info("Database connection established")
        
        # Load configuration
        pipeline_config = config.load_config()
        logger.info(f"Loaded configuration with {len(pipeline_config['data_sources'])} data sources")
        
        # Main processing loop
        while True:
            start_time = datetime.now()
            logger.info(f"Starting processing cycle at {start_time}")
            
            try:
                # Step 1: Collect data from sources
                raw_data = data_collector.collect_from_all_sources(pipeline_config['data_sources'])
                logger.info(f"Collected {len(raw_data)} raw events from data sources")
                
                # Step 2: Process and normalize events
                processed_events = event_processor.process_events(raw_data)
                logger.info(f"Processed and normalized {len(processed_events)} events")
                
                # Step 3: Analyze events for threats
                alerts = threat_detector.detect_threats(processed_events)
                logger.info(f"Generated {len(alerts)} security alerts")
                
                # Step 4: Store results in database
                if alerts:
                    db.store_alerts(alerts)
                    logger.info(f"Stored {len(alerts)} alerts in database")
                
                # Calculate processing time and sleep if needed
                processing_time = (datetime.now() - start_time).total_seconds()
                logger.info(f"Processing cycle completed in {processing_time:.2f} seconds")
                
                # Sleep to maintain the desired processing interval
                interval = pipeline_config.get('processing_interval_seconds', 60)
                if processing_time < interval:
                    sleep_time = interval - processing_time
                    logger.debug(f"Sleeping for {sleep_time:.2f} seconds")
                    time.sleep(sleep_time)
                    
            except Exception as e:
                logger.error(f"Error in processing cycle: {str(e)}")
                # Sleep for a short time before retrying
                time.sleep(10)
                
    except KeyboardInterrupt:
        logger.info("Pipeline stopped by user")
    except Exception as e:
        logger.critical(f"Critical error in pipeline: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)