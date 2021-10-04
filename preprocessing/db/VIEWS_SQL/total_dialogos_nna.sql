CREATE VIEW total_dialogos_nna AS
SELECT DISTINCT 
    id_mesa,
    cantidad_participantes,
    rango_edades_id,
    region_name,
    region_iso
FROM 
    necesidades_nna;