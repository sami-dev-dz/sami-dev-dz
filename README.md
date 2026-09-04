<p align="center">
  <samp>
    <a href="https://portfolio-sami-dev.vercel.app">portfolio</a> ·
    <a href="https://www.linkedin.com/in/sami-ghoul-8773893ba/">linkedin</a> ·
    <a href="https://khamsat.com/user/sami_dev_dz/reviews">client reviews</a> ·
    <a href="mailto:sami.codefree@gmail.com">email</a>
  </samp>
</p>

### Sami Ghoul

Software engineer in Béjaïa, Algeria. I build web platforms, desktop software,
and automation wired to language models.

Freelance since January 2024, rated 5.0/5 across five client engagements. Most
of what I write runs for someone else, so it has to keep working after I hand
it over.

Here is one of them, still running:

```
   4 RSS feeds
        │
        ▼
   deduplicate ······ in-memory cache first, then the WordPress API
        │
        ▼
   draft + cover ···· Gemini 2.5 Pro writes, Flash illustrates
        │
        ▼
   human gate ······· Telegram notification, webhook waits
        │
   ┌────┴────┬──────────┐
   ▼         ▼          ▼
publish    draft     cancel ··· deletes the uploaded image,
                                so no orphan media piles up
```

Built for [dro3tech.com](https://dro3tech.com). **130 articles published**, about
one every two days. Nothing reaches the site without a person saying yes, which
is the whole point: automating publication without automating the mistakes.

The workflow is public — [**quillrail**](https://github.com/sami-dev-dz/quillrail),
47 nodes, tokens replaced with environment variables and the client's details
removed. The README there covers the two decisions the design rests on: why
deduplication runs in two stages rather than one, and why cancelling has to
delete the image it already uploaded.

### Elsewhere

[**DzArtisan**](https://dzartisan-rs.vercel.app) is the largest thing I have
built. A marketplace for tradespeople across Algeria, where one Laravel API
serves the public site and the admin back office: 20 models, 45 migrations, 106
routes, real-time messaging, two-factor on admin, French and Arabic with full
RTL. 226 of its 229 commits are mine. Source is private, available on request.

Public repositories worth your time:

- [**Apple Financial RAG Agent**](https://github.com/sami-dev-dz/n8n-financial-rag-chatbot) answers questions on quarterly reports and hands back the source passage, so you can check it. The model runs locally through Ollama, so no document leaves the machine.
- [**BusTrack CRM**](https://github.com/sami-dev-dz/BusTrack-CRM) is a Java desktop CRM for a transport fleet, built offline-first because the target workstation has no guaranteed network.
- [**UniRide**](https://github.com/sami-dev-dz/UniRide) is a campus carpooling platform with MVC written by hand, no framework, to keep routing and security under direct control.

### Stack

```
backend     PHP · Laravel · Node · Express · REST · WebSockets
frontend    JavaScript · TypeScript · React · Next.js · Tailwind
automation  n8n · LangChain · RAG · Pinecone · Ollama
data        MySQL · Oracle · MongoDB · SQLite
languages   Java · Python · C
testing     Pest · Playwright
tooling     Git · Docker · Linux · Maven
```

Open to internships and freelance work on backend, architecture, and
automation. Arabic, French, English.
