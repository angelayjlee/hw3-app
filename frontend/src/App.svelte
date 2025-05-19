<script lang="ts">
  import { onMount } from 'svelte';
  import svelteLogo from './assets/svelte.svg';
  import viteLogo from '/vite.svg';
  import Counter from './lib/Counter.svelte';

  let apiKey: string = '';
  let articles: any[] = [];
  let currentDate: string = '';
  
  let showDropdown = false;

  function toggleDropdown() {
    showDropdown = !showDropdown;
  }

  function login() {
    // Redirect to your backend's login endpoint
    window.location.href = 'http://localhost:8000/login';
  }

  function getCurrentDate(): string {
    const today = new Date();
    const options: Intl.DateTimeFormatOptions = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    return today.toLocaleDateString('en-US', options); // e.g., "Wednesday, April 16, 2025"
  }

<<<<<<< Updated upstream
=======
  let userInfo: { loggedIn: boolean, email?: string, name?: string } = { loggedIn: false };

  async function fetchUserInfo() {
    try {
      const res = await fetch('http://localhost:8000/api/user', { credentials: 'include' });
      userInfo = await res.json();
    } catch {
      userInfo = { loggedIn: false };
    }
  }



>>>>>>> Stashed changes
  onMount(async () => {
    currentDate = getCurrentDate();
    await fetchArticles();
    try {
<<<<<<< Updated upstream
      const res = await fetch('/api/key');
      const data = await res.json();
      apiKey = data.apiKey;
    } catch (error) {
=======
      const res = await fetch('http://localhost:8000/api/user', { credentials: 'include' }); // Make request to backend for API key
      const data = await res.json(); // Parse the response as JSON
      apiKey = data.apiKey; // Store the API key
    } catch (error) { // Call function to fetch articles after API key is retrieved
>>>>>>> Stashed changes
      console.error('Failed to fetch API key:', error);
      
    }
  }); 

<<<<<<< Updated upstream
    // Function to fetch articles from backend (which fetches from NYT)
=======
    try {
    const userRes = await fetch('http://localhost:8000/api/user', { credentials: 'include' });
    userInfo = await userRes.json();
    console.log('User info:', userInfo);
  } catch (error) {
    userInfo = { loggedIn: false };
    console.error('Failed to fetch user info:', error);
  }

  

  });

  // Function to fetch articles from backend (which fetches from NYT)
>>>>>>> Stashed changes
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

//------------------------
  // --- Commenting State ---
  let comments: { [key: string]: any[] } = {}; // article_id -> comments array
  let newComment: { [key: string]: string } = {}; // article_id -> new comment text

  // --- Authentication State (replace with real logic) ---
  let isAuthenticated: boolean = false;
  let isModerator: boolean = false;
  let currentUser: string = '';

  // Fetch authentication status (replace with real logic)
  async function fetchAuthStatus() {
    try {
      const res = await fetch('/api/auth/status');
      const data = await res.json();
      isAuthenticated = data.isAuthenticated;
      isModerator = data.isModerator;
      currentUser = data.user;
    } catch {
      isAuthenticated = false;
      isModerator = false;
      currentUser = '';
    }
  }

  // Fetch comments for all articles
  async function fetchComments() {
    for (const article of articles) {
      const id = article._id || article.web_url; // fallback if _id missing
      try {
        const res = await fetch(`/api/comments?article_id=${encodeURIComponent(id)}`);
        const data = await res.json();
        comments[id] = data.comments;
      } catch (e) {
        comments[id] = [];
      }
    }
  }

  // Post a new comment
  async function postComment(articleId: string) {
    if (!newComment[articleId]) return;
    try {
      const res = await fetch('/api/comments', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          article_id: articleId,
          text: newComment[articleId],
          user: currentUser // or get from session
        })
      });
      if (res.ok) {
        newComment[articleId] = '';
        await fetchComments();
      }
    } catch (e) {
      alert('Failed to post comment');
    }
  }

  // Remove a comment (moderator only)
  async function removeComment(commentId: string, articleId: string) {
    try {
      const res = await fetch(`/api/comments/${commentId}`, { method: 'DELETE' });
      if (res.ok) {
        await fetchComments();
      }
    } catch (e) {
      alert('Failed to remove comment');
    }
  }



</script>


<<<<<<< Updated upstream
=======

>>>>>>> Stashed changes
<main>
  <header>
    <h1 class="logo">The New York Times</h1>
    <div class="date-header">
      <div class="date">{currentDate}</div>
      <div class="today-label">Today's Paper</div>
    </div>
<<<<<<< Updated upstream
    <hr class="headline-divider">
=======


     <!-- Login or Account button -->
     {#if !userInfo.loggedIn}
     <button class="dex-login-button" on:click={login}>Log In</button>
   {:else}
     <div class="account-container">
     <button class="account-btn" on:click={toggleDropdown}>
       Account ({userInfo.name} {userInfo.email})
     </button>

     {#if showDropdown}
       <aside class="sidebar">
         <div class="sidebar-content">
           <h3>Good morning, {userInfo.name} {userInfo.email}</h3>
           <p>{userInfo.email}</p>
           <a class="logout-link" href="http://localhost:8000/logout">Logout</a>
         </div>
       </aside>
     {/if}
   </div>

   {/if}
>>>>>>> Stashed changes
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

        <!-- Comment Section -->
        <section class="comments">
          <h3>Comments</h3>
          {#each comments[article._id] ?? [] as comment}
            <div class="comment">
              {#if comment.removed}
                <em>COMMENT REMOVED BY MODERATOR!</em>
              {:else}
                <strong>{comment.user}</strong>: {comment.text}
                {#if isModerator}
                  <button on:click={() => removeComment(comment._id, article._id)}>Remove</button>
                {/if}
              {/if}
            </div>
          {/each}
          {#if isAuthenticated}
            <form on:submit|preventDefault={() => postComment(article._id)}>
              <input bind:value={newComment[article._id]} placeholder="Add a comment..." required />
              <button type="submit">Post</button>
            </form>
          {:else}
            <p><a href="/login">Log in to comment</a></p>
          {/if}
        </section>


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

        <!-- Comment Section -->
        <section class="comments">
          <h3>Comments</h3>
          {#each comments[article._id] ?? [] as comment}
            <div class="comment">
              {#if comment.removed}
                <em>COMMENT REMOVED BY MODERATOR!</em>
              {:else}
                <strong>{comment.user}</strong>: {comment.text}
                {#if isModerator}
                  <button on:click={() => removeComment(comment._id, article._id)}>Remove</button>
                {/if}
              {/if}
            </div>
          {/each}
          {#if isAuthenticated}
            <form on:submit|preventDefault={() => postComment(article._id)}>
              <input bind:value={newComment[article._id]} placeholder="Add a comment..." required />
              <button type="submit">Post</button>
            </form>
          {:else}
            <p><a href="/login">Log in to comment</a></p>
          {/if}
        </section>






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



        <!-- Comment Section -->
        <section class="comments">
          <h3>Comments</h3>
          {#each comments[article._id] ?? [] as comment}
            <div class="comment">
              {#if comment.removed}
                <em>COMMENT REMOVED BY MODERATOR!</em>
              {:else}
                <strong>{comment.user}</strong>: {comment.text}
                {#if isModerator}
                  <button on:click={() => removeComment(comment._id, article._id)}>Remove</button>
                {/if}
              {/if}
            </div>
          {/each}
          {#if isAuthenticated}
            <form on:submit|preventDefault={() => postComment(article._id)}>
              <input bind:value={newComment[article._id]} placeholder="Add a comment..." required />
              <button type="submit">Post</button>
            </form>
          {:else}
            <p><a href="/login">Log in to comment</a></p>
          {/if}
        </section>


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

