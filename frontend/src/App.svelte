<script lang="ts">
  import { onMount } from 'svelte';
 

  let apiKey: string = '';
  let articles: any[] = [];
  let currentDate: string = '';

  function getCurrentDate(): string {
    const today = new Date();
    const options: Intl.DateTimeFormatOptions = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    return today.toLocaleDateString('en-US', options); // e.g., "Wednesday, April 16, 2025"
  }

  onMount(async () => {
    currentDate = getCurrentDate();
    await fetchArticles();
    try {
      const res = await fetch('http://localhost:8000/api/key'); // Make request to backend for API key
      const data = await res.json(); // Parse the response as JSON
      apiKey = data.apiKey; // Store the API key
    } catch (error) { // Call function to fetch articles after API key is retrieved
      console.error('Failed to fetch API key:', error);
    }
  });

  // Function to fetch articles from backend (which fetches from NYT)
  const fetchArticles = async () => {
    try{
      const res = await fetch('http://localhost:8000/api/articles'); // Make request to backend for articles
      const data = await res.json(); // Parse the response as JSON
      articles = data.results; // Results key contains articles
      console.log("First article's multimedia:", articles[0]?.multimedia);
    } catch (error) {
      console.error('Failed to fetch articles:', error);
    }
  }
</script>

<main>
  <header>
    <h1 class="logo">The New York Times</h1>
    <div class="date-header">
      <div class="date">{currentDate}</div>
      <div class="today-label">Today's Paper</div>
    </div>
    <hr class="headline-divider">
  </header>

  <div class="content">
    <section class="column 1">
      {#each articles.slice(0, 3) as article}
        <article class="article">
          <h2>{article.headline.main}</h2>
          <p>{article.abstract}</p>

          {#if article.multimedia && article.multimedia.default}
          <img src={article.multimedia.default.url} alt={article.title} />
          {/if}

          <p class="meta">5 min read</p>

          {#if article.web_url}
          <a href={article.web_url} target="_blank" rel="noopener noreferrer" class="readMore-link">
          read full article
          </a>
          {:else}
          <p>No URL available</p>
        {/if}

        <hr />
        </article>
      {/each}
    </section>

    <section class="column 2">
      {#each articles.slice(3, 5) as article}
        <article class="article">
          <h2>{article.headline.main}</h2>
          <p>{article.abstract}</p>

          {#if article.multimedia && article.multimedia.default}
          <img src={article.multimedia.default.url} alt={article.title} />
          {/if}

          <p class="meta">5 min read</p>
  
          {#if article.web_url}
          <a href={article.web_url} target="_blank" rel="noopener noreferrer" class="readMore-link">
          read full article
          </a>
          {:else}
          <p>No URL available</p>
        {/if}

        <hr />
        </article>
      {/each}
    </section>

    <section class="column 3">
      {#each articles.slice(5, 7) as article}
        <article class="article">
          <h2>{article.headline.main}</h2>
          <p>{article.abstract}</p>

          {#if article.multimedia && article.multimedia.default}
          <img src={article.multimedia.default.url} alt={article.title} />
          {/if}

          <p class="meta">5 min read</p>
         
          {#if article.web_url}
          <a href={article.web_url} target="_blank" rel="noopener noreferrer" class="readMore-link">
          read full article
          </a>
          {:else}
          <p>No URL available</p>
        {/if}

        <hr />
        </article>
      {/each}
    </section>
  </div>

  <footer>
    <div class="footer-content">
      <p>ChatGPT MLA Citation: OpenAI. "Prompt." *ChatGPT*, 15 Apr. 2025, chat.openai.com/chat.  
        — "Response."
      </p>
      <p>HTML Citation: W3Schools. "HTML Tutorial." *W3Schools*, 2025</p>
      <p>CSS Citation: W3Schools. "CSS Tutorial." *W3Schools*, 2025</p>
    </div>
  </footer>
</main>


