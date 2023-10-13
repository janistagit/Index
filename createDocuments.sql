-- Table: public.documents

-- DROP TABLE IF EXISTS public.documents;

CREATE TABLE IF NOT EXISTS public.documents
(
    doc integer NOT NULL,
    text character varying COLLATE pg_catalog."default" NOT NULL,
    title character varying COLLATE pg_catalog."default" NOT NULL,
    num_chars integer NOT NULL,
    date date NOT NULL,
    id_categories integer NOT NULL,
    CONSTRAINT documents_pkey PRIMARY KEY (doc)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.documents
    OWNER to postgres;