CREATE OR REPLACE FUNCTION get_top_places_by_province(limit_param INTEGER DEFAULT 5)
RETURNS TABLE (
    id UUID,
    place_id INTEGER,
    place_name VARCHAR,
    category VARCHAR,
    description TEXT,
    province VARCHAR,
    avg_rating NUMERIC,
    rating_count BIGINT,
    rank BIGINT
)
LANGUAGE SQL
STABLE
AS $$
    SELECT
        *
    FROM
        (
            SELECT
                p.id,
                p.place_id,
                p.place_name,
                p.category,
                p.description,
                p.province,
                AVG(upr.rating) AS avg_rating,
                COUNT(upr.rating) AS rating_count,
                ROW_NUMBER() OVER (
                    PARTITION BY p.province
                    ORDER BY
                        AVG(upr.rating) DESC,
                        COUNT(upr.rating) DESC
                ) AS rank
            FROM
                place p
                LEFT JOIN user_place_rating upr ON p.place_id = upr.place_id
            GROUP BY
                p.place_id,
                p.place_name,
                p.category,
                p.description,
                p.province,
                p.id
        ) ranked
    WHERE
        rank <= limit_param
    ORDER BY
        province,
        rank;
$$;
