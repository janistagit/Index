-- Table: public.index

-- DROP TABLE IF EXISTS public.index;

CREATE TABLE IF NOT EXISTS public.index
(
    doc_documents integer NOT NULL,
    term_terms character varying COLLATE pg_catalog."default" NOT NULL,
    count integer NOT NULL,
    CONSTRAINT index_pkey PRIMARY KEY (doc_documents, term_terms)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.index
    OWNER to postgres;