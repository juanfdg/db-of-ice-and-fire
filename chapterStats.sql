SELECT
    ID_Book, POV, MAX(POV_Sequence) AS Num_Chapters
FROM Chapter
GROUP BY ID_Book, POV;

SELECT
    POV, SUM(Num_Chapters) AS Total_Chapters
FROM (SELECT
        ID_Book, POV, MAX(POV_Sequence) AS Num_Chapters
    FROM Chapter
    GROUP BY ID_Book, POV
    )
GROUP BY POV
ORDER BY Total_Chapters;
