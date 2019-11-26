SELECT DISTINCT
    House, 
    (SELECT COUNT(House) FROM House_Battle hb 
    WHERE hb.House = House)
    AS Battle_Count
FROM House_Batlle;