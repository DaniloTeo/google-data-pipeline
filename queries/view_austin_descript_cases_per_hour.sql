SELECT
  descript,
  REGEXP_EXTRACT(safe_cast(time as STRING), "^([0-9]{2}):") as hour,
  COUNT(*) as occurrences
FROM
  `bi-psel.danilo_teo.austin_incidents`
GROUP BY
  descript,
  hour
ORDER BY hour asc, descript asc