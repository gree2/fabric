# http://stackoverflow.com/questions/15242757/import-csv-file-into-sql-server
BULK INSERT [links]   FROM 'D:\\Data\\links.csv'
    WITH (FIRSTROW = 2,
        FIELDTERMINATOR = ',',
        ROWTERMINATOR = '\n',
        ERRORFILE = 'D:\\Data\\links_error.csv',
        TABLOCK );
GO
BULK INSERT [movies]  FROM 'D:\\Data\\movies.csv'
    WITH (FIRSTROW = 2,
        FIELDTERMINATOR = ',',
        ROWTERMINATOR = '\n',
        ERRORFILE = 'D:\\Data\\movies_error.csv',
        TABLOCK );
GO
BULK INSERT [ratings] FROM 'D:\\Data\\ratings.csv'
    WITH (FIRSTROW = 2,
        FIELDTERMINATOR = ',',
        ROWTERMINATOR = '\n',
        ERRORFILE = 'D:\\Data\\ratings_error.csv',
        TABLOCK );
GO
BULK INSERT [tags]    FROM 'D:\\Data\\tags.csv'
    WITH (FIRSTROW = 2,
        FIELDTERMINATOR = ',',
        ROWTERMINATOR = '\n',
        ERRORFILE = 'D:\\Data\\tags_error.csv',
        TABLOCK );
GO