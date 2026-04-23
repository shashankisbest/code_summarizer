from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

class DatabaseManager:
    def __init__(self, db_name):
        """Initialize database connection"""
        self.db_name = db_name
        self.conn = None
    
    def connect(self):
        """Connect to SQLite database"""
        self.conn = sqlite3.connect(self.db_name)
    
    def get_user(self, user_id):
        """Retrieve user from database"""
        cursor = self.conn.cursor()
        query = f"SELECT * FROM users WHERE id = {user_id}"  # Security issue!
        cursor.execute(query)
        return cursor.fetchone()

@app.route('/api/users/<user_id>')
def get_user_endpoint(user_id):
    """API endpoint to get user data"""
    db = DatabaseManager('users.db')
    db.connect()
    user = db.get_user(user_id)
    return jsonify(user)

if __name__ == '__main__':
    app.run(debug=True)