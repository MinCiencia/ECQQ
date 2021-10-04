CREATE TABLE propuestas_nna
(
    id integer PRIMARY KEY,
	id_mesa integer,
    dominant_topic integer,
    topic_perc_contrib float,
    keywords varchar(256),
    text varchar(1024),
    topico varchar(64),
    organizacion varchar(128),
    rango_edades_id varchar(16),
    cantidad_participantes integer,
    inst varchar(64),    
    region_iso varchar(16),
    region_name varchar(32),
    comuna_iso varchar(16),
    comuna_name varchar(32),    
    source varchar(16), 
    target varchar(16)
);
