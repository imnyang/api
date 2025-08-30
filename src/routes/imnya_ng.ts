import cron, { Patterns } from "@elysiajs/cron";
import Elysia from "elysia";
import RSSParser from 'rss-parser';
import { discord_headers, discord_payload } from "../../config";

let invite_link = "";

async function discord_invite_heartbeat(): Promise<string> {
    // The target URL for the POST request
    const url = "https://discord.com/api/v9/users/@me/invites";

    const response = await fetch(url, {
        method: 'POST',
        headers: discord_headers,
        body: JSON.stringify(discord_payload)
    });

    if (response.ok) {
        console.log('Heartbeat sent successfully');
        const data = await response.json();
        return data.code || "";
    } else {
        console.error('Failed to send heartbeat', response.status, await response.text());
        return "";
    }
}

invite_link = await discord_invite_heartbeat(); // Initial call

const imnyang = new Elysia()
    .use(cron({
        name: 'discord_invite',
        pattern: Patterns.EVERY_WEEK,
        async run() {
            invite_link = await discord_invite_heartbeat(); // Initial call
            console.log('New invite link:', invite_link);
        }
    }))

    .get("/discord_invite", () => {
        return `https://discord.gg/${invite_link}`;
    })

    .get("/rss", async () => {
        const parser = new RSSParser();
        const feed = await parser.parseURL('https://blog.imnya.ng/rss.xml');
        return feed.items;
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

export default imnyang;