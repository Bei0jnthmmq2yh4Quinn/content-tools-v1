// Simple SearXNG search helper (Node 18+)
// Usage: node searxng_tool.js "query" [baseUrl]

const query = process.argv.slice(2).join(' ').trim();
if (!query) {
  console.error('Usage: node searxng_tool.js "query" [baseUrl]');
  process.exit(2);
}
const baseUrl = process.env.SEARXNG_BASE_URL || 'https://search.znka.me';
const url = new URL('/search', baseUrl);
url.searchParams.set('q', query);
url.searchParams.set('format', 'json');
url.searchParams.set('safesearch', '1');
url.searchParams.set('language', 'auto');
url.searchParams.set('categories', 'general');
url.searchParams.set('pageno', '1');

(async () => {
  const res = await fetch(url, {
    headers: {
      'accept': 'application/json',
      'user-agent': 'openclaw-searxng-tool/0.1'
    }
  });
  if (!res.ok) {
    const text = await res.text().catch(() => '');
    console.error(`HTTP ${res.status}: ${text.slice(0, 500)}`);
    process.exit(1);
  }
  const data = await res.json();
  const results = (data.results || []).slice(0, 10).map(r => ({
    title: r.title,
    url: r.url,
    snippet: r.content
  }));
  console.log(JSON.stringify({ query, results }, null, 2));
})();
