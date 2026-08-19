CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'user',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS api_keys (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    api_key VARCHAR(255) NOT NULL,
    quota_used INT DEFAULT 0,
    status VARCHAR(50) DEFAULT "live",
    last_used_data DATE,
    crated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS bot_tele (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    bot_token VARCHAR(255) NOT NULL,
    chatid VARCHAR(100) NOT NULL,
    name VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS youtbe_channels (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    bottele_id INT REFERENCES bot_tele(id) ON DELETE SET NULL,
    channel_id VARCHAR(100) NOT NULL,
    link_channel TEXT,
    avatar_url TEXT,
    last_video_id VARCHAR(100),
    last_published_at TIMESTAMP,
    note TEXT, 
    status VARCHAR(20) DEFAULT 'on', -- on, off
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS notification_logs (
    id SERIAL PRIMARY KEY,
    youtube_id INT REFERENCES youtube_channels(id) ON DELETE CASCADE,
    bottele_id INT REFERENCES bot_tele(id) ON DELETE CASCADE,
    video_id VARCHAR(100), 
    status VARCHAR(50), 
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);