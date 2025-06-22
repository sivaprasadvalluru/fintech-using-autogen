"""
Database module for Fintech-AutoGen Application
"""

# Import the initialize_database function
def initialize_database():
    """
    Initialize the database with schema and sample data
    
    This function creates the necessary tables and populates
    them with sample data for demonstration purposes.
    """
    from fintech_autogen.database.db_setup import initialize_database as init_db
    return init_db()

__all__ = ["initialize_database"] 