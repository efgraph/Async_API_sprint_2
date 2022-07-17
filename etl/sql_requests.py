query_film_work = """SELECT fw.id, 
                    fw.title, 
                    fw.description, 
                    fw.rating, 
                    fw.type,
                    fw.modified,
                    ARRAY_REMOVE(ARRAY_AGG(distinct CASE
                        WHEN pfw.role = 'actor' 
                        THEN p.full_name
                    END), NULL) AS actors,
                    JSONB_AGG(distinct CASE
                        WHEN pfw.role = 'actor' 
                        THEN jsonb_build_object(
                            'id', p.id,
                            'name', p.full_name
                        )
                    END) AS actors_json,
                    ARRAY_REMOVE(ARRAY_AGG(distinct CASE
                        WHEN pfw.role = 'writer' 
                        THEN p.full_name
                    END), NULL) AS writers,
                    JSONB_AGG(distinct CASE
                        WHEN pfw.role = 'writer'
                        THEN jsonb_build_object(
                            'id', p.id,
                            'name', p.full_name
                        )
                    END) AS writers_json,
                    ARRAY_REMOVE(ARRAY_AGG(distinct CASE
                        WHEN pfw.role = 'director' 
                        THEN p.full_name
                    END), NULL) AS directors,
                ARRAY_REMOVE(ARRAY_AGG(distinct g.name), NULL) AS genres
                FROM film_work as fw
                LEFT JOIN person_film_work pfw ON pfw.film_work_id = fw.id
                LEFT JOIN person p ON p.id = pfw.person_id
                LEFT JOIN genre_film_work gfw ON gfw.film_work_id = fw.id
                LEFT JOIN genre g ON g.id = gfw.genre_id
                GROUP BY
                    1,2,3,4,5    
                HAVING (fw.modified::time > %s::time) AND (fw.modified::date >= %s::date)"""


query_genre = """SELECT id, name from genre WHERE (modified::time > %s::time) AND (modified::date >= %s::date)"""

query_person = """SELECT 
                        p.id, 
                        p.full_name,
                        ARRAY_REMOVE(ARRAY_AGG(distinct CASE
                            WHEN pfw.role = 'writer' 
                            THEN fw.id
                            END), NULL) AS writer,
                        ARRAY_REMOVE(ARRAY_AGG(distinct CASE
                            WHEN pfw.role = 'director' 
                            THEN fw.id
                            END), NULL) AS director,
                        ARRAY_REMOVE(ARRAY_AGG(distinct CASE
                            WHEN pfw.role = 'actor' 
                            THEN fw.id
                            END), NULL) AS actor
                        FROM person as p 
                        LEFT JOIN person_film_work pfw ON pfw.person_id = p.id
                        LEFT JOIN film_work fw ON fw.id = pfw.film_work_id
                        GROUP BY
                            1,2
                        HAVING (p.modified::time > %s::time) AND (p.modified::date >= %s::date)"""