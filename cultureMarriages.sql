SELECT 
    cc1.Culture AS Char_Culture, cc2.Culture AS Spouse_Culture
FROM Marriage m
JOIN Character_Culture cc1
    ON m.Character = cc1.Character
JOIN Character_Culture cc2
    ON m.Spouse = cc2.Character;

WITH cultmarr AS 
(SELECT 
    cc1.Culture AS Char_Culture, cc2.Culture AS Spouse_Culture
FROM Marriage m
JOIN Character_Culture cc1
    ON m.Character = cc1.Character
JOIN Character_Culture cc2
    ON m.Spouse = cc2.Character)
SELECT DISTINCT
    Char_Culture, Spouse_Culture, 
    (SELECT COUNT(Char_Culture) FROM housecult hc 
    WHERE hc.Char_Culture = Char_Culture AND 
    hc.Spouse_Culture = Spouse_Culture) AS Marriage_Count
FROM housecult
ORDER BY Marriage_Count;
