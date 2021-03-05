SELECT *
FROM people
LEFT JOIN scores
ON people.id = scores.id
WHERE scores.score = 'partisanship'
AND scores.value >= 50;

SELECT people.name, people.address, a.householdmeanscore
FROM people
RIGHT JOIN
	(
        SELECT AVG(scores.value) as HouseholdMeanScore, people.address
        FROM people
            LEFT JOIN scores
                ON people.id = scores.id
        WHERE scores.score = 'partisanship'
        GROUP BY people.address
        HAVING AVG(scores.value) >= 50
    ) AS a
    ON people.address = a.address;

SELECT people.address, youngest.name--, MAX(people.yob) as YoB
FROM people
--  LEFT JOIN scores
--      ON people.id = scores.id
  LEFT JOIN people youngest
  	  ON people.address = youngest.address
      AND people.yob < youngest.yob
WHERE youngest.yob IS NULL;
