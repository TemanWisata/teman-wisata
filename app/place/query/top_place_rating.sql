SELECT
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
    p.place_id,
    p.place_name,
    p.category,
    p.province,
    p.description
ORDER BY
    avg_rating DESC,
    rating_count DESC
LIMIT
    {limit};
