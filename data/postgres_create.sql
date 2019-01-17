CREATE TABLE "Authors" (
	"id" serial,
	"name" varchar,
	CONSTRAINT Authors_pk PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Functions" (
	"id" serial,
	"signature" VARCHAR(255) NOT NULL UNIQUE,
	CONSTRAINT Functions_pk PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Lines" (
	"id" serial NOT NULL,
	"commit_id" integer NOT NULL,
	"author_id" integer NOT NULL,
	"function_id" integer NOT NULL,
	"file_id" integer NOT NULL,
	"line_no" integer NOT NULL,
	CONSTRAINT Lines_pk PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Commits" (
	"id" serial NOT NULL,
	"hash" varchar NOT NULL UNIQUE,
	"time" timestamptz NOT NULL,
	CONSTRAINT Commits_pk PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Files" (
	"id" serial NOT NULL,
	"file_path" varchar NOT NULL,
	CONSTRAINT Files_pk PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);





ALTER TABLE "Lines" ADD CONSTRAINT "Lines_fk0" FOREIGN KEY ("commit_id") REFERENCES "Commits"("id");
ALTER TABLE "Lines" ADD CONSTRAINT "Lines_fk1" FOREIGN KEY ("author_id") REFERENCES "Authors"("id");
ALTER TABLE "Lines" ADD CONSTRAINT "Lines_fk2" FOREIGN KEY ("function_id") REFERENCES "Functions"("id");
ALTER TABLE "Lines" ADD CONSTRAINT "Lines_fk3" FOREIGN KEY ("file_id") REFERENCES "Files"("id");



