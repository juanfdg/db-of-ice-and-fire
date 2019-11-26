SELECT DISTINCT
    Battle_Place, 
    (SELECT COUNT(Battle_Place) FROM Battle b 
    WHERE b.Battle_Place = Battle_Place)
    AS Battle_Count
FROM Batlle;