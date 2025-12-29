use pokemon


BULK INSERT pokemon_species
FROM 'C:\Users\haven\OneDrive\Documents\SQL Server Management Studio 21\City of Corvallis Queries\Personal Queries\Pokemon Simulation\Github Project\Modified Pokemon Database CSV.csv'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    FORMAT='CSV',
    TABLOCK
);


insert into pokeball (pokeball_id,pokeball_name,catch_rate_mult)
values
(1, 'pokeball',1),
(2, 'greatball',1.5),
(3, 'ultraball',2),
(4, 'masterball',100)