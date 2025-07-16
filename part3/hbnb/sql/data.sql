INSERT INTO users (
    id, first_name, last_name, email, password, is_admin
) VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$JgS3zk1MaQowLOJ7vEvRu.uHvKItBfvY2zU9gD8QzjDfvbI9xMoIq',  -- exemple de hash bcrypt pour 'admin1234'
    TRUE
);

INSERT INTO amenities (id, name) VALUES
('e6a3cf64-ec8e-4cc3-b7f6-e506893cc9db', 'Wi-Fi'),
('b9b67f9b-d793-4d6c-bb71-120a5a96b231', 'Piscine'),
('cc12b69a-2e57-445f-b9ce-96d57652cb63', 'Climatisation');