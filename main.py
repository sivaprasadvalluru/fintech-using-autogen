#!/usr/bin/env python
"""
Fintech-AutoGen Application
Main entry point for the application
"""

# Import necessary components
from fintech_autogen.database import db_setup
from fintech_autogen.knowledge_base import kb_setup

def initialize_app():
    """Initialize the application components"""
    print("Initializing Fintech-AutoGen Application...")
    
    # Setup database
    db_setup.initialize_database()
    
    # Setup knowledge base
    kb_setup.initialize_knowledge_base()
    
    print("Initialization complete!")

def run_app():
    """Run the application"""
    print("Running Fintech-AutoGen Application...")
    # TODO: Implement the main application logic
    
    # For Phase 1, we simply print a status message
    print("Phase 1 setup complete. Application components initialized.")

if __name__ == "__main__":
    initialize_app()
    run_app() 