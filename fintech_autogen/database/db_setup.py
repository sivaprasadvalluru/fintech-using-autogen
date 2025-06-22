import os
import sqlite3
from pathlib import Path
import datetime
import logging

# Define database directory and file
DB_DIR = Path(__file__).parent
DB_FILE = DB_DIR / "fintech.db"

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def initialize_database():
    logger = logging.getLogger("db_setup")
    logger.info(f"Initializing database at {DB_FILE}...")
    
    # Create directory if it doesn't exist
    os.makedirs(DB_DIR, exist_ok=True)
    
    # Connect to the database
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Helper to check if a table exists


    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        email TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        role TEXT CHECK(role IN ('admin', 'user', 'analyst')) NOT NULL DEFAULT 'user',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Create portfolios table with cash balance
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS portfolios (
        portfolio_id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        description TEXT,
        cash_balance REAL NOT NULL DEFAULT 10000.0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    ''')

    # Create stocks table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS stocks (
        stock_id INTEGER PRIMARY KEY,
        ticker TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        sector TEXT,
        industry TEXT,
        current_price REAL,
        previous_close_price REAL,
        dividend_yield REAL,
        market_cap REAL,
        pe_ratio REAL,
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Create portfolio_holdings table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS portfolio_holdings (
        holding_id INTEGER PRIMARY KEY,
        portfolio_id INTEGER NOT NULL,
        stock_id INTEGER NOT NULL,
        shares REAL NOT NULL,
        avg_purchase_price REAL NOT NULL,
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (portfolio_id) REFERENCES portfolios(portfolio_id) ON DELETE CASCADE,
        FOREIGN KEY (stock_id) REFERENCES stocks(stock_id),
        UNIQUE(portfolio_id, stock_id)
    )
    ''')

    # Create transactions table with more details
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        transaction_id INTEGER PRIMARY KEY,
        portfolio_id INTEGER NOT NULL,
        stock_id INTEGER NOT NULL,
        transaction_type TEXT CHECK(transaction_type IN ('buy', 'sell', 'dividend', 'deposit', 'withdrawal')) NOT NULL,
        shares REAL,
        price_per_share REAL,
        total_amount REAL NOT NULL,
        fees REAL DEFAULT 0.0,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        notes TEXT,
        FOREIGN KEY (portfolio_id) REFERENCES portfolios(portfolio_id) ON DELETE CASCADE,
        FOREIGN KEY (stock_id) REFERENCES stocks(stock_id)
    )
    ''')

    # Create portfolio_performance table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS portfolio_performance (
        performance_id INTEGER PRIMARY KEY,
        portfolio_id INTEGER NOT NULL,
        date DATE NOT NULL,
        total_value REAL NOT NULL,
        daily_change_pct REAL,
        ytd_change_pct REAL,
        cash_balance REAL NOT NULL,
        FOREIGN KEY (portfolio_id) REFERENCES portfolios(portfolio_id) ON DELETE CASCADE,
        UNIQUE(portfolio_id, date)
    )
    ''')

    # Create stock_historical_prices table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS stock_historical_prices (
        price_id INTEGER PRIMARY KEY,
        stock_id INTEGER NOT NULL,
        date DATE NOT NULL,
        open_price REAL NOT NULL,
        high_price REAL NOT NULL,
        low_price REAL NOT NULL,
        close_price REAL NOT NULL,
        volume INTEGER NOT NULL,
        FOREIGN KEY (stock_id) REFERENCES stocks(stock_id),
        UNIQUE(stock_id, date)
    )
    ''')

    # Create watchlists table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS watchlists (
        watchlist_id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
        UNIQUE(user_id, name)
    )
    ''')

    # Create watchlist_items table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS watchlist_items (
        item_id INTEGER PRIMARY KEY,
        watchlist_id INTEGER NOT NULL,
        stock_id INTEGER NOT NULL,
        added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        price_target REAL,
        notes TEXT,
        FOREIGN KEY (watchlist_id) REFERENCES watchlists(watchlist_id) ON DELETE CASCADE,
        FOREIGN KEY (stock_id) REFERENCES stocks(stock_id),
        UNIQUE(watchlist_id, stock_id)
    )
    ''')
    
    # Insert sample data for demonstration purposes
    seed_sample_data(cursor)
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    logger.info("Database schema created and initialized.")


def seed_sample_data(cursor):
    """Seed the database with sample data"""
    # Check if we already have data
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    
    if user_count > 0:
        print("Sample data already exists, skipping seeding.")
        return
    
    print("Seeding database with sample data...")
    
    # Add sample users
    cursor.execute(
        "INSERT INTO users (email, name, role) VALUES (?, ?, ?)",
        ("admin@example.com", "Admin User", "admin")
    )
    cursor.execute(
        "INSERT INTO users (email, name, role) VALUES (?, ?, ?)",
        ("user@example.com", "Regular User", "user")
    )
    cursor.execute(
        "INSERT INTO users (email, name, role) VALUES (?, ?, ?)",
        ("analyst@example.com", "Market Analyst", "analyst")
    )
    
    # Add sample portfolios with initial cash balance
    cursor.execute(
        "INSERT INTO portfolios (user_id, name, description, cash_balance) VALUES (?, ?, ?, ?)",
        (1, "Admin Portfolio", "Portfolio managed by admin", 25000.50)
    )
    cursor.execute(
        "INSERT INTO portfolios (user_id, name, description, cash_balance) VALUES (?, ?, ?, ?)",
        (2, "Growth Portfolio", "High growth tech stocks", 15000.75)
    )
    cursor.execute(
        "INSERT INTO portfolios (user_id, name, description, cash_balance) VALUES (?, ?, ?, ?)",
        (2, "Default Portfolio", "Focus on dividend income", 10000.25)
    )
    
    # Add sample stocks with more data
    sample_stocks = [
        ("AAPL", "Apple Inc.", "Technology", "Consumer Electronics", 180.75, 179.80, 0.58, 2800000000000, 30.2),
        ("MSFT", "Microsoft Corporation", "Technology", "Software", 330.22, 328.90, 0.77, 2400000000000, 35.8),
        ("GOOGL", "Alphabet Inc.", "Technology", "Internet Services", 140.35, 139.70, 0.0, 1750000000000, 25.4),
        ("AMZN", "Amazon.com Inc.", "Consumer Cyclical", "E-commerce", 135.07, 134.25, 0.0, 1400000000000, 42.6),
        ("JNJ", "Johnson & Johnson", "Healthcare", "Pharmaceuticals", 155.67, 156.10, 3.2, 380000000000, 15.8),
        ("JPM", "JPMorgan Chase & Co.", "Financial Services", "Banking", 145.89, 144.95, 2.5, 425000000000, 12.3),
        ("V", "Visa Inc.", "Financial Services", "Payment Processing", 270.99, 269.85, 0.8, 570000000000, 31.4),
        ("PG", "Procter & Gamble Co.", "Consumer Defensive", "Household Products", 160.21, 159.75, 2.4, 380000000000, 26.7),
        ("DIS", "The Walt Disney Company", "Communication Services", "Entertainment", 105.90, 103.25, 0.0, 195000000000, 70.2),
        ("NVDA", "NVIDIA Corporation", "Technology", "Semiconductors", 440.55, 435.20, 0.05, 1200000000000, 60.8),
        ("KO", "The Coca-Cola Company", "Consumer Defensive", "Beverages", 62.45, 62.30, 2.85, 270000000000, 25.6),
        ("VZ", "Verizon Communications", "Communication Services", "Telecommunications", 40.80, 40.65, 6.70, 170000000000, 8.4)
    ]
    
    for stock in sample_stocks:
        cursor.execute(
            "INSERT INTO stocks (ticker, name, sector, industry, current_price, previous_close_price, dividend_yield, market_cap, pe_ratio) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            stock
        )
    
    # Add sample holdings with updated timestamps
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sample_holdings = [
        (1, 1, 10.0, 175.50, current_time),  # Admin portfolio: AAPL
        (1, 2, 5.0, 320.25, current_time),   # Admin portfolio: MSFT
        (1, 5, 8.0, 152.30, current_time),   # Admin portfolio: JNJ
        (2, 1, 3.0, 178.20, current_time),   # Growth portfolio: AAPL
        (2, 4, 2.0, 130.45, current_time),   # Growth portfolio: AMZN
        (2, 10, 1.0, 420.75, current_time),  # Growth portfolio: NVDA
        (3, 5, 12.0, 154.80, current_time),  # Default portfolio: JNJ
        (3, 11, 20.0, 60.25, current_time),  # Default portfolio: KO
        (3, 12, 15.0, 39.90, current_time)   # Default portfolio: VZ
    ]
    
    for holding in sample_holdings:
        cursor.execute(
            "INSERT INTO portfolio_holdings (portfolio_id, stock_id, shares, avg_purchase_price, last_updated) VALUES (?, ?, ?, ?, ?)",
            holding
        )
    
    # Add sample transactions with more details
    one_week_ago = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')
    three_days_ago = (datetime.datetime.now() - datetime.timedelta(days=3)).strftime('%Y-%m-%d %H:%M:%S')
    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
    
    sample_transactions = [
        # Initial deposits
        (1, 1, "deposit", None, None, 50000.0, 0.0, one_week_ago, "Initial deposit"),
        (2, 1, "deposit", None, None, 25000.0, 0.0, one_week_ago, "Initial deposit"),
        (3, 1, "deposit", None, None, 30000.0, 0.0, one_week_ago, "Initial deposit"),
        
        # Stock purchases for Admin portfolio
        (1, 1, "buy", 10.0, 175.50, 1755.0, 9.99, one_week_ago, "Initial AAPL purchase"),
        (1, 2, "buy", 5.0, 320.25, 1601.25, 9.99, three_days_ago, "MSFT purchase"),
        (1, 5, "buy", 8.0, 152.30, 1218.40, 9.99, yesterday, "JNJ purchase"),
        
        # Stock purchases for Growth portfolio
        (2, 1, "buy", 3.0, 178.20, 534.60, 9.99, three_days_ago, "AAPL purchase"),
        (2, 4, "buy", 2.0, 130.45, 260.90, 9.99, three_days_ago, "AMZN purchase"),
        (2, 10, "buy", 1.0, 420.75, 420.75, 9.99, yesterday, "NVDA purchase"),
        
        # Stock purchases for Default portfolio
        (3, 5, "buy", 12.0, 154.80, 1857.60, 9.99, one_week_ago, "JNJ purchase for dividends"),
        (3, 11, "buy", 20.0, 60.25, 1205.0, 9.99, three_days_ago, "KO purchase"),
        (3, 12, "buy", 15.0, 39.90, 598.50, 9.99, yesterday, "VZ purchase for high yield"),
        
        # Some dividend payments
        (3, 5, "dividend", 0.0, 0.0, 48.0, 0.0, yesterday, "JNJ quarterly dividend"),
        (3, 11, "dividend", 0.0, 0.0, 35.0, 0.0, yesterday, "KO quarterly dividend")
    ]
    
    for transaction in sample_transactions:
        cursor.execute(
            "INSERT INTO transactions (portfolio_id, stock_id, transaction_type, shares, price_per_share, total_amount, fees, timestamp, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            transaction
        )
    


    
    # Add sample watchlists
    cursor.execute(
        "INSERT INTO watchlists (user_id, name, description) VALUES (?, ?, ?)",
        (1, "Tech Stocks", "Promising technology companies")
    )
    cursor.execute(
        "INSERT INTO watchlists (user_id, name, description) VALUES (?, ?, ?)",
        (2, "Dividend Payers", "Stocks with strong dividend history")
    )
    
    # Add watchlist items
    sample_watchlist_items = [
        (1, 3, 145.0, "Potential breakout candidate"),  # Tech watchlist: GOOGL
        (1, 10, 450.0, "Monitoring for AI developments"),  # Tech watchlist: NVDA
        (2, 6, 150.0, "Potential addition to dividend portfolio"),  # Dividend watchlist: JPM
        (2, 8, 165.0, "Strong dividend history"),  # Dividend watchlist: PG
    ]
    
    for item in sample_watchlist_items:
        cursor.execute(
            "INSERT INTO watchlist_items (watchlist_id, stock_id, price_target, notes) VALUES (?, ?, ?, ?)",
            item
        )
    
    # Add sample portfolio performance data
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    two_days_ago = today - datetime.timedelta(days=2)
    
    sample_performance = [
        (1, two_days_ago.strftime('%Y-%m-%d'), 29450.25, 0.8, 5.2, 25025.45),
        (1, yesterday.strftime('%Y-%m-%d'), 29680.50, 0.78, 6.0, 25035.25),
        (1, today.strftime('%Y-%m-%d'), 29820.75, 0.47, 6.5, 25000.50),
        (2, two_days_ago.strftime('%Y-%m-%d'), 9750.30, 1.2, 3.5, 15020.80),
        (2, yesterday.strftime('%Y-%m-%d'), 9890.45, 1.44, 4.9, 15010.25),
        (2, today.strftime('%Y-%m-%d'), 10025.80, 1.37, 6.3, 15000.75),
        (3, two_days_ago.strftime('%Y-%m-%d'), 19950.75, 0.25, 2.8, 10045.50),
        (3, yesterday.strftime('%Y-%m-%d'), 20050.25, 0.5, 3.3, 10015.75),
        (3, today.strftime('%Y-%m-%d'), 20125.80, 0.38, 3.7, 10000.25)
    ]
    
    for perf in sample_performance:
        cursor.execute(
            "INSERT INTO portfolio_performance (portfolio_id, date, total_value, daily_change_pct, ytd_change_pct, cash_balance) VALUES (?, ?, ?, ?, ?, ?)",
            perf
        )
    
    # Add sample historical stock prices
    for stock_id in range(1, 6):  # First 5 stocks
        for days_back in range(5, 0, -1):
            date = (today - datetime.timedelta(days=days_back)).strftime('%Y-%m-%d')
            base_price = 100 + stock_id * 10  # Different base price for each stock
            daily_fluctuation = (5 - days_back) * 0.5  # Increasing trend
            
            cursor.execute(
                "INSERT INTO stock_historical_prices (stock_id, date, open_price, high_price, low_price, close_price, volume) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    stock_id,
                    date,
                    base_price - 0.5 + daily_fluctuation,
                    base_price + 1.5 + daily_fluctuation,
                    base_price - 1.0 + daily_fluctuation,
                    base_price + 0.5 + daily_fluctuation,
                    100000 + stock_id * 50000 + days_back * 10000
                )
            )
    
    print("Sample data seeding complete!")


if __name__ == "__main__":
    initialize_database()