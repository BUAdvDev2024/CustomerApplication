-- SQLite
-- Create the 'items' table
CREATE TABLE items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL CHECK (price >= 0),
    category TEXT NOT NULL
);

-- Create the 'order_items' table
CREATE TABLE order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    modifications TEXT,
    FOREIGN KEY (order_id) REFERENCES orders (order_id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES items (id) ON DELETE CASCADE
);

-- Create the 'orders' table
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    order_date DATE NOT NULL,
    order_status TEXT NOT NULL CHECK (order_status IN ('PENDING', 'IN-PROGRESS', 'COMPLETED', 'OUT-FOR-DELIVERY', 'DELIVERED', 'FAILED', 'SERVED')),
    order_type TEXT NOT NULL CHECK (order_type IN ('EAT IN', 'TAKEAWAY', 'DELIVERY')),
    table_number INTEGER,
    price REAL NOT NULL CHECK (price >= 0),
    branch_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- Create the 'users' table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    role TEXT NOT NULL
);