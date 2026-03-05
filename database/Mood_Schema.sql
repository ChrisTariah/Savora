USE Savora;

-- Adds moods to recipes for spotify integration
ALTER TABLE Recipe 
ADD mood ENUM('default', 'etc') NOT NULL;   -- Replace with appropriate values. 
                                            -- Note that the first value will be the default. 