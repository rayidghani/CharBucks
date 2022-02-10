CREATE TABLE bizscores (
	crawldate DATE NOT NULL,
	yelpid VARCHAR NOT NULL,
	name VARCHAR NOT NULL,
	positives int NOT NULL,
	num_images int NOT NULL,
	city VARCHAR NOT NULL,
	state VARCHAR NOT NULL,
	latitude DECIMAL,
	longitude DECIMAL,
	yelpalias VARCHAR NOT NULL,
	rating DECIMAL NOT NULL,
	num_reviews int NOT NULL
);


CREATE TABLE imgscores (
	crawldate DATE NOT NULL,
	yelpid VARCHAR NOT NULL,
	name VARCHAR NOT NULL,
	imgurl VARCHAR NOT NULL,
	score DECIMAL NOT NULL
);