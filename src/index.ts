import { Elysia, t } from "elysia";
import { swagger } from "@elysiajs/swagger";
import { Logestic } from 'logestic';
import RSSParser from 'rss-parser';
import cors from "@elysiajs/cors";

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
      url: 'https://api.imnya.ng',
      description: "Production server"
    },
    {
      url: 'http://localhost:1108',
      description: "Local server"
    }
  ] : [

    {
      url: 'http://localhost:1108',
      description: "Local server"
    },
    {
      url: 'https://api.imnya.ng',
      description: "Production server"
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
  .get("/google/complete", async ({ query }) => {
    const language = query.hl || 'en';
    const keyword = query.q || '';
    const url = `https://suggestqueries.google.com/complete/search?output=toolbar&hl=${language}&q=${keyword}`;
    const response = await fetch(url);
    const suggestions = await response.text();
    return new Response(suggestions, {
      headers: { 'Content-Type': 'application/xml' }
    });
  }, {
    query: t.Object({
      hl: t.String(),
      q: t.String()
    })
  })
  .get("/wakatime", async () => {
    try {
      const res = await fetch("https://wakatime.com/api/v1/users/imnyang/stats/all_time");
      const json = await res.json();
      return json;
    } catch (err) {
      console.error(err);
      return { error: "Fetch failed" };
    }
  })
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
