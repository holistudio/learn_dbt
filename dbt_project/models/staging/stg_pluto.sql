WITH source_data AS (
    SELECT * FROM {{ source('pluto_raw', 'pluto') }}
)

SELECT 
    * EXCEPT (lotarea),
    SAFE_CAST(lotarea AS NUMERIC) AS lotarea
FROM source_data