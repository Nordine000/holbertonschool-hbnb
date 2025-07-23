SELECT id, email, is_admin FROM users WHERE email = 'admin@hbnb.io';

SELECT id, name FROM amenities;

INSERT INTO reviews (
    id, text, rating, user_id, place_id
) VALUES (
    'a1c2d3e4-5678-90ab-cdef-1234567890ab',
    'Lieu exceptionnel !',
    5,
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'example-place-id'  -- Remplace par un vrai ID si tu en as un
);

SELECT * FROM reviews;

DELETE FROM reviews WHERE id = 'a1c2d3e4-5678-90ab-cdef-1234567890ab';