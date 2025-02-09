import { Elysia, t } from "elysia";
import { swagger } from "@elysiajs/swagger";
import { Logestic } from 'logestic';
import RSSParser from 'rss-parser';

const doc = {
  info: {
    title: "imnyang's Personal API",
    description: "Neko is cute.",
    version: "1.0.0",
    contact: {
      name: "HyunSuk Nam",
      url: "https://imnya.ng",
      email: "support@orygonix.com"
    },
    license: {
      name: "CC0-1.0 license",
      url: "https://creativecommons.org/publicdomain/zero/1.0/",
    }
  },
  servers: process.env.NODE_ENV === 'development' ? [
    {
      url: 'http://localhost:3000',
      description: "Local server"
    },
    {
      url: 'https://api.imnya.ng',
      description: "Production server"
    }
  ] : [
    {
      url: 'https://api.imnya.ng',
      description: "Production server"
    },
    {
      url: 'http://localhost:3000',
      description: "Local server"
    }
  ]
};

const app = new Elysia()
  .get("/", () => "Hello Elysia")
  .get("/rss", async () => {
    const parser = new RSSParser();
    const feed = await parser.parseURL('https://blog.imnya.ng/rss.xml');
    return feed.items;
  })
  
  .use(swagger({documentation: doc}))
  .use(Logestic.preset('fancy'))
  .listen(3000)
;

console.log(
  `🦊 Elysia is running at ${app.server?.hostname}:${app.server?.port}`
);
