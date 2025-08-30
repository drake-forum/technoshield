#!/usr/bin/env python3

import os
import logging
from typing import List, Dict, Any
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, JSON, DateTime, Text
from sqlalchemy.sql import select, insert
from datetime import datetime

logger = logging.getLogger("technoshield-pipeline.utils.db")


class DatabaseConnector:
    """Handles database connections and operations for the pipeline."""
    
    def __init__(self):
        """Initialize the database connector using environment variables."""
        self.db_url = self._build_connection_string()
        self.engine = create_engine(self.db_url)
        self.metadata = MetaData()
        self._define_tables()
        
        # Create tables if they don't exist
        self.metadata.create_all(self.engine)
        logger.info("Database connection initialized")
    
    def _build_connection_string(self) -> str:
        """Build a database connection string from environment variables.
        
        Returns:
            Database connection URL string
        """
        db_user = os.environ.get("POSTGRES_USER", "postgres")
        db_password = os.environ.get("POSTGRES_PASSWORD", "postgres")
        db_server = os.environ.get("POSTGRES_SERVER", "localhost")
        db_name = os.environ.get("POSTGRES_DB", "technoshield")
        
        return f"postgresql://{db_user}:{db_password}@{db_server}/{db_name}"
    
    def _define_tables(self):
        """Define the database tables used by the pipeline."""
        # Define the alerts table
        self.alerts_table = Table(
            'alerts',
            self.metadata,
            Column('id', Integer, primary_key=True),
            Column('alert_id', String(50), unique=True, nullable=False),
            Column('title', String(255), nullable=False),
            Column('description', Text),
            Column('severity', String(20), nullable=False),
            Column('source_ip', String(50)),
            Column('event_type', String(50)),
            Column('created_at', DateTime, default=datetime.now),
            Column('updated_at', DateTime, default=datetime.now, onupdate=datetime.now),
            Column('related_events', JSON),
            Column('status', String(20), default='new'),
            Column('details', JSON)
        )
        
        # Define the events table for storing processed events
        self.events_table = Table(
            'events',
            self.metadata,
            Column('id', Integer, primary_key=True),
            Column('event_id', String(50), unique=True, nullable=False),
            Column('timestamp', DateTime),
            Column('source_name', String(100)),
            Column('source_type', String(50)),
            Column('event_type', String(50)),
            Column('severity', String(20)),
            Column('description', Text),
            Column('source_ip', String(50)),
            Column('user', String(100)),
            Column('processed_at', DateTime),
            Column('raw_data', JSON)
        )
    
    def store_alerts(self, alerts: List[Dict[str, Any]]) -> int:
        """Store detected security alerts in the database.
        
        Args:
            alerts: List of alert dictionaries to store
            
        Returns:
            Number of alerts successfully stored
        """
        if not alerts:
            return 0
        
        connection = self.engine.connect()
        count = 0
        
        try:
            for alert in alerts:
                # Check if alert already exists
                query = select([self.alerts_table]).where(self.alerts_table.c.alert_id == alert['alert_id'])
                result = connection.execute(query).fetchone()
                
                if result is None:
                    # Insert new alert
                    insert_stmt = insert(self.alerts_table).values(
                        alert_id=alert['alert_id'],
                        title=alert['title'],
                        description=alert['description'],
                        severity=alert['severity'],
                        source_ip=alert.get('source_ip'),
                        event_type=alert['event_type'],
                        created_at=datetime.now(),
                        updated_at=datetime.now(),
                        related_events=alert.get('related_events', []),
                        status=alert.get('status', 'new'),
                        details=alert.get('details', {})
                    )
                    connection.execute(insert_stmt)
                    count += 1
            
            logger.info(f"Stored {count} new alerts in the database")
            return count
            
        except Exception as e:
            logger.error(f"Error storing alerts in database: {str(e)}")
            return 0
        finally:
            connection.close()
    
    def store_events(self, events: List[Dict[str, Any]]) -> int:
        """Store processed events in the database for historical analysis.
        
        Args:
            events: List of processed event dictionaries to store
            
        Returns:
            Number of events successfully stored
        """
        if not events:
            return 0
        
        connection = self.engine.connect()
        count = 0
        
        try:
            for event in events:
                # Check if event already exists
                query = select([self.events_table]).where(self.events_table.c.event_id == event['event_id'])
                result = connection.execute(query).fetchone()
                
                if result is None:
                    # Parse timestamp if it's a string
                    timestamp = event.get('timestamp')
                    if isinstance(timestamp, str):
                        try:
                            timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                        except (ValueError, TypeError):
                            timestamp = datetime.now()
                    
                    # Insert new event
                    insert_stmt = insert(self.events_table).values(
                        event_id=event['event_id'],
                        timestamp=timestamp,
                        source_name=event.get('source', {}).get('name'),
                        source_type=event.get('source', {}).get('type'),
                        event_type=event.get('event_type'),
                        severity=event.get('severity'),
                        description=event.get('description'),
                        source_ip=event.get('source_ip'),
                        user=event.get('user'),
                        processed_at=event.get('processed_at'),
                        raw_data=event.get('raw_data')
                    )
                    connection.execute(insert_stmt)
                    count += 1
            
            logger.info(f"Stored {count} new events in the database")
            return count
            
        except Exception as e:
            logger.error(f"Error storing events in database: {str(e)}")
            return 0
        finally:
            connection.close()