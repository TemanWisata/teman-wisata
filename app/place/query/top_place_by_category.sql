SELECT
    *
FROM
    (
        SELECT
            p.place_id,
            p.place_name,
            p.category,
            p.description,
            p.province,
            AVG(upr.rating) AS avg_rating,
            COUNT(upr.rating) AS rating_count,
            ROW_NUMBER() OVER (
                PARTITION BY p.category
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
            p.province
    ) ranked
WHERE
    rank <= {limit}
ORDER BY
    category,
    rank;
