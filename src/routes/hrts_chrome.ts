import { Elysia, t } from "elysia";

const hrts_chrome = new Elysia()
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
    });

export default hrts_chrome;