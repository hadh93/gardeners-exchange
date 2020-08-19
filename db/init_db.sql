INSERT INTO users (username, email, pass, address_id, city, zipcode, country, state, other_address_details,
                             rating) VALUES ('sbutz', 'seymourbutz@example.com', 'pass', '1979 S Main St', 'Upland', 46989,
                                             'United States', 'IN', 'N/A', 2);
INSERT INTO users (username, email, pass, address_id, city, zipcode, country, state, other_address_details,
                             rating) VALUES ('dthomas', 'dfoohy@example.com', 'pass', '5775 Coventry Ln', 'Fort Wayne', 46815,
                                             'United States', 'IN', 'N/A', 4);
INSERT INTO users (username, email, pass, address_id, city, zipcode, country, state, other_address_details,
                             rating) VALUES ('nurk', 'nerd4christ@example.com', 'pass', '301 E Main St', 'Gas City', 46933,
                                             'United States', 'IN', 'N/A', 5);
INSERT INTO users (username, email, pass, address_id, city, zipcode, country, state, other_address_details,
                             rating) VALUES ('drwhite', 'artwhite@example.com', 'pass', '506 E Van Cleve St', 'Hartford City', 47348,
                                             'United States', 'IN', 'N/A', 3);
INSERT INTO users (username, email, pass, address_id, city, zipcode, country, state, other_address_details,
                             rating) VALUES ('MrPresident', 'plowellh@example.com', 'pass', '236 W Reade Ave', 'Upland', 46989,
                                             'United States', 'IN', 'N/A', 1);
INSERT INTO users (username, email, pass, address_id, city, zipcode, country, state, other_address_details,
                             rating) VALUES ('ProfH', 'erichernandez@example.com', 'pass', '7230 County Rd 400 S', 'Upland',
                                             46989, 'United States', 'IN', 'N/A', 1);

INSERT INTO transactions (id, buyer_name, seller_name, timestamp) VALUES (1, 'MrPresident', 'sbutz', 12345);
INSERT INTO transactions (id, buyer_name, seller_name, timestamp) VALUES (2, 'dthomas', 'drwhite', 23451);
INSERT INTO transactions (id, buyer_name, seller_name, timestamp) VALUES (3, 'nurk', 'MrPresident', 25165);
INSERT INTO transactions (id, buyer_name, seller_name, timestamp) VALUES (4, 'sbutz', 'dthomas', 28435);
INSERT INTO transactions (id, buyer_name, seller_name, timestamp) VALUES (5, 'drwhite', 'nurk', 16845);
INSERT INTO transactions (id, buyer_name, seller_name, timestamp) VALUES (6, 'nurk', 'sbutz', 26743);
INSERT INTO transactions (id, buyer_name, seller_name, timestamp) VALUES (7, 'dthomas', 'MrPresident', 19354);
INSERT INTO transactions (id, buyer_name, seller_name, timestamp) VALUES (8, 'MrPresident', 'drwhite', 14236);
INSERT INTO transactions (id, buyer_name, seller_name, timestamp) VALUES (9, 'MrPresident', 'dthomas', 14368);
INSERT INTO transactions (id, buyer_name, seller_name, timestamp) VALUES (10, 'nurk', 'MrPresident', 13587);
INSERT INTO transactions (id, buyer_name, seller_name, timestamp) VALUES (11, 'drwhite', 'dthomas', 18520);
INSERT INTO transactions (id, buyer_name, seller_name, timestamp) VALUES (12, 'drwhite', 'drwhite', 17456);
INSERT INTO transactions (id, buyer_name, seller_name, timestamp) VALUES (13, 'sbutz', 'dthomas', 16875);
INSERT INTO transactions (id, buyer_name, seller_name, timestamp) VALUES (14, 'drwhite', 'MrPresident', 29635);
INSERT INTO transactions (id, buyer_name, seller_name, timestamp) VALUES (15, 'sbutz', 'nurk', 28453);
INSERT INTO transactions (id, buyer_name, seller_name, timestamp) VALUES (16, 'nurk', 'ProfH', 25465);
INSERT INTO transactions (id, buyer_name, seller_name, timestamp) VALUES (17, 'ProfH', 'MrPresident', 15869);
INSERT INTO transactions (id, buyer_name, seller_name, timestamp) VALUES (18, 'ProfH', 'drwhite', 29503);
INSERT INTO transactions (id, buyer_name, seller_name, timestamp) VALUES (19, 'ProfH', 'sbutz', 15869);

INSERT INTO listings (id, name, price_per_unit, unit, seller_name, harvested, quantity) VALUES (DEFAULT, 'Green Beans', 4, 'lb', 'drwhite', '5/9/18', 2);
INSERT INTO listings (id, name, price_per_unit, unit, seller_name, harvested, quantity) VALUES (DEFAULT, 'Kiwis', 5, 'lb', 'dthomas', '5/9/18', 3);
INSERT INTO listings (id, name, price_per_unit, unit, seller_name, harvested, quantity) VALUES (DEFAULT, 'Apple Pie', 10, 'pie', 'MrPresident', '5/9/18', 5);
INSERT INTO listings (id, name, price_per_unit, unit, seller_name, harvested, quantity) VALUES (DEFAULT, 'Chocolate Chip Cookies', 1, 'cookie', 'nurk', '5/9/18', 45);
INSERT INTO listings (id, name, price_per_unit, unit, seller_name, harvested, quantity) VALUES (DEFAULT, 'Raspberries', 7, 'bushel', 'ProfH', '5/9/18', 32);
INSERT INTO listings (id, name, price_per_unit, unit, seller_name, harvested, quantity) VALUES (DEFAULT, 'Apple Butter', 3, 'jar', 'sbutz', '5/9/18', 10);
INSERT INTO listings (id, name, price_per_unit, unit, seller_name, harvested, quantity) VALUES (DEFAULT, 'Grapes', 1, 'cluster', 'ProfH', '5/9/18', 100);
INSERT INTO listings (id, name, price_per_unit, unit, seller_name, harvested, quantity) VALUES (DEFAULT, 'Beef Jerky', 17, 'lb', 'drwhite', '5/9/18', 232);

INSERT INTO photos (id) VALUES (1);
INSERT INTO photos (id) VALUES (2);
INSERT INTO photos (id) VALUES (3);
INSERT INTO photos (id) VALUES (4);
INSERT INTO photos (id) VALUES (5);
INSERT INTO photos (id) VALUES (6);
INSERT INTO photos (id) VALUES (7);
INSERT INTO photos (id) VALUES (8);
INSERT INTO photos (id) VALUES (9);
INSERT INTO photos (id) VALUES (10);
INSERT INTO photos (id) VALUES (11);
INSERT INTO photos (id) VALUES (12);
INSERT INTO photos (id) VALUES (13);
INSERT INTO photos (id) VALUES (14);

INSERT INTO user_photo (photo_id, user_id) VALUES (1, 'drwhite');
INSERT INTO user_photo (photo_id, user_id) VALUES (2, 'dthomas');
INSERT INTO user_photo (photo_id, user_id) VALUES (3, 'MrPresident');
INSERT INTO user_photo (photo_id, user_id) VALUES (4, 'nurk');
INSERT INTO user_photo (photo_id, user_id) VALUES (5, 'ProfH');
INSERT INTO user_photo (photo_id, user_id) VALUES (6, 'sbutz');

INSERT INTO listing_photo (photo_id, listing_id) VALUES (10, 4);
INSERT INTO listing_photo (photo_id, listing_id) VALUES (12, 1);
INSERT INTO listing_photo (photo_id, listing_id) VALUES (11, 7);
INSERT INTO listing_photo (photo_id, listing_id) VALUES (13, 2);
INSERT INTO listing_photo (photo_id, listing_id) VALUES (9, 8);
INSERT INTO listing_photo (photo_id, listing_id) VALUES (8, 3);
INSERT INTO listing_photo (photo_id, listing_id) VALUES (7, 6);
INSERT INTO listing_photo (photo_id, listing_id) VALUES (14, 5);
