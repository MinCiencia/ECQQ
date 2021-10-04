regiones_name = [
    "Tarapacá",
    "Antofagasta",
    "Atacama",
    "Coquimbo",
    "Valparaíso",
    "O’Higgins",
    "Maule",
    "Biobío",
    "Araucanía",
    "RM",
    "Los Ríos",
    "Los Lagos",
    "Aysén",
    "Magallanes",
    "Arica y Parinacota",
    "Ñuble",
]

regiones_iso = [
    'CL-TA', 
    'CL-AN', 
    'CL-AT',
    'CL-CO',  
    'CL-VS',        
    'CL-OH', 
    'CL-MA',
    'CL-BI', 
    'CL-AR', 
    'CL-RM', 
    'CL-LR', 
    'CL-LL',
    'CL-AI', 
    'CL-MG', 
    'CL-AP',   
    'CL-NB',
]

columnas = [
    'id_user',
    'id_file',
    'age',
    'sex',
    'comuna',
    'region',
    'education', 
    'group',
    'date',
    'init_time',
    'end_time',
    'priority',
    'emotion',
    'age_range',
    'code_comuna',
    'emotion_verified',
    'emotion_verified2',
]

new_columnas = [
    'id_user',
    'id_file',
    'age',
    'sex',
    'comuna',
    'region',
    'region_iso',
    'education', 
    'group',
    'date',
    'init_time',
    'end_time',
    'priority',
    'emotion',
    'age_range',
    'code_comuna',
    'emotion_verified',
    'emotion_verified2',
]

sex_options = ['F', 'H', 'OTRO']

sex_wrong = ['Básica_Incompleta', 'Básica_Completa', 'Media_Incompleta', 'Universitaria_Completa', 'Técnico_Incompleto', 'Técnico_Completo']

education_name = {
    'basica_incompleta' : 'Básica Incompleta',
    'basica_completa' : 'Básica Completa',
    'tecnico_completo' : 'Técnico Completo',
    'universitaria_completa' : 'Universitaria Completa',
    'universitaria_incompleta' : 'Universitaria Incompleta',
    'media_incompleta' : 'Media Incompleta',
    'media_completa' : 'Media Completa',
    'postgrado' : 'Postgrado',
    'sin_edu_formal' : 'Sin Educatión Formal',
    'indeterminado' : 'Indeterminado',
    'educacion_especial' : 'Educación Especial',
    'tecnico_incompleto' : 'Técnico Incompleto',
    'nr' : 'NR',
}

education_wrong = ['h', 'f']

education_options = [
    'basica_incompleta',
    'basica_completa',
    'tecnico_completo',
    'universitaria_completa',
    'universitaria_incompleta',
    'media_incompleta',
    'media_completa', 
    'postgrado',
    'sin_edu_formal',
    'indeterminado',
    'educacion_especial',
    'tecnico_incompleto',
]

educ_dict = {
    'basica_incompleta': 'Educación básica incompleta o inferior',
    'basica_completa': 'Básica completa',
    'tecnico_completo' : 'Técnica completa',
    'universitaria_completa': 'Universitaria completa',
    'media_incompleta' : 'Media incompleta (incluyendo Media Técnica)',
    'media_completa' : 'Media completa. Técnica incompleta',
    'universitaria_incompleta': 'Universitaria incompleta. Técnica completa',
    'postgrado'  : 'Post Grado (Master, Doctor o equivalente)',
    'indeterminado' : '',
    'sin_edu_formal' : '',
    'tecnico_incompleto': 'Media completa. Técnica incompleta',
    'educacion_especial' : '',
    '': ''
}