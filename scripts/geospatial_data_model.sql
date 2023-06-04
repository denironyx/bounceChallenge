-- Create the Users table
CREATE TABLE Users (
    user_id SERIAL PRIMARY KEY, 
    user_name VARCHAR(50) NOT NULL,
    full_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL
);

-- Create the locations
CREATE TABLE CheckinLocation (
    location_id SERIAL PRIMARY KEY,
    address_name VARCHAR(100) NOT NULL,
    geom GEOMETRY(POINT, 4326) NOT NULL
);

-- CREATE the checkin table
CREATE TABLE Checkins (
    checkin_id SERIAL PRIMARY KEY, 
    user_id INT, 
    location_id INT,
    checkin_time TIMESTAMP NOT NULL, 
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (location_id) REFERENCES CheckinLocation(location_id)
);


-- Create the adminboundary
CREATE TABLE AdminBoundary (
    admin_id SERIAL PRIMARY KEY,
    location_id INT,
    postal_code VARCHAR(10) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    geom GEOMETRY(POLYGON, 4326) NOT NULL,
    FOREIGN KEY (location_id) REFERENCES CheckinLocation(location_id)
);

--- Heatmap count

SELECT
    ab.admin_id,
    ab.postal_code,
    ab.city,
    ab.state,
    ab.geom,
    COUNT(DISTINCT c.user_id) AS checkin_users_count
FROM
    AdminBoundary ab
JOIN
    CheckinLocation cl ON ST_Intersects(ab.geom, cl.geom)
JOIN
    Checkins c ON cl.location_id = c.location_id
GROUP BY
    ab.admin_id, ab.postal_code, ab.city, ab.state, ab.geom;
