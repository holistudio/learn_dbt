SELECT borough, SUM(lotarea) AS total_sqft
FROM {{ ref('int_vacant_lots') }}
GROUP BY borough;