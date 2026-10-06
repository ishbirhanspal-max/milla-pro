export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname;

    // Normal fetch from Cloudflare Static Assets
    const res = await env.ASSETS.fetch(request);

    // If Cloudflare returns a 30x redirect loop on subpages, serve the .html directly
    if (res.status >= 300 && res.status < 400) {
      const loc = res.headers.get('Location') || '';
      // Check if location redirects to same path (loop) or strips .html
      if (loc === path || loc === path.replace(/\.html$/, '') || loc + '.html' === path || loc + '/' === path) {
        const cleanPath = path.endsWith('.html') ? path : path.replace(/\/$/, '') + '.html';
        const newUrl = new URL(cleanPath, request.url);
        const directRes = await env.ASSETS.fetch(new Request(newUrl, request));
        if (directRes.status === 200) {
          return directRes;
        }
      }
    }

    return res;
  }
};
