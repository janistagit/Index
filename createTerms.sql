-- Table: public.terms

-- DROP TABLE IF EXISTS public.terms;

CREATE TABLE IF NOT EXISTS public.terms
(
    term character varying COLLATE pg_catalog."default" NOT NULL,
    num_chars integer NOT NULL,
    CONSTRAINT terms_pkey PRIMARY KEY (term)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.terms
    OWNER to postgres;