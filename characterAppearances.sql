SELECT 
    Character, 
    (SELECT COUNT(acc.Character) 
    FROM Appearance_Chapter_Character acc
    WHERE Character = acc.Character)
FROM Appearance_Chapter_Character;