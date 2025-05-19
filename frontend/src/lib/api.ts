export async function fetchArticles() {
    const res = await fetch('/api/articles');
    const data = await res.json();
    return data.results;
  }

