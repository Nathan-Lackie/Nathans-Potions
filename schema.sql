-- Capacity
CREATE TABLE
    public.capacity (
        type TEXT NOT NULL,
        capacity INTEGER NOT NULL,
        CONSTRAINT capacity_pkey PRIMARY KEY (
            type,
            capacity
        ),
        CONSTRAINT capacity_type_key UNIQUE (
            type
        )
    ) TABLESPACE pg_default;

ALTER TABLE public.capacity OWNER TO postgres;

INSERT INTO public.capacity
("type", "capacity") VALUES
('liquid', '1'),
('potion', '1');

-- Customers
CREATE TABLE
    public.customers (
        id BIGINT GENERATED BY DEFAULT AS IDENTITY NOT NULL,
        name TEXT NOT NULL,
        character_class TEXT NOT NULL,
        level SMALLINT NOT NULL,
        CONSTRAINT customers_pkey PRIMARY KEY (id),
        CONSTRAINT customers_unique UNIQUE (name, character_class, level)
    ) TABLESPACE pg_default;

ALTER TABLE public.customers OWNER TO postgres;

-- Gold
CREATE TABLE
    public.gold (
        id BIGINT GENERATED BY DEFAULT AS IDENTITY NOT NULL,
        update INTEGER NOT NULL,
        timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
        CONSTRAINT gold_pkey PRIMARY KEY (id)
    ) TABLESPACE pg_default;

ALTER TABLE public.gold OWNER TO postgres;

INSERT INTO public.gold
("update") VALUES
(100);

-- Liquid
CREATE TYPE liquid_color AS ENUM ('red', 'green', 'blue', 'dark');
CREATE TABLE
    public.liquid (
        id BIGINT GENERATED BY DEFAULT AS IDENTITY NOT NULL,
        color public.liquid_color NOT NULL,
        update INTEGER NOT NULL,
        timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
        CONSTRAINT liquid_pkey PRIMARY KEY (id)
    ) TABLESPACE pg_default;

ALTER TABLE public.liquid OWNER TO postgres;

-- Potions
CREATE TABLE
    public.potions (
        sku TEXT NOT NULL,
        name TEXT NOT NULL,
        red SMALLINT NOT NULL,
        green SMALLINT NOT NULL,
        blue SMALLINT NOT NULL,
        dark SMALLINT NOT NULL,
        price INTEGER NOT NULL DEFAULT 50,
        quantity INTEGER NOT NULL DEFAULT 0,
        desired_quantity INTEGER NULL,
        show_in_catalog BOOLEAN NOT NULL DEFAULT TRUE,
        CONSTRAINT potions_pkey PRIMARY KEY (sku),
        CONSTRAINT potions_unique_type UNIQUE (red, green, blue, dark),
        CONSTRAINT potion_sku_name CHECK ((sku ~ '^[a-zA-Z0-9_]{1,20}$'::text)),
        CONSTRAINT potion_valid_price CHECK (
            (
                (1 <= price)
                AND (price <= 500)
            )
        ),
        CONSTRAINT potions_sum_100 CHECK (((((red + green) + blue) + dark) = 100))
    ) TABLESPACE pg_default;

ALTER TABLE public.potions OWNER TO postgres;

INSERT INTO public.potions
(sku,              name,                  red, green, blue, dark, price, quantity, desired_quantity, show_in_catalog) VALUES
('ORANGE_POTION', 'Fire Potion',          75,  25,    0,    0,    50,    0,        NULL,             TRUE),
('GREEN_POTION',  'Druid''s Delight',     0,   100,   0,    0,    50,    0,        NULL,             TRUE),
('DARK_POTION',   'Dark Potion',          0,   0,     0,    100,  75,    0,        NULL,             TRUE),
('BLUE_POTION',   'Blue Potion',          0,   0,     100,  0,    50,    0,        NULL,             TRUE),
('YELLOW_ORANGE', 'Yellow Orange Potion', 50,  50,    0,    0,    50,    0,        NULL,             TRUE),
('RED_POTION',    'Fighter''s Fury',      100, 0,     0,    0,    50,    0,        NULL,             TRUE);

-- Time
CREATE TABLE
    public.time (
        day TEXT NOT NULL,
        hour SMALLINT NOT NULL,
        CONSTRAINT time_pkey PRIMARY KEY (day, hour)
    ) TABLESPACE pg_default;

ALTER TABLE public.time OWNER TO postgres;

INSERT INTO public.time
(day, hour) VALUES
('Edgeday', 0);

-- Visits
CREATE TABLE
    public.visits (
        id BIGINT GENERATED BY DEFAULT AS IDENTITY NOT NULL,
        customer_id BIGINT NOT NULL,
        day TEXT NOT NULL,
        hour SMALLINT NOT NULL,
        timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
        CONSTRAINT visits_pkey PRIMARY KEY (id),
        CONSTRAINT visits_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES customers (id) ON UPDATE CASCADE
    ) TABLESPACE pg_default;

ALTER TABLE public.visits OWNER TO postgres;

-- Carts
CREATE TABLE
    public.carts (
        id BIGINT NOT NULL,
        potion_sku TEXT NOT NULL,
        quantity SMALLINT NOT NULL,
        CONSTRAINT carts_pkey PRIMARY KEY (id, potion_sku),
        CONSTRAINT carts_id_fkey FOREIGN KEY (id) REFERENCES visits (id),
        CONSTRAINT carts_potion_sku_fkey FOREIGN KEY (potion_sku) REFERENCES potions (sku) ON UPDATE CASCADE
    ) TABLESPACE pg_default;

ALTER TABLE public.carts OWNER TO postgres;
