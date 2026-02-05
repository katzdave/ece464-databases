CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE directories (
    directory_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    parent_directory_id INT REFERENCES directories(directory_id), -- NULL means root
    owner_id INT NOT NULL REFERENCES users(user_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE files (
    file_id UUID PRIMARY KEY, -- Reference to external cloud storage
    name VARCHAR(255) NOT NULL,
    size_bytes BIGINT NOT NULL,
    directory_id INT NOT NULL REFERENCES directories(directory_id),
    owner_id INT NOT NULL REFERENCES users(user_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE file_shares (
    file_id UUID NOT NULL REFERENCES files(file_id),
    shared_with_user_id INT NOT NULL REFERENCES users(user_id),
    shared_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (file_id, shared_with_user_id)
);