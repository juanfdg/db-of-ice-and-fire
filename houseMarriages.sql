SELECT 
    a1.House AS Char_House, a2.House AS Spouse_House
FROM Marriage m
JOIN Allegiance a1
    ON m.Character = a1.Character
JOIN Allegiance a2
    ON m.Spouse = a2.Character;

WITH housemarr AS 
(SELECT 
    a1.House AS Char_House, a2.House AS Spouse_House
FROM Marriage m
JOIN Allegiance a1
    ON m.Character = a1.Character
JOIN Allegiance a2
    ON m.Spouse = a2.Character)
SELECT DISTINCT
    Char_House, Spouse_House, 
    (SELECT COUNT(Char_house) FROM housemarr hm 
    WHERE hm.Char_House = Char_House AND 
    hm.Spouse_House = Spouse_House) AS Marriage_Count
FROM housemarr
ORDER BY Marriage_Count;
