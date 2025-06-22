"""
Database query utilities for user portfolios and holdings
"""
import sqlite3
from pathlib import Path
from typing import List, Dict, Any

DB_DIR = Path(__file__).parent
DB_FILE = DB_DIR / "fintech.db"

def get_user_by_email(email: str) -> Dict[str, Any]:
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = ?", (email,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None

def get_user_portfolios(user_id: int) -> List[Dict[str, Any]]:
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM portfolios WHERE user_id = ?", (user_id,))
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_portfolio_holdings(portfolio_id: int) -> List[Dict[str, Any]]:
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('''
        SELECT h.*, s.ticker, s.name, s.current_price
        FROM portfolio_holdings h
        JOIN stocks s ON h.stock_id = s.stock_id
        WHERE h.portfolio_id = ?
    ''', (portfolio_id,))
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]
