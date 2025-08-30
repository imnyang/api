import { Elysia, t } from "elysia";
import { swagger } from "@elysiajs/swagger";
import { Logestic } from 'logestic';
import cors from "@elysiajs/cors";
import cron, { Patterns } from "@elysiajs/cron";
import doc from './docs';

import hrts_chrome from "./routes/hrts_chrome";
import imnyang from "./routes/imnya_ng";

const app = new Elysia()

  .get("/", () => "Hello Elysia")

  .use(hrts_chrome)
  .use(imnyang)

  .use(swagger({ documentation: doc }))
  .use(Logestic.preset('fancy'))
  .use(cors({
    origin: '*',
    methods: '*'
  }))
  .listen(1108);

console.log(
  `🦊 Elysia is running at ${app.server?.hostname}:${app.server?.port}`
);
