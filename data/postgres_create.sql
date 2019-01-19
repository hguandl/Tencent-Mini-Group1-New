CREATE TABLE "Authors" (
	"id" serial,
	"name" varchar,
	CONSTRAINT Authors_pk PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Signatures" (
	"id" serial,
	"signature" text NOT NULL UNIQUE,
	CONSTRAINT Signatures_pk PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Changes" (
	"id" serial NOT NULL,
	"commit_id" integer NOT NULL,
	"author_id" integer NOT NULL,
	"signature_id" integer NOT NULL,
	"file_id" integer NOT NULL,
	CONSTRAINT Changes_pk PRIMARY KEY ("id")
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





ALTER TABLE "Changes" ADD CONSTRAINT "Changes_fk0" FOREIGN KEY ("commit_id") REFERENCES "Commits"("id");
ALTER TABLE "Changes" ADD CONSTRAINT "Changes_fk1" FOREIGN KEY ("author_id") REFERENCES "Authors"("id");
ALTER TABLE "Changes" ADD CONSTRAINT "Changes_fk2" FOREIGN KEY ("signature_id") REFERENCES "Signatures"("id");
ALTER TABLE "Changes" ADD CONSTRAINT "Changes_fk3" FOREIGN KEY ("file_id") REFERENCES "Files"("id");



