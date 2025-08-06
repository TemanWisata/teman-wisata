CREATE OR REPLACE FUNCTION get_top_places_rating(limit_param INTEGER DEFAULT 10)
RETURNS TABLE (
    id UUID,
    place_id INTEGER,
    place_name VARCHAR,
    category VARCHAR,
    description TEXT,
    province VARCHAR,
    avg_rating NUMERIC,
    rating_count BIGINT
)
LANGUAGE SQL
STABLE
AS $$
    SELECT
        p.id,
        p.place_id,
        p.place_name,
        p.category,
        p.description,
        p.province,
        AVG(upr.rating) AS avg_rating,
        COUNT(upr.rating) AS rating_count
    FROM
        user_place_rating upr
        JOIN place p ON upr.place_id = p.place_id
    GROUP BY
        p.id,
        p.place_id,
        p.place_name,
        p.category,
        p.province,
        p.description
    ORDER BY
        avg_rating DESC,
        rating_count DESC
    LIMIT limit_param;
$$;
