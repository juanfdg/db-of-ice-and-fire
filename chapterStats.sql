SELECT
    POV, 
    (SELECT COUNT(POV)
    FROM Chapter c
    WHERE c.POV = POV) AS Total_Chapters
FROM Chapter
ORDER BY Total_Chapters;
